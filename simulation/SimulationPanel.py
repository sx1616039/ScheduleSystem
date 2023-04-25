# -*- coding: utf-8 -*-

from __future__ import division

import os
import time
import wx

from MainUI import NavTree
from simulation import SimNotebook


class SimulationPanel(wx.Panel):
    selected_id = 0

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_model = wx.Button(calib_panel, wx.ID_ANY, u"仿真设置",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_model.SetFont(font_button)
        self.btn_model.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_model, self.btn_model)

        self.btn_opt = wx.Button(calib_panel, wx.ID_ANY, u"运行",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_opt.SetFont(font_button)
        self.btn_opt.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_opt, self.btn_opt)

        tab_sizer.Add(self.btn_model, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_opt, 0, wx.ALL, 5)

        # 下方导航树及展示界面panel
        tree_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = NavTree.NavTree(tree_panel)
        self.simNotebook = SimNotebook.SimNotebook(tree_panel)

        # tree_panel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.navTree, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.simNotebook, 4, wx.EXPAND | wx.ALL, 5)
        tree_panel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(calib_panel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(tree_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
        self.order_path = ''

    def is_selected(self):
        try:
            print(self.navTree.GetItemData(self.navTree.GetSelection()))
            if os.path.exists(self.navTree.GetItemData(self.navTree.GetSelection())):
                self.order_path = self.navTree.GetItemData(self.navTree.GetSelection())
                return True
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个仿真模型', caption='warning')
            dlg.ShowModal()
            return False
        return True

    def on_button_model(self, event):
        if self.is_selected():
            self.simNotebook.show_modeling_page()

    def on_button_opt(self, event):
        if self.is_selected():
            self.simNotebook.show_opt_page()

    def on_button_view(self, event):
        if self.is_selected():
            self.simNotebook.show_view_page()

    def on_button_explore(self, event):
        if self.is_selected():
            self.simNotebook.show_explore_page()
