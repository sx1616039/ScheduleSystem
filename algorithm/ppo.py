import os
import time
import numpy as np
import pandas as pd
import torch
from math import floor, ceil
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optimizer
from torch.distributions import Categorical
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler


def SpatialPyramidPooling2d(input_x, level, pool_type='max_pool'):
    N, C, H, W = input_x.size()
    for i in range(level):
        level = i + 1
        kernel_size = (ceil(H / level), ceil(W / level))
        stride = (ceil(H / level), ceil(W / level))
        padding = (floor((kernel_size[0] * level - H + 1) / 2), floor((kernel_size[1] * level - W + 1) / 2))

        if pool_type == 'max_pool':
            tensor = (F.max_pool2d(input_x, kernel_size=kernel_size, stride=stride, padding=padding)).view(N, -1)
        else:
            tensor = (F.avg_pool2d(input_x, kernel_size=kernel_size, stride=stride, padding=padding)).view(N, -1)

        if i == 0:
            res = tensor
        else:
            res = torch.cat((res, tensor), 1)
    return res


def _cal_num_grids(level):
    count = 0
    for i in range(level):
        count += (i + 1) * (i + 1)
    return count


class SPP_Actor(nn.Module):
    def __init__(self, config, out_num=12):
        super(SPP_Actor, self).__init__()
        input_channel = config.spp_actor_input_channel
        out_channel = config.spp_actor_output_channel
        kernel = config.spp_actor_kernel_size
        padding = config.spp_actor_padding
        self.num_level = config.spp_actor_level
        self.num_grid = _cal_num_grids(self.num_level)
        self.feature1 = nn.Sequential(
            nn.Conv2d(input_channel, out_channel, kernel_size=(kernel, kernel), padding=padding), nn.ReLU())

        self.linear1 = nn.Linear(out_channel * self.num_grid, out_num)

    def forward(self, x):
        x = self.feature1(x)
        x = SpatialPyramidPooling2d(x, self.num_level)
        action_prob = F.softmax(self.linear1(x), dim=1)
        return action_prob


class SPP_Critic(nn.Module):
    def __init__(self, config, out_num=1):
        super(SPP_Critic, self).__init__()
        input_channel = config.spp_critic_input_channel
        out_channel = config.spp_critic_output_channel
        kernel = config.spp_critic_kernel_size
        padding = config.spp_critic_padding
        self.num_level = config.spp_critic_level
        self.num_grid = _cal_num_grids(self.num_level)
        self.feature1 = nn.Sequential(
            nn.Conv2d(input_channel, out_channel, kernel_size=(kernel, kernel), padding=padding), nn.ReLU())
        self.linear1 = nn.Linear(out_channel * self.num_grid, out_num)

    def forward(self, x):
        x = self.feature1(x)
        x = SpatialPyramidPooling2d(x, self.num_level)
        state_value = self.linear1(x)
        return state_value


class MLP_Actor(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim, hidden_layers=1):
        super(MLP_Actor, self).__init__()
        self.input_layer = nn.Linear(input_dim, hidden_dim[0])
        self.linears = nn.ModuleList()
        for i in range(hidden_layers - 1):
            self.linears.append(nn.Linear(hidden_dim[i], hidden_dim[i + 1]))
        self.output_layer = nn.Linear(hidden_dim[hidden_layers - 1], output_dim)

    def forward(self, x):
        x = F.relu(self.input_layer(x))
        for layer in self.linears:
            x = F.relu(layer(x))
        action_prob = F.softmax(self.output_layer(x), dim=1)
        return action_prob


class MLP_Critic(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim=1, hidden_layers=1):
        super(MLP_Critic, self).__init__()
        self.input_layer = nn.Linear(input_dim, hidden_dim[0])
        self.linears = nn.ModuleList()
        for i in range(hidden_layers - 1):
            self.linears.append(nn.Linear(hidden_dim[i], hidden_dim[i + 1]))
        self.output_layer = nn.Linear(hidden_dim[hidden_layers - 1], output_dim)

    def forward(self, x):
        x = F.relu(self.input_layer(x))
        for layer in self.linears:
            x = F.relu(layer(x))
        value = self.output_layer(x)
        return value


class CNN_Actor(nn.Module):
    def __init__(self, height, width, num_output, input_channel=3, out_channel=8):
        super(CNN_Actor, self).__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(input_channel, 16, kernel_size=(5, 5), padding=2), nn.ReLU(),
                                   nn.MaxPool2d(2))
        self.conv2 = nn.Sequential(nn.Conv2d(16, out_channel, kernel_size=(5, 5), padding=2), nn.ReLU(),
                                   nn.MaxPool2d(2))
        self.action_head = nn.Linear(out_channel*int(height/4)*int(width/4), num_output)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        action_prob = F.softmax(self.action_head(x), dim=1)
        return action_prob


