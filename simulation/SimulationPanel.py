# -*- coding: utf-8 -*-

from __future__ import division

import os
import time
import wx

from MainUI import OrderTree, ModelTree
from simulation import SimNotebook


class SimulationPanel(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_setting = wx.Button(calib_panel, wx.ID_ANY, u"仿真设置",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_setting.SetFont(font_button)
        self.btn_setting.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_setting, self.btn_setting)

        self.btn_run = wx.Button(calib_panel, wx.ID_ANY, u"运行",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_run.SetFont(font_button)
        self.btn_run.SetBitmap(wx.Bitmap('icon/run.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_run, self.btn_run)

        self.btn_suspend = wx.Button(calib_panel, wx.ID_ANY, u"暂停",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_suspend.SetFont(font_button)
        self.btn_suspend.SetBitmap(wx.Bitmap('icon/optimize.ico'))

        self.btn_end = wx.Button(calib_panel, wx.ID_ANY, u"结束",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_end.SetFont(font_button)
        self.btn_end.SetBitmap(wx.Bitmap('icon/quit.ico'))

        tab_sizer.Add(self.btn_setting, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_run, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_suspend, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_end, 0, wx.ALL, 5)

        # 下方导航树及展示界面panel
        show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.TreePage = wx.Notebook(show_panel, wx.ID_ANY,
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.TreePage.SetPadding(wx.Size(20, 5))
        self.TreePage.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL, False))
        self.order_tree = OrderTree.OrderTree(self.TreePage)
        self.model_tree = ModelTree.ModelTree(self.TreePage)
        self.TreePage.AddPage(self.order_tree, u"订单", True)
        self.TreePage.AddPage(self.model_tree, u"模型", False)

        self.simNotebook = SimNotebook.SimNotebook(show_panel)
        # show_panel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.TreePage, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.simNotebook, 4, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(calib_panel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
        self.order_path = ''
        self.model_path = ''

    def is_selected(self):
        try:
            self.order_path = self.order_tree.GetItemData(self.order_tree.GetSelection())
            print(self.order_path)
            if os.path.exists(self.order_path):
                self.model_path = self.model_tree.GetItemData(self.model_tree.GetSelection())
                return True
        except:
            dlg = wx.MessageDialog(None, message='请选择订单和模型', caption='提示')
            dlg.ShowModal()
            return False

    def on_button_setting(self, event):
        if self.is_selected():
            self.simNotebook.show_setting_page(self.btn_setting.GetLabel(), self.order_path, self.model_path)

    def on_button_run(self, event):
        if self.is_selected():
            self.simNotebook.show_opt_page()
