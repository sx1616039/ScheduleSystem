# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os
import wx.xrc
import wx.lib.newevent
import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element


class EditPanel(wx.Panel):

    def __init__(self, parent, model_path, page_id):
        wx.Panel.__init__(self, parent, page_id, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        dir_name = os.path.basename(model_path)
        description_file = dir_name + '_description.xml'
        self.path = os.path.join(model_path, description_file)
        self.tree = et.parse(self.path)
        self.root = self.tree.getroot()
        base = self.root.find('base')
        state = base.get('state')
        action = base.get('action')
        reward = base.get('reward')
        policy = base.get('policy')

        ''' 第二行设置参数面板 '''
        parameter_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 状态表示
        self.representation_method = ['状态变量表示', '可行解矩阵表示', '图像表示']
        label_representation_method = wx.StaticText(parameter_panel, wx.ID_ANY, u"状态特征表示方法:",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.combobox_representation = wx.ComboBox(parameter_panel, -1, size=wx.Size(80, -1),
                                                   choices=self.representation_method)
        self.combobox_representation.SetSelection(int(state))
        # 动作空间
        self.action_space = ['PDR', '成对PDR', '工序']
        label_action_space = wx.StaticText(parameter_panel, wx.ID_ANY, u"动作空间:",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.combobox_action_space = wx.ComboBox(parameter_panel, -1, size=wx.Size(80, -1), choices=self.action_space)
        self.combobox_action_space.SetSelection(int(action))
        # 回报函数
        self.reward = ['调度面积', '机器空闲时间', '虚实机器空闲时间']
        label_reward = wx.StaticText(parameter_panel, wx.ID_ANY, u"奖励函数:",
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.combobox_reward = wx.ComboBox(parameter_panel, -1, size=wx.Size(80, -1), choices=self.reward)
        self.combobox_reward.SetSelection(int(reward))

        # 调度策略网络
        self.policy_networks = ['MLP', 'SPP']
        label_policy_networks = wx.StaticText(parameter_panel, wx.ID_ANY, u"调度策略网络:", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.combobox_policy_networks = wx.ComboBox(parameter_panel, -1, size=wx.Size(80, -1),
                                                    choices=self.policy_networks)
        self.combobox_policy_networks.SetSelection(int(policy))
        self.combobox_policy_networks.Bind(wx.EVT_COMBOBOX, self.on_select_combobox_policy_networks)
        ''' 保存模型按钮 '''
        btn_save = wx.Button(parameter_panel, wx.ID_ANY, u"保存模型", wx.DefaultPosition, wx.Size(100, 26), 0)
        btn_save.SetBitmap(wx.Bitmap('icon/run.ico'))
        btn_save.Bind(wx.EVT_BUTTON, self.on_button_save)
        # 设置参数布局
        parameter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        parameter_sizer.Add(label_representation_method, 1, wx.ALL, 7)
        parameter_sizer.Add(self.combobox_representation, 5, wx.ALL, 5)
        parameter_sizer.Add(label_action_space, 0, wx.ALL, 7)
        parameter_sizer.Add(self.combobox_action_space, 5, wx.ALL, 5)
        parameter_sizer.Add(label_reward, 0, wx.ALL, 7)
        parameter_sizer.Add(self.combobox_reward, 5, wx.ALL, 5)
        parameter_sizer.Add(label_policy_networks, 0, wx.ALL, 7)
        parameter_sizer.Add(self.combobox_policy_networks, 5, wx.ALL, 5)
        parameter_sizer.Add(btn_save, 5, wx.ALL, 5)

        parameter_panel.SetSizer(parameter_sizer)

        # 深度神经网络参数
        self.networks_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        if policy == '0':
            self.show_MLP()
        else:
            self.show_SPP()

        # 强化学习模型参数
        base = self.root.find('ppo')
        optimizer = base.get('optimizer')
        gamma = base.get('gamma')
        epsilon = base.get('epsilon')
        updates = base.get('updates')
        self.RL_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_ppo = wx.StaticText(self.RL_panel, wx.ID_ANY, u"PPO模型参数:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)

        label_gamma = wx.StaticText(self.RL_panel, wx.ID_ANY, u"回报折扣率(gamma):", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.text_gamma = wx.TextCtrl(self.RL_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                      style=wx.TE_LEFT)
        self.text_gamma.AppendText(gamma)
        # 优化求解器
        self.optimizer = ['Adam', 'SGD']
        label_optimizer = wx.StaticText(self.RL_panel, wx.ID_ANY, u"优化器:",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.combobox_optimizer = wx.ComboBox(self.RL_panel, -1, size=wx.Size(80, -1), choices=self.optimizer)
        self.combobox_optimizer.SetSelection(int(optimizer))

        label_epsilon = wx.StaticText(self.RL_panel, wx.ID_ANY, u"裁剪参数(epsilon):", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.text_epsilon = wx.TextCtrl(self.RL_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                        style=wx.TE_LEFT)
        self.text_epsilon.AppendText(epsilon)
        label_updates = wx.StaticText(self.RL_panel, wx.ID_ANY, u"网络更新次数:", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.text_updates = wx.TextCtrl(self.RL_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                        style=wx.TE_LEFT)
        self.text_updates.AppendText(updates)

        ppo_box2 = wx.BoxSizer(wx.HORIZONTAL)
        ppo_box2.Add((30, 20))
        ppo_box2.Add(label_optimizer, 0, wx.ALL | wx.EXPAND, 7)
        ppo_box2.Add(self.combobox_optimizer, 1, wx.ALL | wx.EXPAND, 5)
        ppo_box2.Add(label_gamma, 0, wx.ALL | wx.EXPAND, 7)
        ppo_box2.Add(self.text_gamma, 5, wx.ALL | wx.EXPAND, 5)
        ppo_box2.Add(label_epsilon, 0, wx.ALL | wx.EXPAND, 7)
        ppo_box2.Add(self.text_epsilon, 5, wx.ALL | wx.EXPAND, 5)
        ppo_box2.Add(label_updates, 0, wx.ALL | wx.EXPAND, 7)
        ppo_box2.Add(self.text_updates, 5, wx.ALL | wx.EXPAND, 5)

        RL_box = wx.BoxSizer(wx.VERTICAL)
        RL_box.Add(label_ppo, 0, wx.ALL, 7)
        RL_box.Add(ppo_box2, 0, wx.ALL, 0)
        self.RL_panel.SetSizer(RL_box)

        # main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(parameter_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.networks_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.RL_panel, 0, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def on_select_combobox_policy_networks(self, event):
        pos = self.combobox_policy_networks.GetSelection()
        if pos == 0:
            self.show_MLP()
        else:
            self.show_SPP()

        self.Layout()

    def on_button_save(self, event):
        state = self.combobox_representation.GetSelection()
        action = self.combobox_action_space.GetSelection()
        reward = self.combobox_reward.GetSelection()
        policy = self.combobox_policy_networks.GetSelection()
        old_base = self.root.find("base")
        if not old_base is None:
            self.root.remove(old_base)
        base = Element("base")
        base.set('state', str(state))
        base.set('action', str(action))
        base.set('reward', str(reward))
        base.set('policy', str(policy))

        if policy == 0:
            layers = self.text_hidden_layers.GetLineText(0)
            dim = self.text_hidden_layer_dim.GetLineText(0)
            lr = self.text_actor_lr.GetLineText(0)
            activation = self.combobox_actor_af.GetSelection()
            Actor_MLP = Element("Actor_MLP",
                                {'layers': str(layers), 'dim': str(dim), 'lr': str(lr), 'activation': str(activation)})
            old = self.root.find("Actor_MLP")
            if not old is None:
                self.root.remove(old)
            self.root.append(Actor_MLP)
            critic_layers = self.text_critic_hidden_layers.GetLineText(0)
            critic_dim = self.text_critic_hidden_layer_dim.GetLineText(0)
            critic_lr = self.text_critic_lr.GetLineText(0)
            critic_activation = self.combobox_critic_af.GetSelection()
            critic_MLP = Element("Critic_MLP",
                                 {'layers': str(critic_layers), 'dim': str(critic_dim), 'lr': str(critic_lr),
                                  'activation': str(critic_activation)})
            old = self.root.find("Critic_MLP")
            if not old is None:
                self.root.remove(old)
            self.root.append(critic_MLP)
        else:
            kernel_size = self.combobox_kernel_size.GetSelection()
            input_channel = self.text_input_channel.GetLineText(0)
            output_channel = self.text_output_channel.GetLineText(0)
            padding = self.text_padding.GetLineText(0)
            spp_level = self.text_spp_level.GetLineText(0)
            pooling_type = self.combobox_pooling_type.GetSelection()
            full_connect_layers = self.text_full_connect_num.GetLineText(0)
            full_connect_dim = self.text_full_connect_dim.GetLineText(0)
            lr = self.text_actor_lr.GetLineText(0)
            activation = self.combobox_actor_af.GetSelection()
            spp_actor = Element("Actor_SPP", {'kernel_size': str(kernel_size), 'input_channel': str(input_channel),
                                              'output_channel': str(output_channel), 'padding': str(padding),
                                              'spp_level': str(spp_level), 'pooling_type': str(pooling_type),
                                              'full_connect_layers': str(full_connect_layers),
                                              'full_connect_dim': str(full_connect_dim), 'lr': str(lr),
                                              'activation': str(activation)})
            kernel_size = self.combobox_critic_kernel_size.GetSelection()
            input_channel = self.text_critic_input_channel.GetLineText(0)
            output_channel = self.text_critic_output_channel.GetLineText(0)
            padding = self.text_critic_padding.GetLineText(0)
            spp_level = self.text_critic_spp_level.GetLineText(0)
            pooling_type = self.combobox_critic_pooling_type.GetSelection()
            full_connect_layers = self.text_critic_full_connect_num.GetLineText(0)
            full_connect_dim = self.text_critic_full_connect_dim.GetLineText(0)
            lr = self.text_critic_lr.GetLineText(0)
            activation = self.combobox_critic_af.GetSelection()
            spp_critic = Element("Critic_SPP", {'kernel_size': str(kernel_size), 'input_channel': str(input_channel),
                                                'output_channel': str(output_channel), 'padding': str(padding),
                                                'spp_level': str(spp_level), 'pooling_type': str(pooling_type),
                                                'full_connect_layers': str(full_connect_layers),
                                                'full_connect_dim': str(full_connect_dim), 'lr': str(lr),
                                                'activation': str(activation)})
            old = self.root.find("Actor_SPP")
            if not old is None:
                self.root.remove(old)
            self.root.append(spp_actor)
            old = self.root.find("Critic_SPP")
            if not old is None:
                self.root.remove(old)
            self.root.append(spp_critic)

        optimizer = self.combobox_optimizer.GetSelection()
        gamma = self.text_gamma.GetLineText(0)
        epsilon = self.text_epsilon.GetLineText(0)
        updates = self.text_updates.GetLineText(0)
        ppo = Element("ppo", {'optimizer': str(optimizer), 'gamma': str(gamma), 'epsilon': str(epsilon),
                              'updates': str(updates)})
        old = self.root.find("ppo")
        if not old is None:
            self.root.remove(old)
        self.root.append(base)
        self.root.append(ppo)
        self.tree.write(self.path)

    def show_MLP(self):
        MLP_Actor = self.root.find('Actor_MLP')
        layers = MLP_Actor.get('layers')
        dim = MLP_Actor.get('dim')
        lr = MLP_Actor.get('lr')
        activation = MLP_Actor.get('activation')

        self.networks_panel.DestroyChildren()
        label_networks = wx.StaticText(self.networks_panel, wx.ID_ANY, u"Actor网络参数:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        label_hidden_layers = wx.StaticText(self.networks_panel, wx.ID_ANY, u"隐藏层数量:", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.text_hidden_layers = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                              style=wx.TE_LEFT)
        self.text_hidden_layers.AppendText(layers)
        label_hidden_layer_dim = wx.StaticText(self.networks_panel, wx.ID_ANY, u"隐藏层维度:", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.text_hidden_layer_dim = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                 style=wx.TE_LEFT)
        self.text_hidden_layer_dim.AppendText(dim)
        label_actor_lr = wx.StaticText(self.networks_panel, wx.ID_ANY, u"学习率:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.text_actor_lr = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                         style=wx.TE_LEFT)
        self.text_actor_lr.AppendText(lr)
        # activation function
        self.activation_functions = ['Relu', 'LeakyRelu', 'Softmax', 'Tanh']
        label_actor_af = wx.StaticText(self.networks_panel, wx.ID_ANY, u"激活函数:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.combobox_actor_af = wx.ComboBox(self.networks_panel, -1, size=wx.Size(80, -1),
                                             choices=self.activation_functions)
        self.combobox_actor_af.SetSelection(int(activation))

        actor_box = wx.BoxSizer(wx.HORIZONTAL)
        actor_box.Add((30, 20))
        actor_box.Add(label_hidden_layers, 1, wx.ALL | wx.EXPAND, 7)
        actor_box.Add(self.text_hidden_layers, 5, wx.ALL | wx.EXPAND, 5)
        actor_box.Add(label_hidden_layer_dim, 0, wx.ALL | wx.EXPAND, 7)
        actor_box.Add(self.text_hidden_layer_dim, 5, wx.ALL | wx.EXPAND, 5)
        actor_box.Add(label_actor_lr, 0, wx.ALL | wx.EXPAND, 7)
        actor_box.Add(self.text_actor_lr, 5, wx.ALL | wx.EXPAND, 5)
        actor_box.Add(label_actor_af, 0, wx.ALL | wx.EXPAND, 7)
        actor_box.Add(self.combobox_actor_af, 5, wx.ALL | wx.EXPAND, 5)

        MLP_Critc = self.root.find('Critic_MLP')
        layers = MLP_Critc.get('layers')
        dim = MLP_Critc.get('dim')
        lr = MLP_Critc.get('lr')
        activation = MLP_Critc.get('activation')
        label_critic = wx.StaticText(self.networks_panel, wx.ID_ANY, u"Critic网络参数:", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        label_critic_hidden_layers = wx.StaticText(self.networks_panel, wx.ID_ANY, u"隐藏层数量:", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.text_critic_hidden_layers = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                     style=wx.TE_LEFT)
        self.text_critic_hidden_layers.AppendText(layers)
        label_critic_hidden_layer_dim = wx.StaticText(self.networks_panel, wx.ID_ANY, u"隐藏层维度:", wx.DefaultPosition,
                                                      wx.DefaultSize, 0)
        self.text_critic_hidden_layer_dim = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                        style=wx.TE_LEFT)
        self.text_critic_hidden_layer_dim.AppendText(dim)

        label_critic_lr = wx.StaticText(self.networks_panel, wx.ID_ANY, u"学习率:", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.text_critic_lr = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                          style=wx.TE_LEFT)
        self.text_critic_lr.AppendText(lr)
        # activation function
        label_critic_af = wx.StaticText(self.networks_panel, wx.ID_ANY, u"激活函数:", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.combobox_critic_af = wx.ComboBox(self.networks_panel, -1, size=wx.Size(80, -1),
                                              choices=self.activation_functions)
        self.combobox_critic_af.SetSelection(int(activation))

        critic_box = wx.BoxSizer(wx.HORIZONTAL)
        critic_box.Add((30, 20))
        critic_box.Add(label_critic_hidden_layers, 1, wx.ALL | wx.EXPAND, 7)
        critic_box.Add(self.text_critic_hidden_layers, 5, wx.ALL | wx.EXPAND, 5)
        critic_box.Add(label_critic_hidden_layer_dim, 0, wx.ALL | wx.EXPAND, 7)
        critic_box.Add(self.text_critic_hidden_layer_dim, 5, wx.ALL | wx.EXPAND, 5)
        critic_box.Add(label_critic_lr, 0, wx.ALL | wx.EXPAND, 7)
        critic_box.Add(self.text_critic_lr, 5, wx.ALL | wx.EXPAND, 5)
        critic_box.Add(label_critic_af, 0, wx.ALL | wx.EXPAND, 7)
        critic_box.Add(self.combobox_critic_af, 5, wx.ALL | wx.EXPAND, 5)

        network_box = wx.BoxSizer(wx.VERTICAL)
        network_box.Add(label_networks, 0, wx.ALL, 5)
        network_box.Add(actor_box, 0, wx.ALL, 0)
        network_box.Add(label_critic, 0, wx.ALL, 5)
        network_box.Add(critic_box, 0, wx.ALL, 0)
        self.networks_panel.SetSizer(network_box)
        self.networks_panel.Layout()

    def show_SPP(self):
        self.networks_panel.DestroyChildren()
        label_actor = wx.StaticText(self.networks_panel, wx.ID_ANY, u"Actor网络参数:", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        label_conv = wx.StaticText(self.networks_panel, wx.ID_ANY, u"卷积层网络参数:", wx.DefaultPosition,
                                   wx.DefaultSize, 0)
        label_kernel_size = wx.StaticText(self.networks_panel, wx.ID_ANY, u"卷积核大小:", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.kernel_sizes = ['5x5', '3x3', '1x1']
        self.combobox_kernel_size = wx.ComboBox(self.networks_panel, -1, size=wx.Size(80, -1),
                                                choices=self.kernel_sizes)
        self.combobox_kernel_size.SetSelection(0)
        # 输入通道数
        label_input_channel = wx.StaticText(self.networks_panel, wx.ID_ANY, u"输入通道数:", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.text_input_channel = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                              style=wx.TE_LEFT)
        self.text_input_channel.AppendText('3')

        label_output_channel = wx.StaticText(self.networks_panel, wx.ID_ANY, u"输出通道数:", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.text_output_channel = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                               style=wx.TE_LEFT)
        self.text_output_channel.AppendText('16')

        label_padding = wx.StaticText(self.networks_panel, wx.ID_ANY, u"填充数(padding):", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.text_padding = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                        style=wx.TE_LEFT)
        self.text_padding.AppendText('2')

        conv_box = wx.BoxSizer(wx.HORIZONTAL)
        conv_box.Add((30, 20))
        conv_box.Add(label_conv, 1, wx.ALL | wx.EXPAND, 7)
        conv_box.Add(label_kernel_size, 0, wx.ALL | wx.EXPAND, 7)
        conv_box.Add(self.combobox_kernel_size, 1, wx.ALL | wx.EXPAND, 5)
        conv_box.Add(label_input_channel, 0, wx.ALL | wx.EXPAND, 7)
        conv_box.Add(self.text_input_channel, 5, wx.ALL | wx.EXPAND, 5)
        conv_box.Add(label_output_channel, 0, wx.ALL | wx.EXPAND, 7)
        conv_box.Add(self.text_output_channel, 5, wx.ALL | wx.EXPAND, 5)
        conv_box.Add(label_padding, 0, wx.ALL | wx.EXPAND, 7)
        conv_box.Add(self.text_padding, 5, wx.ALL | wx.EXPAND, 5)

        # SPP层
        label_spp = wx.StaticText(self.networks_panel, wx.ID_ANY, u"SPP层网络参数:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        # 输入通道数
        label_spp_level = wx.StaticText(self.networks_panel, wx.ID_ANY, u"SPP层数:", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.text_spp_level = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                          style=wx.TE_LEFT)
        self.text_spp_level.AppendText('4')

        label_pooling_type = wx.StaticText(self.networks_panel, wx.ID_ANY, u"池化类型:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.pooling_type = ['最大池化', '平均池化']
        self.combobox_pooling_type = wx.ComboBox(self.networks_panel, -1, size=wx.Size(80, -1),
                                                 choices=self.pooling_type)
        self.combobox_pooling_type.SetSelection(0)

        spp_box = wx.BoxSizer(wx.HORIZONTAL)
        spp_box.Add((30, 20))
        spp_box.Add(label_spp, 1, wx.ALL | wx.EXPAND, 7)
        spp_box.Add(label_spp_level, 0, wx.ALL | wx.EXPAND, 7)
        spp_box.Add(self.text_spp_level, 5, wx.ALL | wx.EXPAND, 5)
        spp_box.Add(label_pooling_type, 0, wx.ALL | wx.EXPAND, 7)
        spp_box.Add(self.combobox_pooling_type, 5, wx.ALL | wx.EXPAND, 5)

        # 全连接层
        label_full_connect = wx.StaticText(self.networks_panel, wx.ID_ANY, u"全连接层网络参数:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        label_full_connect_num = wx.StaticText(self.networks_panel, wx.ID_ANY, u"全连接层数:", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.text_full_connect_num = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                 style=wx.TE_LEFT)
        self.text_full_connect_num.AppendText('1')

        label_full_connect_dim = wx.StaticText(self.networks_panel, wx.ID_ANY, u"全连接层维度:", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.text_full_connect_dim = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                 style=wx.TE_LEFT)
        self.text_full_connect_dim.AppendText('12')
        label_actor_lr = wx.StaticText(self.networks_panel, wx.ID_ANY, u"学习率:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.text_actor_lr = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                         style=wx.TE_LEFT)
        self.text_actor_lr.AppendText('1e-3')
        # activation function
        self.activation_functions = ['Relu', 'LeakyRelu', 'Softmax', 'Tanh']
        label_actor_af = wx.StaticText(self.networks_panel, wx.ID_ANY, u"激活函数:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.combobox_actor_af = wx.ComboBox(self.networks_panel, -1, size=wx.Size(80, -1),
                                             choices=self.activation_functions)
        self.combobox_actor_af.SetSelection(0)

        full_connect_box = wx.BoxSizer(wx.HORIZONTAL)
        full_connect_box.Add((30, 20))
        full_connect_box.Add(label_full_connect, 1, wx.ALL | wx.EXPAND, 7)
        full_connect_box.Add(label_full_connect_num, 0, wx.ALL | wx.EXPAND, 7)
        full_connect_box.Add(self.text_full_connect_num, 5, wx.ALL | wx.EXPAND, 5)
        full_connect_box.Add(label_full_connect_dim, 0, wx.ALL | wx.EXPAND, 7)
        full_connect_box.Add(self.text_full_connect_dim, 5, wx.ALL | wx.EXPAND, 5)
        full_connect_box.Add(label_actor_lr, 0, wx.ALL | wx.EXPAND, 7)
        full_connect_box.Add(self.text_actor_lr, 5, wx.ALL | wx.EXPAND, 5)
        full_connect_box.Add(label_actor_af, 0, wx.ALL | wx.EXPAND, 7)
        full_connect_box.Add(self.combobox_actor_af, 5, wx.ALL | wx.EXPAND, 5)

        # Critic网络参数
        label_critic = wx.StaticText(self.networks_panel, wx.ID_ANY, u"Critic网络参数:", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        label_critic_conv = wx.StaticText(self.networks_panel, wx.ID_ANY, u"卷积层网络参数:", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        label_critic_kernel_size = wx.StaticText(self.networks_panel, wx.ID_ANY, u"卷积核大小:", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.combobox_critic_kernel_size = wx.ComboBox(self.networks_panel, -1, size=wx.Size(80, -1),
                                                       choices=self.kernel_sizes)
        self.combobox_critic_kernel_size.SetSelection(0)
        # 输入通道数
        label_critic_input_channel = wx.StaticText(self.networks_panel, wx.ID_ANY, u"输入通道数:", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.text_critic_input_channel = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                     style=wx.TE_LEFT)
        self.text_critic_input_channel.AppendText('3')

        label_critic_output_channel = wx.StaticText(self.networks_panel, wx.ID_ANY, u"输出通道数:", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
        self.text_critic_output_channel = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                      style=wx.TE_LEFT)
        self.text_critic_output_channel.AppendText('16')

        label_critic_padding = wx.StaticText(self.networks_panel, wx.ID_ANY, u"填充数(padding):", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.text_critic_padding = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                               style=wx.TE_LEFT)
        self.text_critic_padding.AppendText('2')

        critic_conv_box = wx.BoxSizer(wx.HORIZONTAL)
        critic_conv_box.Add((30, 20))
        critic_conv_box.Add(label_critic_conv, 1, wx.ALL, 7)
        critic_conv_box.Add(label_critic_kernel_size, 0, wx.ALL | wx.EXPAND, 7)
        critic_conv_box.Add(self.combobox_critic_kernel_size, 1, wx.ALL | wx.EXPAND, 5)
        critic_conv_box.Add(label_critic_input_channel, 0, wx.ALL | wx.EXPAND, 7)
        critic_conv_box.Add(self.text_critic_input_channel, 5, wx.ALL | wx.EXPAND, 5)
        critic_conv_box.Add(label_critic_output_channel, 0, wx.ALL | wx.EXPAND, 7)
        critic_conv_box.Add(self.text_critic_output_channel, 5, wx.ALL | wx.EXPAND, 5)
        critic_conv_box.Add(label_critic_padding, 0, wx.ALL | wx.EXPAND, 7)
        critic_conv_box.Add(self.text_critic_padding, 5, wx.ALL | wx.EXPAND, 5)

        # SPP层
        label_critic_spp = wx.StaticText(self.networks_panel, wx.ID_ANY, u"SPP层网络参数:", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        # 输入通道数
        label_critic_spp_level = wx.StaticText(self.networks_panel, wx.ID_ANY, u"SPP层数:", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.text_critic_spp_level = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                 style=wx.TE_LEFT)
        self.text_critic_spp_level.AppendText('4')

        label_critic_pooling_type = wx.StaticText(self.networks_panel, wx.ID_ANY, u"池化类型:", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.critic_pooling_type = {'最大池化', '平均池化'}
        self.combobox_critic_pooling_type = wx.ComboBox(self.networks_panel, -1, size=wx.Size(80, -1),
                                                        choices=self.pooling_type)
        self.combobox_critic_pooling_type.SetSelection(0)

        critic_spp_box = wx.BoxSizer(wx.HORIZONTAL)
        critic_spp_box.Add((30, 20))
        critic_spp_box.Add(label_critic_spp, 1, wx.ALL | wx.EXPAND, 7)
        critic_spp_box.Add(label_critic_spp_level, 0, wx.ALL | wx.EXPAND, 7)
        critic_spp_box.Add(self.text_critic_spp_level, 5, wx.ALL | wx.EXPAND, 5)
        critic_spp_box.Add(label_critic_pooling_type, 0, wx.ALL | wx.EXPAND, 7)
        critic_spp_box.Add(self.combobox_critic_pooling_type, 5, wx.ALL | wx.EXPAND, 5)

        # 全连接层
        label_critic_full_connect = wx.StaticText(self.networks_panel, wx.ID_ANY, u"全连接层网络参数:", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        label_critic_full_connect_num = wx.StaticText(self.networks_panel, wx.ID_ANY, u"全连接层数:", wx.DefaultPosition,
                                                      wx.DefaultSize, 0)
        self.text_critic_full_connect_num = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                        style=wx.TE_LEFT)
        self.text_critic_full_connect_num.AppendText('1')

        label_critic_full_connect_dim = wx.StaticText(self.networks_panel, wx.ID_ANY, u"全连接层维度:", wx.DefaultPosition,
                                                      wx.DefaultSize, 0)
        self.text_critic_full_connect_dim = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                        style=wx.TE_LEFT)
        self.text_critic_full_connect_dim.AppendText('12')

        label_critic_lr = wx.StaticText(self.networks_panel, wx.ID_ANY, u"学习率:", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.text_critic_lr = wx.TextCtrl(self.networks_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                          style=wx.TE_LEFT)
        self.text_critic_lr.AppendText('3e-3')
        # activation function
        label_critic_af = wx.StaticText(self.networks_panel, wx.ID_ANY, u"激活函数:", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.combobox_critic_af = wx.ComboBox(self.networks_panel, -1, size=wx.Size(80, -1),
                                              choices=self.activation_functions)
        self.combobox_critic_af.SetSelection(0)

        critic_full_connect_box = wx.BoxSizer(wx.HORIZONTAL)
        critic_full_connect_box.Add((30, 20))
        critic_full_connect_box.Add(label_critic_full_connect, 1, wx.ALL | wx.EXPAND, 7)
        critic_full_connect_box.Add(label_critic_full_connect_num, 0, wx.ALL | wx.EXPAND, 7)
        critic_full_connect_box.Add(self.text_critic_full_connect_num, 5, wx.ALL | wx.EXPAND, 5)
        critic_full_connect_box.Add(label_critic_full_connect_dim, 0, wx.ALL | wx.EXPAND, 7)
        critic_full_connect_box.Add(self.text_critic_full_connect_dim, 5, wx.ALL | wx.EXPAND, 5)
        critic_full_connect_box.Add(label_critic_lr, 0, wx.ALL | wx.EXPAND, 7)
        critic_full_connect_box.Add(self.text_critic_lr, 5, wx.ALL | wx.EXPAND, 5)
        critic_full_connect_box.Add(label_critic_af, 0, wx.ALL | wx.EXPAND, 7)
        critic_full_connect_box.Add(self.combobox_critic_af, 5, wx.ALL | wx.EXPAND, 5)

        network_box = wx.BoxSizer(wx.VERTICAL)
        network_box.Add(label_actor, 0, wx.ALL, 5)
        network_box.Add(conv_box, 0, wx.ALL, 0)
        network_box.Add(spp_box, 0, wx.ALL, 0)
        network_box.Add(full_connect_box, 0, wx.ALL, 0)
        network_box.Add(label_critic, 0, wx.ALL, 5)
        network_box.Add(critic_conv_box, 0, wx.ALL, 0)
        network_box.Add(critic_spp_box, 0, wx.ALL, 0)
        network_box.Add(critic_full_connect_box, 0, wx.ALL, 5)
        self.networks_panel.SetSizer(network_box)
        self.networks_panel.Layout()
