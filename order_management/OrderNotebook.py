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

    def show_create_page(self, title):
        if self.is_new_page(0):
            new_panel = CreatePanel.CreatePanel(self)
            page_title = u"创建订单"
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_open_page(self, order_path, title):
        page_id = hash(order_path+title) % 32000
        if self.is_new_page(page_id):
            new_panel = OpenPanel.OpenPanel(self, order_path, page_id)
            model_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_edit_page(self, order_path, title):
        page_id = hash(order_path+title) % 32000
        if self.is_new_page(page_id):
            new_panel = EditPanel.EditPanel(self, order_path, page_id)
            model_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_delete_page(self, order_path, title):
        page_id = hash(order_path+title) % 32000
        if self.is_new_page(page_id):
            delete_panel = DeletePanel.DeletePanel(self, order_path, page_id)
            model_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(delete_panel, page_title, True, wx.NullBitmap)

    def show_uncertain_order_page(self, order_path, title):
        page_id = hash(order_path+title) % 32000
        if self.is_new_page(page_id):
            uncertain_order_panel = UncertainOrderPanel.UncertainOrderPanel(self, order_path, page_id)
            model_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(uncertain_order_panel, page_title, True, wx.NullBitmap)
