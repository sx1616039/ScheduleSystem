import os
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optimizer
from torch.distributions import Categorical
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler
from env_solution import JobEnv


class Actor(nn.Module):
    def __init__(self, input_num, hidden_num, num_output):
        super(Actor, self).__init__()
        self.rnn = nn.RNN(  # if use nn.RNN(), it hardly learns
            input_size=input_num,
            hidden_size=hidden_num,  # rnn hidden unit
            num_layers=1,  # number of rnn layer
            batch_first=True,  # input & output will has batch size as 1s dimension. e.g. (batch, time_step, input_size)
        )
        self.fc1 = nn.Linear(hidden_num, hidden_num)
        self.action_head = nn.Linear(hidden_num, num_output)

    def forward(self, x, h_state=None):
        # r_out, (h_n, h_c) = self.rnn(x, None)
        r_out, h_state = self.rnn(x.view(len(x), 1, -1), h_state)
        # r_out, (h_n, h_c) = self.rnn(x.view(len(x), 1, -1), hidden)
        x = r_out[:, -1, :]
        x = F.relu(self.fc1(x))
        out = self.action_head(x)
        action_prob = F.softmax(out, dim=1)
        return action_prob


class Critic(nn.Module):
    def __init__(self, input_num, hidden_num, num_output=1):
        super(Critic, self).__init__()
        self.rnn = nn.RNN(  # if use nn.RNN(), it hardly learns
            input_size=input_num,
            hidden_size=hidden_num,  # rnn hidden unit
            num_layers=1,  # number of rnn layer
            batch_first=True,  # input & output will has batch size as 1s dimension. e.g. (batch, time_step, input_size)
        )
        self.fc1 = nn.Linear(hidden_num, hidden_num)
        self.state_value = nn.Linear(hidden_num, num_output)

    def forward(self, x, h_state=None):
        # r_out, (h_n, h_c) = self.rnn(x, None)
        r_out, h_state = self.rnn(x.view(len(x), 1, -1), h_state)
        # r_out, (h_n, h_c) = self.rnn(x.view(len(x), 1, -1), None)
        x = r_out[:, -1, :]
        x = F.relu(self.fc1(x))
        value = self.state_value(x)
        return value


