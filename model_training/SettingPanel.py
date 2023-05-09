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


class SettingPanel(wx.Panel):

    def __init__(self, parent, model_path=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        dir_name = os.path.basename(model_path)
        description_file = dir_name + '_description.xml'
        self.path = os.path.join(model_path, description_file)
        self.tree = et.parse(self.path)
        self.root = self.tree.getroot()
        train_base = self.root.find('train_base')
        if train_base is not None:
            order_path = str(train_base.get('order_path'))
            max_episodes = str(train_base.get('max_episodes'))
            max_time = str(train_base.get('max_time'))
            trajectory_num = str(train_base.get('trajectory_num'))
            batch_size = str(train_base.get('batch_size'))
        else:
            order_path = 'C:\\Users\\wxq\\Desktop\\ScheduleSystem-main\\training'
            max_episodes = '4000'
            max_time = '3600'
            trajectory_num = '3'
            batch_size = '256'
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

        ''' 训练按钮 '''
        btn_save = wx.Button(file_panel, wx.ID_ANY, u"开始训练", wx.DefaultPosition, wx.Size(100, 26), 0)
        btn_save.SetBitmap(wx.Bitmap('icon/run.ico'))
        btn_save.Bind(wx.EVT_BUTTON, self.on_button_train)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_sizer.Add(label_file_name, 0, wx.ALL, 7)
        file_sizer.Add(self.text_file_name, 5, wx.ALL, 5)
        file_sizer.Add(label_file_path, 0, wx.ALL, 7)
        file_sizer.Add(self.text_file_path, 5, wx.ALL, 5)
        file_sizer.Add(btn_selection, 1, wx.ALL, 5)
        file_sizer.Add(btn_save, 1, wx.ALL, 5)
        file_panel.SetSizer(file_sizer)

        # 基本训练参数
        self.train_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_base = wx.StaticText(self.train_panel, wx.ID_ANY, u"基本训练参数:", wx.DefaultPosition,
                                       wx.DefaultSize, 0)

        label_episodes = wx.StaticText(self.train_panel, wx.ID_ANY, u"最大训练轮数:", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.text_max_episodes = wx.TextCtrl(self.train_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                          style=wx.TE_LEFT)
        self.text_max_episodes.AppendText(max_episodes)

        label_time = wx.StaticText(self.train_panel, wx.ID_ANY, u"最大训练时长:", wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        self.text_max_time = wx.TextCtrl(self.train_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                      style=wx.TE_LEFT)
        self.text_max_time.AppendText(max_time)
        label_second = wx.StaticText(self.train_panel, wx.ID_ANY, u"秒", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        label_trajectories = wx.StaticText(self.train_panel, wx.ID_ANY, u"轨迹数:", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.text_trajectories = wx.TextCtrl(self.train_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                        style=wx.TE_LEFT)
        self.text_trajectories.AppendText(trajectory_num)
        label_batch = wx.StaticText(self.train_panel, wx.ID_ANY, u"训练批次大小:", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.text_batch = wx.TextCtrl(self.train_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                        style=wx.TE_LEFT)
        self.text_batch.AppendText(batch_size)

        base_box = wx.BoxSizer(wx.HORIZONTAL)
        base_box.Add((30, 20))
        base_box.Add(label_episodes, 1, wx.ALL | wx.EXPAND, 7)
        base_box.Add(self.text_max_episodes, 5, wx.ALL | wx.EXPAND, 5)
        base_box.Add(label_time, 0, wx.ALL | wx.EXPAND, 7)
        base_box.Add(self.text_max_time, 5, wx.ALL | wx.EXPAND, 5)
        base_box.Add(label_second, 0, wx.ALL | wx.EXPAND, 7)
        base_box.Add(label_trajectories, 0, wx.ALL | wx.EXPAND, 7)
        base_box.Add(self.text_trajectories, 5, wx.ALL | wx.EXPAND, 5)
        base_box.Add(label_batch, 0, wx.ALL | wx.EXPAND, 7)
        base_box.Add(self.text_batch, 5, wx.ALL | wx.EXPAND, 5)

        RL_box = wx.BoxSizer(wx.VERTICAL)
        RL_box.Add(label_base, 0, wx.ALL, 7)
        RL_box.Add(base_box, 0, wx.ALL, 0)
        self.train_panel.SetSizer(RL_box)

        per = self.root.find('PER')
        if per is not None:
            check_per = per.get('check_per')
            alpha = str(per.get('alpha'))
            conv_steps = str(per.get('conv_steps'))
            replay_num = str(per.get('replay_num'))
            check_is = str(per.get('check_is'))
            beta = str(per.get('beta'))
            sample_type = str(per.get('sample_type'))
            batch_type = str(per.get('batch_type'))
            init_replay_batch = str(per.get('init_replay_batch'))
            max_replay_batch = str(per.get('max_replay_batch'))
        else:
            check_per = 'False'
            alpha = '0.6'
            conv_steps = '500'
            replay_num = '1'
            check_is = 'False'
            beta = '0.4'
            sample_type = '0'
            batch_type = '0'
            init_replay_batch = '10'
            max_replay_batch = '10'
        # 基本训练参数
        bool_value = {'False': False, 'True': True}
        self.per_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.check_per = wx.CheckBox(self.per_panel, label='优先经验重放:')
        self.check_per.SetValue(bool_value[check_per])

        label_alpha = wx.StaticText(self.per_panel, wx.ID_ANY, u"优先指数(alpha):", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.text_alpha = wx.TextCtrl(self.per_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                             style=wx.TE_LEFT)
        self.text_alpha.AppendText(alpha)

        label_conv_steps = wx.StaticText(self.per_panel, wx.ID_ANY, u"收敛步数:", wx.DefaultPosition,
                                   wx.DefaultSize, 0)
        self.text_conv_steps = wx.TextCtrl(self.per_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                         style=wx.TE_LEFT)
        self.text_conv_steps.AppendText(conv_steps)
        label_replays = wx.StaticText(self.per_panel, wx.ID_ANY, u"重放次数:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.text_replays = wx.TextCtrl(self.per_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                             style=wx.TE_LEFT)
        self.text_replays.AppendText(replay_num)
        self.check_is = wx.CheckBox(self.per_panel, label='重要性权重修正:')
        self.check_is.SetValue(bool_value[check_is])

        label_beta = wx.StaticText(self.per_panel, wx.ID_ANY, u"初始权重指数(beta):", wx.DefaultPosition,
                                   wx.DefaultSize, 0)
        self.text_beta = wx.TextCtrl(self.per_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                     style=wx.TE_LEFT)
        self.text_beta.AppendText(beta)

        per_box = wx.BoxSizer(wx.HORIZONTAL)
        per_box.Add((30, 20))
        per_box.Add(label_alpha, 1, wx.ALL | wx.EXPAND, 7)
        per_box.Add(self.text_alpha, 5, wx.ALL | wx.EXPAND, 5)
        per_box.Add(label_conv_steps, 0, wx.ALL | wx.EXPAND, 7)
        per_box.Add(self.text_conv_steps, 5, wx.ALL | wx.EXPAND, 5)
        per_box.Add(label_replays, 0, wx.ALL | wx.EXPAND, 7)
        per_box.Add(self.text_replays, 5, wx.ALL | wx.EXPAND, 5)
        per_box.Add(self.check_is, 0, wx.ALL | wx.EXPAND, 7)
        per_box.Add(label_beta, 0, wx.ALL | wx.EXPAND, 7)
        per_box.Add(self.text_beta, 5, wx.ALL | wx.EXPAND, 5)

        # 样本类型
        self.sample_type = ['正TD样本', '负TD样本', '所有样本']
        label_sample_type = wx.StaticText(self.per_panel, wx.ID_ANY, u"样本类型:",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.combobox_sample_type = wx.ComboBox(self.per_panel, -1, size=wx.Size(80, -1),
                                                choices=self.sample_type)
        self.combobox_sample_type.SetSelection(int(sample_type))
        # 优先经验重放批次
        self.batch_type = ['固定大小', '线性增加', '二次增加']
        label_batch_type = wx.StaticText(self.per_panel, wx.ID_ANY, u"优先经验重放批次:",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.combobox_batch_type = wx.ComboBox(self.per_panel, -1, size=wx.Size(80, -1),
                                                choices=self.batch_type)
        self.combobox_batch_type.SetSelection(int(batch_type))
        label_init_replay_batch = wx.StaticText(self.per_panel, wx.ID_ANY, u"初始批次大小:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.text_init_replay_batch = wx.TextCtrl(self.per_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                             style=wx.TE_LEFT)
        self.text_init_replay_batch.AppendText(init_replay_batch)
        label_max_replay_batch = wx.StaticText(self.per_panel, wx.ID_ANY, u"最大批次大小:", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.text_max_replay_batch = wx.TextCtrl(self.per_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25),
                                                  style=wx.TE_LEFT)
        self.text_max_replay_batch.AppendText(max_replay_batch)

        is_box = wx.BoxSizer(wx.HORIZONTAL)
        is_box.Add((30, 20))
        is_box.Add(label_sample_type, 1, wx.ALL | wx.EXPAND, 7)
        is_box.Add(self.combobox_sample_type, 5, wx.ALL | wx.EXPAND, 5)
        is_box.Add(label_batch_type, 1, wx.ALL | wx.EXPAND, 7)
        is_box.Add(self.combobox_batch_type, 5, wx.ALL | wx.EXPAND, 5)
        is_box.Add(label_init_replay_batch, 0, wx.ALL | wx.EXPAND, 7)
        is_box.Add(self.text_init_replay_batch, 5, wx.ALL | wx.EXPAND, 5)
        is_box.Add(label_max_replay_batch, 0, wx.ALL | wx.EXPAND, 7)
        is_box.Add(self.text_max_replay_batch, 5, wx.ALL | wx.EXPAND, 5)

        per_vbox = wx.BoxSizer(wx.VERTICAL)
        per_vbox.Add(self.check_per, 0, wx.ALL, 7)
        per_vbox.Add(per_box, 0, wx.ALL, 0)
        per_vbox.Add(is_box, 0, wx.ALL, 0)
        self.per_panel.SetSizer(per_vbox)
        # main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(file_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.train_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.per_panel, 0, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def on_selection_button(self, event):
        dlg = wx.FileDialog(self, u"选择文件", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_file_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_button_train(self, event):
        train_base = self.root.find("train_base")
        if train_base is None:
            train_base = Element("train_base")
            self.root.append(train_base)
        order_path = self.text_file_path.GetLineText(0)
        max_episodes = self.text_max_episodes.GetLineText(0)
        max_time = self.text_max_time.GetLineText(0)
        trajectory_num = self.text_trajectories.GetLineText(0)
        batch_size = self.text_batch.GetLineText(0)
        train_base.set('order_path', str(order_path))
        train_base.set('max_episodes', str(max_episodes))
        train_base.set('max_time', str(max_time))
        train_base.set('trajectory_num', str(trajectory_num))
        train_base.set('batch_size', str(batch_size))

        per = self.root.find("PER")
        if per is None:
            per = Element('PER')
            self.root.append(per)
        check_per = self.check_per.GetValue()
        alpha = self.text_alpha.GetLineText(0)
        conv_steps = self.text_conv_steps.GetLineText(0)
        replay_num = self.text_replays.GetLineText(0)
        check_is = self.check_is.GetValue()
        beta = self.text_beta.GetLineText(0)
        sample_type = self.combobox_sample_type.GetSelection()
        batch_type = self.combobox_batch_type.GetSelection()
        init_replay_batch = self.text_init_replay_batch.GetLineText(0)
        max_replay_batch = self.text_max_replay_batch.GetLineText(0)

        per.set('check_per', str(check_per))
        per.set('alpha', str(alpha))
        per.set('conv_steps', str(conv_steps))
        per.set('replay_num', str(replay_num))
        per.set('check_is', str(check_is))
        per.set('beta', str(beta))
        per.set('sample_type', str(sample_type))
        per.set('batch_type', str(batch_type))
        per.set('init_replay_batch', str(init_replay_batch))
        per.set('max_replay_batch', str(max_replay_batch))

        self.tree.write(self.path)
