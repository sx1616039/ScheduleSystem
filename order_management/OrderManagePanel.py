# -*- coding: utf-8 -*-

from __future__ import division

import os
import time
import wx

from MainUI import OrderTree, ModelTree
from order_management import OrderNotebook


class OrderManagePanel(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_create = wx.Button(calib_panel, wx.ID_ANY, u"创建订单",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_create.SetFont(font_button)
        self.btn_create.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_create, self.btn_create)

        self.btn_open = wx.Button(calib_panel, wx.ID_ANY, u"打开订单",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_open.SetFont(font_button)
        self.btn_open.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_open, self.btn_open)

        self.btn_edit = wx.Button(calib_panel, wx.ID_ANY, u"修改订单",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_edit.SetFont(font_button)
        self.btn_edit.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_edit, self.btn_edit)

        self.btn_delete = wx.Button(calib_panel, wx.ID_ANY, u"删除订单",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_delete.SetFont(font_button)
        self.btn_delete.SetBitmap(wx.Bitmap('icon/delete.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_delete, self.btn_delete)

        self.btn_uncertain_order = wx.Button(calib_panel, wx.ID_ANY, u"生成不确定订单",
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_uncertain_order.SetFont(font_button)
        self.btn_uncertain_order.SetBitmap(wx.Bitmap('icon/data.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_uncertain_order, self.btn_uncertain_order)

        tab_sizer.Add(self.btn_create, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_open, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_edit, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_delete, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_uncertain_order, 0, wx.ALL, 5)

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

        self.orderNotebook = OrderNotebook.OrderNotebook(show_panel)
        # show_panel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.TreePage, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.orderNotebook, 4, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(calib_panel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
        self.order_path = ''

    def is_selected(self):
        try:
            if not os.path.isdir(self.order_tree.GetItemData(self.order_tree.GetSelection())):
                print(self.order_tree.GetItemData(self.order_tree.GetSelection()))
                self.order_path = self.order_tree.GetItemData(self.order_tree.GetSelection())
                return True
            else:
                dlg = wx.MessageDialog(None, message='请先选择一个订单', caption='提示')
                dlg.ShowModal()
                return False
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个订单', caption='提示')
            dlg.ShowModal()
            return False

    def on_button_create(self, event):
        self.orderNotebook.show_create_page()

    def on_button_open(self, event):
        if self.is_selected():
            self.orderNotebook.show_open_page(self.order_path)

    def on_button_edit(self, event):
        if self.is_selected():
            self.orderNotebook.show_edit_page(self.order_path)

    def on_button_delete(self, event):
        if self.is_selected():
            self.orderNotebook.show_delete_page(self.order_path)

    def on_button_uncertain_order(self, event):
        if os.path.exists(self.order_tree.GetItemData(self.order_tree.GetSelection())):
            self.orderNotebook.show_uncertain_order_page(self.order_tree.GetItemData(self.order_tree.GetSelection()))
