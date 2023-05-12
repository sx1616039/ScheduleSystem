import argparse
import os

import pandas as pd
import torch
import random
import numpy as np

from algorithm.env_jobshop import JobshopEnv
from algorithm.ppo import Agent


def main(input_parameters=''):
    print('hello')
    fix_seed = 2023
    random.seed(fix_seed)
    torch.manual_seed(fix_seed)
    np.random.seed(fix_seed)

    parser = argparse.ArgumentParser(description='DRL scheduling method for job shop scheduling problems')
    parser.add_argument('--policy', type=int, default=0, help='policy networks, 0: MLP, 1: SPP')
    parser.add_argument('--model_path', type=str, default='../models', help='model path')
    # environment config
    parser.add_argument('--order_path', type=str, default='../orders',
                        help='the path of orders/input data')
    parser.add_argument('--snapshot_percent', type=float, default=0, help='make snapshot based on completion rate')
    parser.add_argument('--no_op', type=bool, default=False, help='whether consider no op')
    parser.add_argument('--state', type=int, default=0,
                        help='state representation method, 0: variable, 1: matrix, 2:image')
    parser.add_argument('--action', type=int, default=0,
                        help='action space, 0:6-PDR, 1:12-PDR, 2:operation')
    parser.add_argument('--reward', type=int, default=0,
                        help='reward function, 0: area, 1: machine idle time, 2: real and imaginary machine idle time')
    # training config
    parser.add_argument('--batch_size', type=int, default=256,
                        help='batch_size: the number of trajectories')
    parser.add_argument('--max_episodes', type=int, default=4000, help='maximum training episodes')
    parser.add_argument('--max_training_time', type=int, default=3600, 
                        help='training time use second unit')
    parser.add_argument('--trajectory_num', type=int, default=3, help='the capacity of training memory')
    parser.add_argument('--rescheduling_mode', type=int, default=2,
                        help='rescheduling_mode: 0: trained, 1: reused, 2: retrained')
    # PER parameters
    parser.add_argument('--alpha', type=float, default=0.6, help='exponent of TD-error for proportional priority')
    parser.add_argument('--beta', type=float, default=0.4, help='the initial exponent for important weights ')
    parser.add_argument('--use_IS', type=bool, default=False, help='whether use the IS')
    parser.add_argument('--use_PER', type=bool, default=False, help='whether use the PER')
    parser.add_argument('--conv_steps', type=int, default=5000, help='the convergence steps for PER')
    parser.add_argument('--replay_num', type=int, default=1, help='the number of performing replay')
    parser.add_argument('--sample_type', type=int, default=0,
                        help='the samples are divided into 3 categories: positive, negative and all')

    # MLP policy network parameters
    parser.add_argument('--mlp_actor_hidden_layers', type=int, default=1, help='mlp_actor__hidden_layers')
    parser.add_argument('--mlp_actor_activation', type=int, default=0,
                        help='0:relu, 1:leaky relu, 2:sigmoid, 3:tanh')
    parser.add_argument('--mlp_actor_hidden_dim', type=int, default=100, help='the dimension of hidden layers')
    parser.add_argument('--mlp_actor_lr', type=float, default=1e-3, help='learning rate')
    parser.add_argument('--mlp_critic_hidden_layers', type=int, default=1, help='mlp_critic_hidden_layers')
    parser.add_argument('--mlp_critic_activation', type=int, default=0,
                        help='0:relu, 1:leaky relu, 2:sigmoid, 3:tanh')
    parser.add_argument('--mlp_critic_hidden_dim', type=int, default=100, help='the dimension of hidden layers')
    parser.add_argument('--mlp_critic_lr', type=float, default=3e-3, help='learning rate')

    # SPP policy network parameters
    parser.add_argument('--spp_actor_activation', type=int, default=0, help='0:relu, 1:leaky relu, 2:sigmoid, 3:tanh')
    parser.add_argument('--spp_actor_full_connect_layers', type=int, default=1, help='the number of full connect layers')
    parser.add_argument('--spp_actor_full_connect_dim', type=int, default=100, help='full connect layer dimension')
    parser.add_argument('--spp_actor_input_channel', type=int, default=3, help='input image channels')
    parser.add_argument('--spp_actor_output_channel', type=int, default=6, help='output image channels')
    parser.add_argument('--spp_actor_kernel_size', type=int, default=5, help='the dimension of kernel size')
    parser.add_argument('--spp_actor_lr', type=float, default=1e-3, help='learning rate of SPP actor')
    parser.add_argument('--spp_actor_padding', type=int, default=2, help='padding')
    parser.add_argument('--spp_actor_level', type=int, default=4, help='level of SPP')
    parser.add_argument('--spp_actor_pooling_type', type=int, default=0,
                        help='0:max pooling, 1:average pooling')
    parser.add_argument('--spp_critic_activation', type=int, default=0, help='0:relu, 1:leaky relu, 2:sigmoid, 3:tanh')
    parser.add_argument('--spp_critic_full_connect_layers', type=int, default=1,
                        help='the number of full connect layers')
    parser.add_argument('--spp_critic_full_connect_dim', type=int, default=100, help='full connect layer dimension')
    parser.add_argument('--spp_critic_input_channel', type=int, default=3, help='input image channels')
    parser.add_argument('--spp_critic_output_channel', type=int, default=6, help='output image channels')
    parser.add_argument('--spp_critic_kernel_size', type=int, default=5, help='the dimension of kernel size')
    parser.add_argument('--spp_critic_lr', type=float, default=1e-3, help='learning rate of SPP actor')
    parser.add_argument('--spp_critic_padding', type=int, default=2, help='padding')
    parser.add_argument('--spp_critic_level', type=int, default=4, help='level of SPP')
    parser.add_argument('--spp_critic_pooling_type', type=int, default=0,
                        help='0:max pooling, 1:average pooling')

    # ppo parameters
    parser.add_argument('--ppo_epsilon', type=float, default=0.2, help='clipped epsilon')
    parser.add_argument('--ppo_gamma', type=float, default=0.999, help='discount reward rate')
    parser.add_argument('--ppo_optimizer', type=int, default=0, help='0:Adam, 1:SGD')
    parser.add_argument('--ppo_updates', type=int, default=32, help='the number of updates for each collected data')

    args = parser.parse_args(input_parameters.split())
    print(args)
    path = args.order_path
    print(path)
    if os.path.isdir(path):
        parameters = '{}_{}_{}_{}'.format(args.policy, args.batch_size, args.trajectory_num, args.ppo_epsilon)
        print(parameters)
        param = ['instance', "converge_cnt", "total_time", "min make span"]
        simple_results = pd.DataFrame(columns=param, dtype=int)
        for file_name in os.listdir(path):
            print(file_name + "========================")
            file_path = os.path.join(path, file_name)
            title = file_name.split('.')[0]
            env = JobshopEnv(file_path, args)
            model = Agent(env, args)
            name = file_name.split('_')[0]
            if args.rescheduling_mode == 0:
                simple_results.loc[title] = model.test(name)
            elif args.rescheduling_mode == 1:
                simple_results.loc[title] = model.train(name, is_rescheduling=True)
            elif args.rescheduling_mode == 2:
                simple_results.loc[title] = model.train(title, is_rescheduling=False)
        simple_results.to_csv(path + parameters + "_result.csv")
    else:
        env = JobshopEnv(path, args)
        model = Agent(env, args)
        title = os.path.basename(path)
        name = title.split('_')[0]
        if args.rescheduling_mode == 0:
            model.test(name)
        elif args.rescheduling_mode == 1:
            model.train(name, is_rescheduling=True)
        elif args.rescheduling_mode == 2:
            model.train(title, is_rescheduling=False)


if __name__ == "__main__":
    main()
