# -*- coding: utf-8 -*-

from __future__ import division

import os
import time
import wx

from MainUI import OrderTree, ModelTree
from model_optimization import OptNotebook


class OptPanel(wx.Panel):
    selected_id = 0

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_setting = wx.Button(calib_panel, wx.ID_ANY, u"优化设置",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_setting.SetFont(font_button)
        self.btn_setting.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_setting, self.btn_setting)

        self.btn_opt = wx.Button(calib_panel, wx.ID_ANY, u"结果分析",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_opt.SetFont(font_button)
        self.btn_opt.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_opt, self.btn_opt)

        tab_sizer.Add(self.btn_setting, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_opt, 0, wx.ALL, 5)

        # 下方导航树及展示界面panel
        show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.TreePage = wx.Notebook(show_panel, wx.ID_ANY,
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.TreePage.SetPadding(wx.Size(20, 5))
        self.TreePage.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL, False))
        self.order_tree = OrderTree.OrderTree(self.TreePage)
        self.model_tree = ModelTree.ModelTree(self.TreePage)
        self.TreePage.AddPage(self.order_tree, u"订单", False)
        self.TreePage.AddPage(self.model_tree, u"模型", True)

        self.optNotebook = OptNotebook.OptNotebook(show_panel)
        # show_panel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.TreePage, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.optNotebook, 4, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(calib_panel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
        self.order_path = ''

    def is_selected(self):
        print(self.model_tree.GetItemData(self.model_tree.GetSelection()))
        try:
            if os.path.isdir(self.model_tree.GetItemData(self.model_tree.GetSelection())):
                print(self.model_tree.GetItemData(self.model_tree.GetSelection()))
                self.model_path = self.model_tree.GetItemData(self.model_tree.GetSelection())
                return True
            else:
                dlg = wx.MessageDialog(None, message='请先选择一个模型', caption='提示')
                dlg.ShowModal()
                return False
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个模型', caption='提示')
            dlg.ShowModal()
            return False

    def on_button_setting(self, event):
        if self.is_selected():
            self.optNotebook.show_setting_page(self.btn_setting.GetLabel(), self.model_path)

    def on_button_opt(self, event):
        if self.is_selected():
            self.optNotebook.show_opt_page(self.btn_opt.GetLabel(), self.model_path)

