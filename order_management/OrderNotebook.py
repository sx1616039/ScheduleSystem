# -*- coding: utf-8 -*-

from __future__ import division

import os

from wx import aui
import wx
import wx.grid
from order_management import OpenPanel, EditPanel, DeletePanel, UncertainOrderPanel
from order_management import CreatePanel


class OrderNotebook(aui.AuiNotebook):
    
    def __init__(self, parent=None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)

    def on_close(self, event):
        print("close")

    def is_new_page(self, flag=0):   # flag=0:建模；flag=1：优化；flag=2:数据生成；flag=3：试验设计
        page_id = flag
        for x in range(self.GetPageCount()):
            if page_id == self.GetPage(x).GetId():
                page = self.GetPage(x)
                page.SetFocus()
                self.Refresh()
                return False
        return True

    def show_create_page(self):
        if self.is_new_page(flag=0):
            new_panel = CreatePanel.CreatePanel(self)
            page_title = u"创建订单"
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_open_page(self, order_path):
        if self.is_new_page(flag=1):
            new_panel = OpenPanel.OpenPanel(self, order_path)
            model_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (u" 打开订单", model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_edit_page(self, order_path):
        if self.is_new_page(flag=2):
            new_panel = EditPanel.EditPanel(self, order_path)
            model_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (u" 修改订单", model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_delete_page(self, order_path):
        if self.is_new_page(flag=3):
            delete_panel = DeletePanel.DeletePanel(self, order_path)
            model_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (u" 删除订单", model_name)
            self.AddPage(delete_panel, page_title, True, wx.NullBitmap)

    def show_uncertain_order_page(self, order_path):
        if self.is_new_page(flag=4):
            uncertain_order_panel = UncertainOrderPanel.UncertainOrderPanel(self, order_path)
            model_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (u" 生成不确定订单", model_name)
            self.AddPage(uncertain_order_panel, page_title, True, wx.NullBitmap)
