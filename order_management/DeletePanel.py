# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os
import wx.xrc
import wx.lib.newevent
import numpy as np


class DeletePanel(wx.Panel):

    def __init__(self, parent, order_path=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.path = order_path
        # 表格
        grid_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        ''' 删除订单按钮 '''
        btn_delete = wx.Button(grid_panel, wx.ID_ANY, u"删除订单", wx.DefaultPosition, wx.Size(100, 26), 0)
        btn_delete.SetBitmap(wx.Bitmap('icon/delete.ico'))
        btn_delete.Bind(wx.EVT_BUTTON, self.on_button_delete)

        self.grid = wx.grid.Grid(grid_panel, id=wx.ID_ANY, size=(900, 500))
        # 创建一个100X50的电子表格
        self.grid.CreateGrid(100, 50 * 2)
        self.grid.EnableEditing(False)

        grid_box = wx.BoxSizer(wx.VERTICAL)
        grid_box.Add(btn_delete, 0, wx.EXPAND | wx.ALL, 10)
        grid_box.Add(self.grid, 0, wx.EXPAND | wx.ALL, 0)
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

    def on_button_delete(self, event):
        dlg = wx.MessageBox("确认删除该订单", "提示", wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
        if dlg == 4:
            os.remove(self.path)
            # 找到OrderManagementPanel的树结构并更新
            self.Parent.Parent.Parent.order_tree.updateTree()
            for j in range(self.job_num):
                for i in range(self.machine_num):
                    self.grid.SetCellValue(j, 2 * i, '')
                    self.grid.SetCellValue(j, 2 * i + 1, '')
