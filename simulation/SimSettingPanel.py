# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os

import pandas as pd
import wx.xrc
import wx.lib.newevent
import wx.lib.scrolledpanel as scrolled
import random
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element


class SimSettingPanel(wx.Panel):

    def __init__(self, parent, order_path, model_path, page_id):
        wx.Panel.__init__(self, parent, page_id, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.model_path = model_path
        ''' 第一行：订单路径按钮 '''
        file_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.check_simulation_batches = wx.CheckBox(file_panel, label='批量仿真')
        label_file_name = wx.StaticText(file_panel, wx.ID_ANY, u"订单路径:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_file_path = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25), style=wx.TE_LEFT)
        self.text_file_path.AppendText(order_path)
        btn_select_order = wx.Button(file_panel, wx.ID_ANY, u"选择", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_select_order.Bind(wx.EVT_BUTTON, self.on_button_select_order)

        ''' 运行按钮 '''
        btn_save = wx.Button(file_panel, wx.ID_ANY, u"运行", wx.DefaultPosition, wx.Size(100, 26), 0)
        btn_save.SetBitmap(wx.Bitmap('icon/run.ico'))
        btn_save.Bind(wx.EVT_BUTTON, self.on_button_run)

        order_sizer = wx.BoxSizer(wx.HORIZONTAL)
        order_sizer.Add(self.check_simulation_batches, 0, wx.ALL, 7)
        order_sizer.Add(label_file_name, 0, wx.ALL, 7)
        order_sizer.Add(self.text_file_path, 5, wx.ALL, 5)
        order_sizer.Add(btn_select_order, 1, wx.ALL, 5)
        order_sizer.Add(btn_save, 1, wx.ALL, 5)
        file_panel.SetSizer(order_sizer)

        self.model_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_model_type = wx.StaticText(self.model_panel, wx.ID_ANY, u"调度模型：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.model_type = ['PDR', 'DRL']
        self.combobox_model_type = wx.ComboBox(self.model_panel, -1, size=wx.Size(100, -1),
                                               choices=self.model_type)
        self.combobox_model_type.SetSelection(0)
        self.combobox_model_type.Bind(wx.EVT_COMBOBOX, self.on_select_combobox_model)
        self.PDR_type = ['None', 'SPT', 'MWKR', 'FDD/MWKR', 'MOPNR', 'LRM ', 'FIFO ',
                                 'LPT', 'LWKR', 'FDD/LWKR', 'LOPNR', 'SRM ', 'FILO ']
        self.combobox_PDR_type = wx.ComboBox(self.model_panel, -1, size=wx.Size(100, -1),
                                               choices=self.PDR_type)
        self.combobox_PDR_type.SetSelection(1)

        label_path = wx.StaticText(self.model_panel, wx.ID_ANY, u"模型路径：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_model_path = wx.TextCtrl(self.model_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25),
                                           style=wx.TE_LEFT)
        self.text_model_path.AppendText(self.model_path)
        ''' 选择路径按钮 '''
        btn_select_model = wx.Button(self.model_panel, wx.ID_ANY, u"选择", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_select_model.Bind(wx.EVT_BUTTON, self.on_button_select_model)

        self.model_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.model_sizer.Add(label_model_type, 0, wx.ALL, 7)
        self.model_sizer.Add(self.combobox_model_type, 1, wx.ALL, 5)
        self.model_sizer.Add(self.combobox_PDR_type, 1, wx.ALL, 5)
        self.model_sizer.Add(label_path, 0, wx.ALL, 7)
        self.model_sizer.Add(self.text_model_path, 5, wx.ALL, 5)
        self.model_sizer.Add(btn_select_model, 1, wx.ALL, 5)
        self.model_panel.SetSizer(self.model_sizer)

        self.show_panel = scrolled.ScrolledPanel(self, -1, style=wx.TAB_TRAVERSAL
                                                                 | wx.SUNKEN_BORDER, name="show_panel")
        # main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(file_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.model_panel, 0, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def on_button_select_order(self, event):
        mode = self.check_simulation_batches.GetValue()
        if not mode:
            dlg = wx.FileDialog(self, u"选择订单", style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.text_file_path.SetValue(dlg.GetPath())
            dlg.Destroy()
        else:
            dlg = wx.DirDialog(self, u"选择订单", style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.text_file_path.SetValue(dlg.GetPath())
            dlg.Destroy()

    def on_button_select_model(self, event):
        dlg = wx.DirDialog(self, u"选择模型", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_model_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_select_combobox_model(self, event):
        pos = self.combobox_model_type.GetSelection()
        if pos == 0:
            self.combobox_PDR_type.SetSelection(1)
        else:
            self.combobox_PDR_type.SetSelection(0)

    def init_show_panel(self):
        show_panel = self.show_panel
        for child in show_panel.Children:
            child.Destroy()

        if self.check_simulation_batches.GetValue():
            # 绘制make span, reward, opt_make span界面
            figure_results = plt.figure()
            self.axes_lines = figure_results.add_subplot(1, 1, 1)
            canvas_results = FigureCanvas(show_panel, -1, figure_results)
            process_sizer = wx.BoxSizer(wx.VERTICAL)
            process_sizer.Add(canvas_results, 1, wx.EXPAND | wx.ALL, 0)
            show_panel.SetSizer(process_sizer)
        else:
            # 绘制最优调度序列和甘特图
            fig_solution = plt.figure()
            self.axes_gantt = fig_solution.add_subplot(1, 1, 1)
            canvas_solution = FigureCanvas(show_panel, -1, fig_solution)
            gbSizer_result = wx.BoxSizer(wx.VERTICAL)
            gbSizer_result.Add(canvas_solution, 1, wx.EXPAND | wx.ALL, 0)
            show_panel.SetSizer(gbSizer_result)

        show_panel.Layout()

    def on_button_run(self, event):
        print("run")
        # self.init_show_panel()
        # if self.check_simulation_batches.GetValue():
        #     file_path = self.text_file_path.GetLineText(0)
        #     data = pd.read_csv(file_path)
        #     episodes = data.values[:, 0]
        #     make_span = data.values[:, 2]
        #     reward = data.values[:, 3]
        #     min_make_span = data.values[:, 4]
        #
        #     ''' 绘制曲线'''
        #     labels = ['最大完成时间', '最优完成时间', '回报函数']
        #     h_make_span, = self.axes_lines.plot(episodes, make_span, 'r-')
        #     h_min_make_span, = self.axes_lines.plot(episodes, min_make_span, 'b--')
        #     self.axes_lines.set(xlabel=u'迭代次数', ylabel=u'完成时间', title=u'结果曲线')
        #
        #     axes_twins = self.axes_lines.twinx()
        #     '''绘制次坐标reward'''
        #     h_reward, = axes_twins.plot(episodes, reward, 'g-')
        #     axes_twins.set(xlabel=u'迭代次数', ylabel=u'回报')
        #     axes_twins.legend(handles=[h_make_span, h_min_make_span, h_reward], labels=labels, loc='upper left')
        # else:
        #     solution_path = file_path.split('.')[0] + '_solution.csv'
        #     gantt = pd.read_csv(solution_path)
        #     job = gantt.values[:, 1]
        #     machine = gantt.values[:, 2]
        #     start = gantt.values[:, 3]
        #     end = gantt.values[:, 4]
        #     width = gantt.values[:, 5]
        #
        #     job_labels = []  # 生成图例标签
        #     dict = np.zeros(round(max(job)), dtype=int)
        #     handles = []
        #     colors = ['#%06X' % random.randint(0, 256 ** 3 - 1) for _ in range(200)]
        #     for i in range(len(job)):
        #         if dict[round(job[i] - 1)] == 0:
        #             job_labels.append("作业" + str(round(job[i])))
        #             h1, = self.axes_gantt.barh(y=machine[i], width=width[i], left=start[i], edgecolor="black",
        #                                        color=colors[round(job[i])])
        #             handles.append(h1)
        #             dict[round(job[i] - 1)] = 1
        #         else:
        #             self.axes_gantt.barh(y=machine[i], width=width[i], left=start[i], edgecolor="black",
        #                                  color=colors[round(job[i])])
        #     x, length = self.axes_gantt.get_xlim()
        #     self.axes_gantt.set_xlim(0, length + 100)
        #     self.axes_gantt.legend(handles=handles, labels=job_labels, loc='upper right')
        #     self.axes_gantt.set(xlabel=u'时间', ylabel=u'机器编号', title=u'甘特图')
        # self.show_panel.Layout()


