# -*- coding: utf-8 -*-

from __future__ import division

import os

from wx import aui
import wx
import wx.grid
from model_management import OpenPanel, EditPanel
from model_management import CreateModelPanel


class ModelNotebook(aui.AuiNotebook):
    
    def __init__(self, parent=None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)

    def on_close(self, event):
        print("close")

    def is_new_page(self, flag=0):   # flag=0:创建模型；flag=1：查看模型；flag=2:修改模型；flag=3：删除模型
        page_id = flag
        for x in range(self.GetPageCount()):
            if page_id == self.GetPage(x).GetId():
                page = self.GetPage(x)
                page.SetFocus()
                self.Refresh()
                return False
        return True

    def show_create_page(self, title):
        if self.is_new_page(flag=0):
            new_panel = CreateModelPanel.CreateModelPanel(self)
            self.AddPage(new_panel, title, True, wx.NullBitmap)

    def show_open_page(self, title, model_path):
        if self.is_new_page(flag=1):
            new_panel = OpenPanel.OpenPanel(self, model_path)
            model_name = os.path.basename(model_path).split('.')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_edit_page(self, title, model_path):
        if self.is_new_page(flag=2):
            new_panel = EditPanel.EditPanel(self, model_path)
            model_name = os.path.basename(model_path).split('.')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

