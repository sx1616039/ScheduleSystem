# -*- coding: utf-8 -*-

from __future__ import division

import os

from wx import aui
import wx
import wx.grid

from model_optimization import OptSettingPanel, ShowPanel


class OptNotebook(aui.AuiNotebook):
    
    def __init__(self, parent=None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.model_id = 0

    def on_close(self, event):
        print('close')

    def is_new_page(self, page_id):   # flag=0:参数设置；flag=1：优化；
        page_id = page_id
        for x in range(self.GetPageCount()):
            print(self.GetPage(x).GetId())
            if page_id == self.GetPage(x).GetId():
                page = self.GetPage(x)
                page.SetFocus()
                self.Refresh()
                return False
        return True

    def show_setting_page(self, title, model_path):
        page_id = hash(model_path) % 32000
        if self.is_new_page(page_id):
            new_panel = OptSettingPanel.OptSettingPanel(self, model_path, page_id)
            model_name = os.path.basename(model_path).split('\\')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_opt_page(self, title, model_path):
        page_id = hash(model_path) % 32000
        if self.is_new_page(page_id):
            new_panel = ShowPanel.ShowPanel(self, model_path, page_id)
            model_name = os.path.basename(model_path).split('\\')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)
