# -*- coding: utf-8 -*-

from __future__ import division

import os

from wx import aui
import wx
import wx.grid

from simulation import SimSettingPanel


class SimNotebook(aui.AuiNotebook):
    
    def __init__(self, parent=None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.model_id = 0

    def on_close(self, event):
        print("close")

    def is_new_page(self, flag=0):
        page_id = flag
        for x in range(self.GetPageCount()):
            if page_id == self.GetPage(x).GetId():
                page = self.GetPage(x)
                page.SetFocus()
                self.Refresh()
                return False
        return True

    def show_setting_page(self, title, order_path, model_path):
        page_id = hash(order_path + title) % 32000
        if self.is_new_page(page_id):
            new_panel = SimSettingPanel.SimSettingPanel(self, order_path, model_path, page_id)
            order_name = os.path.basename(order_path).split('.')[0]
            page_title = "%s: %s" % (title, order_name)
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_opt_page(self):
        if self.is_new_page(flag=1):
            print("opt")
