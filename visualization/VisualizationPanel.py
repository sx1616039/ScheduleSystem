# -*- coding: utf-8 -*-

from __future__ import division

import time
import wx
import NavTree
import ShowNotebook


class VisualizationPanel(wx.Panel):
    selected_id = 0

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_model = wx.Button(calib_panel, wx.ID_ANY, u"回报分析",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_model.SetFont(font_button)
        self.btn_model.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_model, self.btn_model)

        self.btn_opt = wx.Button(calib_panel, wx.ID_ANY, u"时间对比",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_opt.SetFont(font_button)
        self.btn_opt.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_opt, self.btn_opt)

        self.btn_view = wx.Button(calib_panel, wx.ID_ANY, u"收敛性分析",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_view.SetFont(font_button)
        self.btn_view.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_view, self.btn_view)

        self.btn_explore = wx.Button(calib_panel, wx.ID_ANY, u"结果对比",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_explore.SetFont(font_button)
        self.btn_explore.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_explore, self.btn_explore)

        tab_sizer.Add(self.btn_model, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_opt, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_view, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_explore, 0, wx.ALL, 5)

        # 下方导航树及展示界面panel
        tree_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = NavTree.NavTree(tree_panel)
        self.showNotebook = ShowNotebook.ShowNotebook(tree_panel)

        # tree_panel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.navTree, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.showNotebook, 4, wx.EXPAND | wx.ALL, 5)
        tree_panel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(calib_panel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(tree_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)

    def is_selected(self):
        try:
            '''获取校准模型的id'''
            CalibrationPanel.selected_id = self.navTree.GetItemData(self.navTree.GetSelection())
            if CalibrationPanel.selected_id == 0 or CalibrationPanel.selected_id == 1: # 区分各个节点
                raise NameError('...')
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个仿真模型', caption='warning')
            dlg.ShowModal()
            return False
        return True

    def on_button_model(self, event):
        if self.is_selected():
            self.showNotebook.show_modeling_page()

    def on_button_opt(self, event):
        if self.is_selected():
            self.showNotebook.show_opt_page()

    def on_button_view(self, event):
        if self.is_selected():
            self.showNotebook.show_view_page()

    def on_button_explore(self, event):
        if self.is_selected():
            self.showNotebook.show_explore_page()
