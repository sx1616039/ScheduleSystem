# -*- coding: utf-8 -*-

from __future__ import division

import time
import wx

from MainUI import NavTree, ShowNotebook


class OrderManagePanel(wx.Panel):
    selected_id = 0

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_model = wx.Button(calib_panel, wx.ID_ANY, u"创建订单",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_model.SetFont(font_button)
        self.btn_model.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_model, self.btn_model)

        self.btn_open = wx.Button(calib_panel, wx.ID_ANY, u"打开订单",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_open.SetFont(font_button)
        self.btn_open.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_open, self.btn_open)

        self.btn_view = wx.Button(calib_panel, wx.ID_ANY, u"修改订单",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_view.SetFont(font_button)
        self.btn_view.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_view, self.btn_view)

        self.btn_explore = wx.Button(calib_panel, wx.ID_ANY, u"删除订单",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_explore.SetFont(font_button)
        self.btn_explore.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_explore, self.btn_explore)

        self.btn_uncertain_order = wx.Button(calib_panel, wx.ID_ANY, u"不确定订单生成",
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_uncertain_order.SetFont(font_button)
        self.btn_uncertain_order.SetBitmap(wx.Bitmap('icon/data.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_explore, self.btn_uncertain_order)

        tab_sizer.Add(self.btn_model, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_open, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_view, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_explore, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_uncertain_order, 0, wx.ALL, 5)

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
            print(self.navTree.GetItemData(self.navTree.GetSelection()))
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个订单', caption='提示')
            dlg.ShowModal()
            return False
        return True

    def on_button_model(self, event):
        if self.is_selected():
            self.showNotebook.show_modeling_page()

    def on_button_open(self, event):
        if self.is_selected():
            self.showNotebook.show_opt_page()

    def on_button_view(self, event):
        if self.is_selected():
            self.showNotebook.show_view_page()

    def on_button_explore(self, event):
        if self.is_selected():
            self.showNotebook.show_explore_page()