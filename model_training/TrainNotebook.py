# -*- coding: utf-8 -*-

from __future__ import division

import os

from wx import aui
import wx
import wx.grid

from model_training import GenDataPanel, SettingPanel, AnalyzePanel


class TrainNotebook(aui.AuiNotebook):
    
    def __init__(self, parent=None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.model_id = 0

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

    def show_gen_data_page(self, title):
        if self.is_new_page(flag=1):
            new_panel = GenDataPanel.GenDataPanel(self)
            self.AddPage(new_panel, title, True, wx.NullBitmap)

    def show_setting_page(self, title, model_path):
        if self.is_new_page(flag=1):
            new_panel = SettingPanel.SettingPanel(self, model_path)
            model_name = os.path.basename(model_path).split('.')[0]
            page_title = "%s: %s" % (title, model_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_analyze_page(self, title, model_path):
        if self.is_new_page(flag=1):
            new_panel = AnalyzePanel.AnalyzePanel(self, model_path)
            self.AddPage(new_panel, title, True, wx.NullBitmap)
