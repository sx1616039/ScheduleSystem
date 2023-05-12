# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os
import wx.xrc
import wx.lib.newevent
import numpy as np


class EditPanel(wx.Panel):

    def __init__(self, parent, order_path, page_id):
        wx.Panel.__init__(self, parent, page_id, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.path = order_path
        # 表格
        grid_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.grid = wx.grid.Grid(grid_panel, id=wx.ID_ANY, size=(900, 500))
        # 创建一个100X50的电子表格
        self.grid.CreateGrid(100, 50 * 2)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.change_value)
        grid_box = wx.BoxSizer(wx.HORIZONTAL)
        grid_box.Add(self.grid, proportion=1, flag=wx.EXPAND)
        grid_panel.SetSizer(grid_box)

        # main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(grid_panel, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

        with open(self.path, 'r') as f:
            user_line = f.readline()
            data = user_line.split('\t')
            m_n = list(map(int, data))
            data = f.read()
            data = str(data).replace('\n', '\t')
            data = str(data).split('\t')
            while data.__contains__(""):
                data.remove("")
            job = list(map(int, data))
            self.job = np.array(job).reshape(m_n[0], m_n[1] * 2)
        f.close()
        self.job_num = m_n[0]
        self.machine_num = m_n[1]
        for j in range(self.job_num):
            for i in range(self.machine_num):
                self.grid.SetCellValue(j, 2 * i, str(self.job[j][2 * i]))
                self.grid.SetCellValue(j, 2 * i + 1, str(self.job[j][2 * i + 1]))

    def change_value(self, event):
        self.save_order()

    def save_order(self):
        file = open(self.path, mode='w')
        file.write(str(self.job_num) + '\t')
        file.write(str(self.machine_num))
        file.write('\n')
        for j in range(self.job_num):
            jobi = []
            for i in range(self.machine_num):
                machine = self.grid.GetCellValue(j, 2 * i)
                time = self.grid.GetCellValue(j, 2 * i + 1)
                jobi.append(machine)
                jobi.append('\t')
                jobi.append(time)
                jobi.append('\t')
            jobi.append('\n')
            file.writelines(jobi)
        file.close()