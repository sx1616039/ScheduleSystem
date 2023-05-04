# -*- coding: utf-8 -*-

from __future__ import division

import os
import time
import wx

from MainUI import OrderTree, ModelTree
from model_training import TrainNotebook


class TrainPanel(wx.Panel):
    selected_id = 0

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_gen_data = wx.Button(calib_panel, wx.ID_ANY, u"训练数据生成",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_gen_data.SetFont(font_button)
        self.btn_gen_data.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_gen_data, self.btn_gen_data)

        self.btn_settings = wx.Button(calib_panel, wx.ID_ANY, u"参数设置",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_settings.SetFont(font_button)
        self.btn_settings.SetBitmap(wx.Bitmap('icon/setting.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_setting, self.btn_settings)

        self.button_analyze = wx.Button(calib_panel, wx.ID_ANY, u"结果分析",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_analyze.SetFont(font_button)
        self.button_analyze.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_analyze, self.button_analyze)

        tab_sizer.Add(self.btn_gen_data, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_settings, 0, wx.ALL, 5)
        tab_sizer.Add(self.button_analyze, 0, wx.ALL, 5)

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

        self.trainNotebook = TrainNotebook.TrainNotebook(show_panel)
        # show_panel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.TreePage, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.trainNotebook, 4, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(calib_panel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
        self.model_path = ''

    def is_selected(self):
        try:
            print(self.model_tree.GetItemData(self.model_tree.GetSelection()))
            if os.path.exists(self.model_tree.GetItemData(self.model_tree.GetSelection())):
                self.model_path = self.model_tree.GetItemData(self.model_tree.GetSelection())
                return True
            else:
                return False
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个调度模型', caption='提示')
            dlg.ShowModal()
            return False

    def on_button_gen_data(self, event):
        self.trainNotebook.show_gen_data_page(self.btn_gen_data.GetLabel())

    def on_button_setting(self, event):
        if self.is_selected():
            self.trainNotebook.show_setting_page(self.btn_settings.GetLabel(), self.model_path)

    def on_button_analyze(self, event):
        if self.is_selected():
            self.trainNotebook.show_analyze_page(self.button_analyze.GetLabel(), self.model_path)
