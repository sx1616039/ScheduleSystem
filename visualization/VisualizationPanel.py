# -*- coding: utf-8 -*-

from __future__ import division

import os
import time
import wx

from MainUI import OrderTree, ModelTree
from visualization import ShowNotebook


class VisualizationPanel(wx.Panel):
    selected_id = 0

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_reward_analysis = wx.Button(calib_panel, wx.ID_ANY, u"回报分析",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_reward_analysis.SetFont(font_button)
        self.btn_reward_analysis.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_reward_analysis, self.btn_reward_analysis)

        self.btn_time_analysis = wx.Button(calib_panel, wx.ID_ANY, u"时间对比",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_time_analysis.SetFont(font_button)
        self.btn_time_analysis.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_time_analysis, self.btn_time_analysis)

        self.btn_conv_analysis = wx.Button(calib_panel, wx.ID_ANY, u"收敛性分析",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_conv_analysis.SetFont(font_button)
        self.btn_conv_analysis.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_conv_analysis, self.btn_conv_analysis)

        self.btn_results = wx.Button(calib_panel, wx.ID_ANY, u"结果对比",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_results.SetFont(font_button)
        self.btn_results.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_results, self.btn_results)

        tab_sizer.Add(self.btn_reward_analysis, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_time_analysis, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_conv_analysis, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_results, 0, wx.ALL, 5)

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

        self.showNotebook = ShowNotebook.ShowNotebook(show_panel)
        # show_panel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.TreePage, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.showNotebook, 4, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(calib_panel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
        self.order_path = ''

    def is_selected(self):
        try:
            print(self.order_tree.GetItemData(self.order_tree.GetSelection()))
            if os.path.exists(self.order_tree.GetItemData(self.order_tree.GetSelection())):
                self.order_path = self.order_tree.GetItemData(self.order_tree.GetSelection())
                return True
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个仿真模型', caption='提示')
            dlg.ShowModal()
            return False
        return True

    def on_button_reward_analysis(self, event):
        if self.is_selected():
            self.showNotebook.show_modeling_page()

    def on_button_time_analysis(self, event):
        if self.is_selected():
            self.showNotebook.show_opt_page()

    def on_button_conv_analysis(self, event):
        if self.is_selected():
            self.showNotebook.show_view_page()

    def on_button_results(self, event):
        if self.is_selected():
            self.showNotebook.show_explore_page()