class PPO:
    def __init__(self, j_env, memory_size=5, batch_size=32, clip_ep=0.2):
        super(PPO, self).__init__()
        self.env = j_env
        self.memory_size = memory_size
        self.batch_size = batch_size  # update batch size
        self.epsilon = clip_ep

        self.action_dim = self.env.action_num
        self.case_name = self.env.case_name
        self.gamma = 0.999  # reward discount
        self.A_LR = 1e-3  # learning rate for actor
        self.C_LR = 3e-3  # learning rate for critic
        self.UPDATE_STEPS = 10  # actor update steps
        self.max_grad_norm = 0.5
        self.training_step = 0

        state_dim = self.env.state_num
        hidden_num = self.env.state_num
        self.actor_net = Actor(state_dim, hidden_num, self.action_dim)
        self.critic_net = Critic(state_dim, hidden_num,)
        self.actor_optimizer = optimizer.Adam(self.actor_net.parameters(), self.A_LR)
        self.critic_net_optimizer = optimizer.Adam(self.critic_net.parameters(), self.C_LR)

        if not os.path.exists('param'):
            os.makedirs('param')
        self.capacity = self.memory_size * self.env.job_num * self.env.machine_num
        self.priorities = np.zeros([self.capacity], dtype=np.float32)
        self.alpha = 0.6  # parameters for priority replay
        self.beta = 0.4
        self.upper_bound = 1
        self.convergence_episode = 5000
        self.beta_increment = (self.upper_bound - self.beta) / self.convergence_episode
        self.train_steps = 0
        self.max_batch_size = 600
        self.PER_NUM = 1

    def select_action(self, state):
        state_tensor = torch.tensor(np.array(state), dtype=torch.float)
        state = state_tensor.unsqueeze(0)
        with torch.no_grad():
            action_prob = self.actor_net(state)
        c = Categorical(action_prob)
        action = c.sample()
        return action.item(), action_prob[:, action.item()].item()

    def get_value(self, state):
        state = torch.tensor(state, dtype=torch.float)
        with torch.no_grad():
            value = self.critic_net(state)
        return value.item()

    def save_params(self, instance_name):
        torch.save(self.actor_net.state_dict(), 'param/' + instance_name + '_actor_net.model')
        torch.save(self.critic_net.state_dict(), 'param/' + instance_name + '_critic_net.model')

    def load_params(self, instance_name):
        self.critic_net.load_state_dict(torch.load('param/' + instance_name + '_critic_net.model'))
        self.actor_net.load_state_dict(torch.load('param/' + instance_name + '_actor_net.model'))

    def learn(self, state, action, d_r, old_prob, w=None):
        if w is not None:
            weights = torch.tensor(w, dtype=torch.float).view(-1, 1)
        else:
            weights = 1
        #  compute the advantage
        d_reward = d_r.view(-1, 1)
        V = self.critic_net(state)
        delta = d_reward - V
        advantage = delta.detach()

        # epoch iteration, PPO core!
        action_prob = self.actor_net(state).gather(1, action)  # new policy
        ratio = (action_prob / old_prob)
        surrogate = ratio * advantage
        clip_loss = torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * advantage
        action_loss = -torch.min(surrogate, clip_loss).mean()

        # update actor network
        self.actor_optimizer.zero_grad()
        action_loss.backward()
        nn.utils.clip_grad_norm_(self.actor_net.parameters(), self.max_grad_norm)
        self.actor_optimizer.step()

        # update critic network
        value_loss = sum((d_reward - V).pow(2) / d_reward.size(0) * weights)
        self.critic_net_optimizer.zero_grad()
        value_loss.backward()
        nn.utils.clip_grad_norm_(self.critic_net.parameters(), self.max_grad_norm)
        self.critic_net_optimizer.step()
        # calculate priorities
        if self.train_steps > self.convergence_episode:
            for w in range(len(advantage)):
                if advantage[w] < 0:
                    advantage[w] = 1e-5
        prob = abs(advantage) ** self.alpha
        return np.array(prob).flatten()

    def update(self, bs, ba, br, bp):
        # get old actor log prob
        old_log_prob = torch.tensor(bp, dtype=torch.float).view(-1, 1)
        state = torch.tensor(np.array(bs), dtype=torch.float)
        action = torch.tensor(ba, dtype=torch.long).view(-1, 1)
        d_reward = torch.tensor(br, dtype=torch.float)

        for k in range(self.UPDATE_STEPS):
            self.train_steps += 1
            # # replay all experience
            for index in BatchSampler(SubsetRandomSampler(range(len(ba))), self.batch_size, False):
                self.priorities[index] = self.learn(state[index], action[index], d_reward[index], old_log_prob[index])
            # priority replay
            for w in range(self.PER_NUM):
                prob1 = self.priorities / np.sum(self.priorities)
                indices = np.random.choice(len(prob1), min(self.max_batch_size, self.batch_size), p=prob1)
                weights = (len(ba) * prob1[indices]) ** (- self.beta)
                if self.beta < self.upper_bound:
                    self.beta += self.beta_increment
                weights = weights / np.max(weights)
                weights = np.array(weights, dtype=np.float32)
                self.learn(state[indices], action[indices], d_reward[indices], old_log_prob[indices], weights)

    def train(self, data_set, save_params=False):
        if not save_params:
            self.load_params(data_set)
        column = ["episode", "make_span", "reward", 'min_make_span']
        results = pd.DataFrame(columns=column, dtype=float)
        index = 0
        converged = 0
        min_make_span = 100000
        converged_value = []
        t0 = time.time()
        for i_epoch in range(4000):
            if time.time() - t0 >= 3600:
                break
            bs, ba, br, bp = [], [], [], []
            for m in range(self.memory_size):  # memory size is the number of complete episode
                buffer_s, buffer_a, buffer_r, buffer_p = [], [], [], []
                state = self.env.reset()
                episode_reward = 0
                while True:
                    action, action_prob = self.select_action(state)
                    next_state, reward, done = self.env.step(action)
                    buffer_s.append(state)
                    buffer_a.append(action)
                    buffer_r.append(reward)
                    buffer_p.append(action_prob)

                    state = next_state
                    episode_reward += reward
                    if done:
                        v_s_ = 0
                        discounted_r = []
                        for r in buffer_r[::-1]:
                            v_s_ = r + self.gamma * v_s_
                            discounted_r.append(v_s_)
                        discounted_r.reverse()

                        bs[len(bs):len(bs)] = buffer_s
                        ba[len(ba):len(ba)] = buffer_a
                        br[len(br):len(br)] = discounted_r
                        bp[len(bp):len(bp)] = buffer_p

                        index = i_epoch * self.memory_size + m
                        if min_make_span > self.env.current_time:
                            min_make_span = self.env.current_time
                        # Episode: make_span: Episode reward: no-op count
                        print('{}    {}    {:.2f}  {}'.format(i_epoch, self.env.current_time,
                                                              episode_reward, min_make_span))
                        results.loc[index] = [i_epoch, self.env.current_time, episode_reward, min_make_span]
                        converged_value.append(self.env.current_time)
                        if len(converged_value) >= 31:
                            converged_value.pop(0)
                        break
            self.update(bs, ba, br, bp)
            converged = index
            if min(converged_value) == max(converged_value) and len(converged_value) >= 30:
                converged = index
                break
        if not os.path.exists('results'):
            os.makedirs('results')
        results.to_csv("results/" + str(self.env.case_name) + "_" + data_set + ".csv")
        if save_params:
            self.save_params(data_set)
        return min(converged_value), converged, time.time() - t0, self.env.no_op_cnt

    def test(self, data_set):
        self.load_params(data_set)
        converged_value = []
        for ci in range(30):
            state = self.env.reset()
            while True:
                action, _ = self.select_action(state)
                next_state, reward, done = self.env.step(action)
                state = next_state
                if done:
                    break
            # print(self.env.current_time)
            converged_value.append(env.current_time)
        return min(converged_value), 0, 0, 0


if __name__ == '__main__':
    # training policy
    parameters = "rnn-1-0999"
    path = "../data_set_sizes/"
    print(parameters)
    param = [parameters, "converge_cnt", "total_time", "min make span"]
    simple_results = pd.DataFrame(columns=param, dtype=int)
    for cnt in range(1):
        parameters += str(cnt)
        for file_name in os.listdir(path):
            print(file_name + "========================")
            title = file_name.split('.')[0]
            name = file_name.split('_')[0]
            env = JobEnv(title, path)
            scale = env.job_num * env.machine_num
            model = PPO(env, memory_size=3, batch_size=1 * scale, clip_ep=0.2)
            simple_results.loc[title] = model.train(title, save_params=True)
            # simple_results.loc[title] = model.train(name, save_params=False)
            # simple_results.loc[title] = model.test(name)
            # simple_results.loc[title] = model.test("ta61")
        simple_results.to_csv(parameters + "_result.csv")
