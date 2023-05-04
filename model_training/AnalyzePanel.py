# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os
import wx.xrc
import wx.lib.newevent
import random
import numpy as np
import wx.lib.scrolledpanel as scrolled
from matplotlib import pyplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd


class AnalyzePanel(wx.Panel):

    def __init__(self, parent, model_path=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 显示中文标签
        ''' 第一行：选择路径按钮 '''
        file_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_file_path = wx.StaticText(file_panel, wx.ID_ANY, u"结果文件",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_file_path = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25), style=wx.TE_LEFT)
        ''' 选择路径按钮 '''
        btn_selection = wx.Button(file_panel, wx.ID_ANY, u"选择文件", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_selection.Bind(wx.EVT_BUTTON, self.on_selection_button)
        ''' 结果分析按钮 '''
        btn_analyzing = wx.Button(file_panel, wx.ID_ANY, u"结果分析",
                                   wx.DefaultPosition, wx.Size(100, 26), 0)
        btn_analyzing.SetBitmap(wx.Bitmap('icon/run.ico'))
        btn_analyzing.Bind(wx.EVT_BUTTON, self.on_button_analyzing)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_sizer.Add(label_file_path, 0, wx.ALL, 7)
        file_sizer.Add(self.text_file_path, 5, wx.ALL, 5)
        file_sizer.Add(btn_selection, 1, wx.ALL, 5)
        file_sizer.Add(btn_analyzing, 1, wx.ALL, 5)
        file_panel.SetSizer(file_sizer)

        self.show_panel = scrolled.ScrolledPanel(self, -1, style=wx.TAB_TRAVERSAL
                                                                 | wx.SUNKEN_BORDER, name="show_panel")
        # main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(file_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.show_panel, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def on_selection_button(self, event):
        dlg = wx.FileDialog(self, u"选择文件", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_file_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def init_show_panel(self):
        show_panel = self.show_panel
        for child in show_panel.Children:
            child.Destroy()

        self.notebook_analyzing = wx.Notebook(show_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.notebook_analyzing.Hide()
        # 绘制make span, reward, opt_make span界面
        panel_lines = wx.Panel(self.notebook_analyzing, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                      wx.TAB_TRAVERSAL)

        figure_results = plt.figure()
        self.axes_lines = figure_results.add_subplot(1, 1, 1)
        canvas_results = FigureCanvas(panel_lines, -1, figure_results)
        process_sizer = wx.BoxSizer(wx.VERTICAL)
        process_sizer.Add(canvas_results, 1, wx.EXPAND | wx.ALL, 0)
        panel_lines.SetSizer(process_sizer)
        self.notebook_analyzing.AddPage(panel_lines, u"训练结果", True)

        # 绘制最优调度序列和甘特图
        panel_solution = wx.Panel(self.notebook_analyzing, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        fig_solution = plt.figure()

        self.axes_gantt = fig_solution.add_subplot(1, 1, 1)
        canvas_solution = FigureCanvas(panel_solution, -1, fig_solution)
        gbSizer_result = wx.BoxSizer(wx.VERTICAL)
        gbSizer_result.Add(canvas_solution, 1, wx.EXPAND | wx.ALL, 0)
        panel_solution.SetSizer(gbSizer_result)
        self.notebook_analyzing.AddPage(panel_solution, u"调度结果", False)

        show_sizer = wx.BoxSizer(wx.VERTICAL)
        show_sizer.Add(self.notebook_analyzing, 1, wx.EXPAND | wx.ALL, 0)
        show_panel.SetSizer(show_sizer)
        show_panel.Layout()

    def on_button_analyzing(self, event):
        self.init_show_panel()
        file_path = self.text_file_path.GetLineText(0)
        data = pd.read_csv(file_path)
        episodes = data.values[:, 0]
        make_span = data.values[:, 2]
        reward = data.values[:, 3]
        min_make_span = data.values[:, 4]

        ''' 绘制曲线'''
        labels = ['最大完成时间', '最优完成时间', '回报函数']
        h_make_span, = self.axes_lines.plot(episodes, make_span, 'r-')
        h_min_make_span, = self.axes_lines.plot(episodes, min_make_span, 'b--')
        self.axes_lines.set(xlabel=u'迭代次数', ylabel=u'完成时间', title=u'结果曲线')

        axes_twins = self.axes_lines.twinx()
        '''绘制次坐标reward'''
        h_reward, = axes_twins.plot(episodes, reward, 'g-')
        axes_twins.set(xlabel=u'迭代次数', ylabel=u'回报')
        axes_twins.legend(handles=[h_make_span, h_min_make_span, h_reward], labels=labels, loc='upper left')

        solution_path = file_path.split('.')[0]+'_solution.csv'
        gantt = pd.read_csv(solution_path)
        job = gantt.values[:, 1]
        machine = gantt.values[:, 2]
        start = gantt.values[:, 3]
        end = gantt.values[:, 4]
        width = gantt.values[:, 5]

        job_labels = []  # 生成图例标签
        dict = np.zeros(round(max(job)), dtype=int)
        handles = []
        colors = ['#%06X' % random.randint(0, 256 ** 3 - 1) for _ in range(200)]
        for i in range(len(job)):
            if dict[round(job[i]-1)] == 0:
                job_labels.append("作业" + str(round(job[i])))
                h1, = self.axes_gantt.barh(y=machine[i], width=width[i], left=start[i], edgecolor="black",
                                                    color=colors[round(job[i])])
                handles.append(h1)
                dict[round(job[i]-1)] = 1
            else:
                self.axes_gantt.barh(y=machine[i], width=width[i], left=start[i], edgecolor="black",
                                     color=colors[round(job[i])])
        x, length = self.axes_gantt.get_xlim()
        self.axes_gantt.set_xlim(0, length+100)
        self.axes_gantt.legend(handles=handles, labels=job_labels, loc='upper right')
        self.axes_gantt.set(xlabel=u'时间', ylabel=u'机器编号', title=u'甘特图')
        self.notebook_analyzing.Show()
        self.show_panel.Layout()
