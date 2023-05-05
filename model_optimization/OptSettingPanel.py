# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os
import wx.xrc
import wx.lib.newevent
import random
import numpy as np
import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element


class OptSettingPanel(wx.Panel):

    def __init__(self, parent, model_path, page_id):
        wx.Panel.__init__(self, parent, page_id, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        dir_name = os.path.basename(model_path)
        description_file = dir_name + '_description.xml'
        self.path = os.path.join(model_path, description_file)
        self.tree = et.parse(self.path)
        self.root = self.tree.getroot()
        train_base = self.root.find('train_base')
        if train_base is not None:
            order_path = str(train_base.get('order_path'))
            trajectory_num = str(train_base.get('trajectory_num'))
            batch_size = str(train_base.get('batch_size'))
        else:
            order_path = 'C:\\Users\\wxq\\Desktop\\ScheduleSystem-main\\training'
            trajectory_num = '3'
            batch_size = '1'
        ''' 第一行：选择路径按钮 '''
        file_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_file_name = wx.StaticText(file_panel, wx.ID_ANY, u"模型路径:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_file_name = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25), style=wx.TE_LEFT)
        self.text_file_name.AppendText(model_path)
        self.text_file_name.SetEditable(False)
        label_file_path = wx.StaticText(file_panel, wx.ID_ANY, u"订单路径：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_file_path = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25), style=wx.TE_LEFT)
        self.text_file_path.AppendText(order_path)
        ''' 选择路径按钮 '''
        btn_selection = wx.Button(file_panel, wx.ID_ANY, u"选择", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_selection.Bind(wx.EVT_BUTTON, self.on_selection_button)

        ''' 优化按钮 '''
        btn_save = wx.Button(file_panel, wx.ID_ANY, u"开始优化", wx.DefaultPosition, wx.Size(100, 26), 0)
        btn_save.SetBitmap(wx.Bitmap('icon/run.ico'))
        btn_save.Bind(wx.EVT_BUTTON, self.on_button_opt)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_sizer.Add(label_file_name, 0, wx.ALL, 7)
        file_sizer.Add(self.text_file_name, 5, wx.ALL, 5)
        file_sizer.Add(label_file_path, 0, wx.ALL, 7)
        file_sizer.Add(self.text_file_path, 5, wx.ALL, 5)
        file_sizer.Add(btn_selection, 1, wx.ALL, 5)
        file_sizer.Add(btn_save, 1, wx.ALL, 5)
        file_panel.SetSizer(file_sizer)

        # 设置优化参数
        self.parameter_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_train_parameter = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"优化训练参数:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.check_trajectories = wx.CheckBox(self.parameter_panel, label='经验池大小(轨迹数):')
        label_min_trajectories = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最小值:", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.text_min_trajectories = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                          style=wx.TE_LEFT)
        self.text_min_trajectories.AppendText(trajectory_num)
        label_max_trajectories = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最大值:", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.text_max_trajectories = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                 style=wx.TE_LEFT)
        self.text_max_trajectories.AppendText(trajectory_num)

        base_box = wx.BoxSizer(wx.HORIZONTAL)
        base_box.Add((30, 20))
        base_box.Add(self.check_trajectories, 1, wx.ALL | wx.EXPAND, 5)
        base_box.Add(label_min_trajectories, 0, wx.ALL | wx.EXPAND, 7)
        base_box.Add(self.text_min_trajectories, 5, wx.ALL | wx.EXPAND, 5)
        base_box.Add(label_max_trajectories, 0, wx.ALL | wx.EXPAND, 7)
        base_box.Add(self.text_max_trajectories, 5, wx.ALL | wx.EXPAND, 5)

        self.check_batch = wx.CheckBox(self.parameter_panel, label='经验回放批次大小:')
        label_min_batch = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最小值:", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.text_min_batch = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                 style=wx.TE_LEFT)
        self.text_min_batch.AppendText(batch_size)
        label_max_batch = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最大值:", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.text_max_batch = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                 style=wx.TE_LEFT)
        self.text_max_batch.AppendText(batch_size)
        base_box2 = wx.BoxSizer(wx.HORIZONTAL)
        base_box2.Add((30, 20))
        base_box2.Add(self.check_batch, 1, wx.ALL | wx.EXPAND, 5)
        base_box2.Add((10, 20))
        base_box2.Add(label_min_batch, 0, wx.ALL | wx.EXPAND, 7)
        base_box2.Add(self.text_min_batch, 5, wx.ALL | wx.EXPAND, 5)
        base_box2.Add(label_max_batch, 0, wx.ALL | wx.EXPAND, 7)
        base_box2.Add(self.text_max_batch, 5, wx.ALL | wx.EXPAND, 5)

        # 设置Actor网络参数
        label_actor_parameter = wx.StaticText(self.parameter_panel, wx.ID_ANY, u" Actor网络参数:", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.check_layers = wx.CheckBox(self.parameter_panel, label='隐藏层层数:')
        label_min_layers = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最小值:", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.text_min_layers = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                           style=wx.TE_LEFT)
        self.text_min_layers.AppendText('1')
        label_max_layers = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最大值:", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.text_max_layers = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                           style=wx.TE_LEFT)
        self.text_max_layers.AppendText('1')

        base_box0 = wx.BoxSizer(wx.HORIZONTAL)
        base_box0.Add((30, 20))
        base_box0.Add(self.check_layers, 1, wx.ALL | wx.EXPAND, 5)
        base_box0.Add(label_min_layers, 0, wx.ALL | wx.EXPAND, 7)
        base_box0.Add(self.text_min_layers, 5, wx.ALL | wx.EXPAND, 5)
        base_box0.Add(label_max_layers, 0, wx.ALL | wx.EXPAND, 7)
        base_box0.Add(self.text_max_layers, 5, wx.ALL | wx.EXPAND, 5)

        self.check_hidden_dim = wx.CheckBox(self.parameter_panel, label='隐藏层维度:')
        label_min_hidden_dim = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最小值:", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.text_min_hidden_dim = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                               style=wx.TE_LEFT)
        self.text_min_hidden_dim.AppendText('50')
        label_max_hidden_dim = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最大值:", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.text_max_hidden_dim = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                               style=wx.TE_LEFT)
        self.text_max_hidden_dim.AppendText('240')

        base_box1 = wx.BoxSizer(wx.HORIZONTAL)
        base_box1.Add((30, 20))
        base_box1.Add(self.check_hidden_dim, 1, wx.ALL | wx.EXPAND, 5)
        base_box1.Add(label_min_hidden_dim, 0, wx.ALL | wx.EXPAND, 7)
        base_box1.Add(self.text_min_hidden_dim, 5, wx.ALL | wx.EXPAND, 5)
        base_box1.Add(label_max_hidden_dim, 0, wx.ALL | wx.EXPAND, 7)
        base_box1.Add(self.text_max_hidden_dim, 5, wx.ALL | wx.EXPAND, 5)
        # 优化PPO参数
        ppo = self.root.find('ppo')
        gamma = ppo.get('gamma')
        epsilon = ppo.get('epsilon')
        updates = ppo.get('updates')
        label_ppo_parameter = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"优化PPO模型参数:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        self.check_gamma = wx.CheckBox(self.parameter_panel, label='回报折扣率(gamma):')
        label_min = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最小值:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        label_max = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最大值:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        self.text_min_gamma = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                          style=wx.TE_LEFT)
        self.text_min_gamma.AppendText(gamma)
        self.text_max_gamma = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                          style=wx.TE_LEFT)
        self.text_max_gamma.AppendText(gamma)
        base_box3 = wx.BoxSizer(wx.HORIZONTAL)
        base_box3.Add((30, 20))
        base_box3.Add(self.check_gamma, 1, wx.ALL | wx.EXPAND, 5)
        base_box3.Add(label_min, 0, wx.ALL | wx.EXPAND, 7)
        base_box3.Add(self.text_min_gamma, 5, wx.ALL | wx.EXPAND, 5)
        base_box3.Add(label_max, 0, wx.ALL | wx.EXPAND, 7)
        base_box3.Add(self.text_max_gamma, 5, wx.ALL | wx.EXPAND, 5)

        self.check_epsilon = wx.CheckBox(self.parameter_panel, label='裁剪参数(epsilon):')
        label_min = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最小值:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        label_max = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最大值:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        self.text_min_epsilon = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                            style=wx.TE_LEFT)
        self.text_min_epsilon.AppendText(epsilon)
        self.text_max_epsilon = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                            style=wx.TE_LEFT)
        self.text_max_epsilon.AppendText(epsilon)
        base_box4 = wx.BoxSizer(wx.HORIZONTAL)
        base_box4.Add((30, 20))
        base_box4.Add(self.check_epsilon, 1, wx.ALL | wx.EXPAND, 5)
        base_box4.Add((17, 20))
        base_box4.Add(label_min, 0, wx.ALL | wx.EXPAND, 7)
        base_box4.Add(self.text_min_epsilon, 5, wx.ALL | wx.EXPAND, 5)
        base_box4.Add(label_max, 0, wx.ALL | wx.EXPAND, 7)
        base_box4.Add(self.text_max_epsilon, 5, wx.ALL | wx.EXPAND, 5)

        self.check_updates = wx.CheckBox(self.parameter_panel, label='网络更新次数:')
        label_min = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最小值:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        label_max = wx.StaticText(self.parameter_panel, wx.ID_ANY, u"最大值:", wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        self.text_min_updates = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                            style=wx.TE_LEFT)
        self.text_min_updates.AppendText(updates)
        self.text_max_updates = wx.TextCtrl(self.parameter_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                            style=wx.TE_LEFT)
        self.text_max_updates.AppendText(updates)
        base_box5 = wx.BoxSizer(wx.HORIZONTAL)
        base_box5.Add((30, 20))
        base_box5.Add(self.check_updates, 1, wx.ALL | wx.EXPAND, 5)
        base_box5.Add((37, 20))
        base_box5.Add(label_min, 0, wx.ALL | wx.EXPAND, 7)
        base_box5.Add(self.text_min_updates, 5, wx.ALL | wx.EXPAND, 5)
        base_box5.Add(label_max, 0, wx.ALL | wx.EXPAND, 7)
        base_box5.Add(self.text_max_updates, 5, wx.ALL | wx.EXPAND, 5)

        RL_box = wx.BoxSizer(wx.VERTICAL)
        RL_box.Add(label_train_parameter, 0, wx.ALL, 7)
        RL_box.Add(base_box, 0, wx.ALL, 0)
        RL_box.Add(base_box2, 0, wx.ALL, 0)
        RL_box.Add(label_actor_parameter, 0, wx.ALL, 0)
        RL_box.Add(base_box0, 0, wx.ALL, 0)
        RL_box.Add(base_box1, 0, wx.ALL, 0)
        RL_box.Add(label_ppo_parameter, 0, wx.ALL, 7)
        RL_box.Add(base_box3, 0, wx.ALL, 0)
        RL_box.Add(base_box4, 0, wx.ALL, 0)
        RL_box.Add(base_box5, 0, wx.ALL, 0)
        self.parameter_panel.SetSizer(RL_box)
        # main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(file_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.parameter_panel, 0, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def on_selection_button(self, event):
        dlg = wx.FileDialog(self, u"选择文件", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_file_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_button_opt(self, event):
        print("opt")