class CNN_Critic(nn.Module):
    def __init__(self, height, width, input_channel=3, num_output=1, out_channel=8):
        super(CNN_Critic, self).__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(input_channel, 16, kernel_size=(5, 5), padding=2), nn.ReLU(),
                                   nn.MaxPool2d(2))
        self.conv2 = nn.Sequential(nn.Conv2d(16, out_channel, kernel_size=(5, 5), padding=2), nn.ReLU(),
                                   nn.MaxPool2d(2))
        self.state_value = nn.Linear(out_channel*int(height/4)*int(width/4), num_output)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        value = self.state_value(x)
        return value


class Agent:
    def __init__(self, env, config):
        super(Agent, self).__init__()
        self.env = env
        self.case_name = self.env.case_name
        self.memory_size = config.trajectory_num
        self.batch_size = config.batch_size  # update batch size
        self.max_episodes = config.max_episodes
        self.max_training_time = config.max_training_time
        self.epsilon = config.ppo_epsilon
        self.gamma = config.ppo_gamma  # reward discount
        self.policy_type = config.policy
        self.UPDATE_STEPS = config.ppo_updates  # actor update steps
        if self.policy_type == 0:  # MLP
            self.A_LR = config.mlp_actor_lr  # learning rate for actor
            self.C_LR = config.mlp_critic_lr  # learning rate for critic

            input_dim = (self.env.job_num+self.env.machine_num)*2
            output_dim = self.env.action_num
            hidden_dim = [config.mlp_actor_hidden_dim]
            hidden_layers = config.mlp_critic_hidden_layers
            self.actor_net = MLP_Actor(input_dim, output_dim, hidden_dim, hidden_layers)
            self.critic_net = MLP_Critic(input_dim, hidden_dim)
        elif self.policy_type == 1:
            self.A_LR = config.spp_actor_lr  # learning rate for actor
            self.C_LR = config.spp_critic_lr  # learning rate for critic
            self.actor_net = SPP_Actor(config)
            self.critic_net = SPP_Critic(config)

        self.actor_optimizer = optimizer.Adam(self.actor_net.parameters(), self.A_LR)
        self.critic_net_optimizer = optimizer.Adam(self.critic_net.parameters(), self.C_LR)
        self.max_grad_norm = 0.5
        self.train_steps = 0

        self.capacity = self.memory_size * self.env.job_num * self.env.machine_num
        self.priorities = np.zeros([self.capacity], dtype=np.float32)
        self.alpha = config.alpha
        self.beta = config.beta
        self.upper_bound = 1
        self.convergence_episode = config.conv_steps
        self.beta_increment = (self.upper_bound - self.beta) / self.convergence_episode
        self.max_batch_size = int(self.batch_size/2)
        self.PER_NUM = config.replay_num
        self.model_path = config.model_path

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
        torch.save(self.actor_net.state_dict(), self.model_path + instance_name + '_actor_net.model')
        torch.save(self.critic_net.state_dict(), self.model_path + instance_name + '_critic_net.model')

    def load_params(self, instance_name):
        self.critic_net.load_state_dict(torch.load(self.model_path + instance_name + '_critic_net.model'))
        self.actor_net.load_state_dict(torch.load(self.model_path + instance_name + '_actor_net.model'))

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

    def test(self, model_name):
        self.load_params(model_name)
        value = []
        t0 = time.time()
        for m in range(1):
            state = self.env.reset()
            while True:
                action, _ = self.select_action(state)
                next_state, reward, done = self.env.step(action)
                state = next_state
                if done:
                    break
            value.append(self.env.current_time)
        return min(value), 1, time.time() - t0

    def train(self, data_set, is_rescheduling=False):
        if is_rescheduling:
            self.load_params(data_set)
        column = ["episode", "make_span", "reward", 'min make span']
        results = pd.DataFrame(columns=column, dtype=float)
        index = 0
        converged = 0
        min_make_span = 100000
        converged_value = []
        t0 = time.time()
        for i_epoch in range(self.max_episodes):
            if time.time() - t0 >= self.max_training_time:
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
                        if min_make_span > self.env.current_time:
                            min_make_span = self.env.current_time
                        # Episode: make_span: Episode reward
                        print('{}    {}    {:.2f} {}'.format(i_epoch, self.env.current_time, episode_reward,
                                                             min_make_span))
                        index = i_epoch * self.memory_size + m
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

        results.to_csv(self.model_path + str(self.env.case_name) + "_" + data_set + ".csv")
        if not is_rescheduling:
            self.save_params(data_set)
        return min(converged_value), converged, time.time() - t0, min_make_span
