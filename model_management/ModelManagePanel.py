# -*- coding: utf-8 -*-

from __future__ import division

import os
import shutil
import time
import wx

from MainUI import ModelTree, OrderTree
from model_management import ModelNotebook


class ModelManagePanel(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 上方按钮区域panel
        calib_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,  wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        calib_panel.SetSizer(tab_sizer)

        font_button = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False)
        self.btn_create = wx.Button(calib_panel, wx.ID_ANY, u"创建模型",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_create.SetFont(font_button)
        self.btn_create.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_create, self.btn_create)

        self.btn_open = wx.Button(calib_panel, wx.ID_ANY, u"查看模型",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_open.SetFont(font_button)
        self.btn_open.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_open, self.btn_open)

        self.btn_edit = wx.Button(calib_panel, wx.ID_ANY, u"修改模型",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_edit.SetFont(font_button)
        self.btn_edit.SetBitmap(wx.Bitmap('icon/edit.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_edit, self.btn_edit)

        self.btn_delete = wx.Button(calib_panel, wx.ID_ANY, u"删除模型",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_delete.SetFont(font_button)
        self.btn_delete.SetBitmap(wx.Bitmap('icon/delete.ico'))
        self.Bind(wx.EVT_BUTTON, self.on_button_delete, self.btn_delete)

        self.btn_import = wx.Button(calib_panel, wx.ID_ANY, u"导入",
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_import.SetFont(font_button)
        self.btn_import.SetBitmap(wx.Bitmap('icon/import.ico'))

        self.btn_export = wx.Button(calib_panel, wx.ID_ANY, u"导出",
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_export.SetFont(font_button)
        self.btn_export.SetBitmap(wx.Bitmap('icon/select.ico'))

        tab_sizer.Add(self.btn_create, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_open, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_edit, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_delete, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_import, 0, wx.ALL, 5)
        tab_sizer.Add(self.btn_export, 0, wx.ALL, 5)

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

        self.modelNotebook = ModelNotebook.ModelNotebook(show_panel)
        # show_panel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.TreePage, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.modelNotebook, 4, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(calib_panel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(show_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
        self.model_path = ''

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

    def on_button_create(self, event):
        print(self.btn_create.GetLabel())
        self.modelNotebook.show_create_page(self.btn_create.GetLabel())

    def on_button_open(self, event):
        if self.is_selected():
            self.modelNotebook.show_open_page(self.btn_open.GetLabel(), self.model_path)

    def on_button_edit(self, event):
        if self.is_selected():
            self.modelNotebook.show_edit_page(self.btn_edit.GetLabel(), self.model_path)

    def on_button_delete(self, event):
        if self.is_selected():
            dlg = wx.MessageBox("确认删除该模型？", "提示", wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
            if dlg == 4:
                shutil.rmtree(self.model_path)
                # 找到ModelManagementPanel的树结构并更新
                self.Parent.Parent.Parent.update_model_tree()
