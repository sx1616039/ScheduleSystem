# -*- coding: utf-8 -*-

from __future__ import division
from wx import aui
import wx
import wx.grid


class OptNotebook(aui.AuiNotebook):
    
    def __init__(self, parent=None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.model_id = 0

    def on_close(self, event):
        self.model_id = 0
        cp.CalibrationPanel.selected_id = 0

    def is_new_page(self, flag=0):   # flag=0:建模；flag=1：优化；flag=2:数据生成；flag=3：试验设计
        self.model_id = self.GetParent().GetParent().navTree.GetItemData(
            self.GetParent().GetParent().navTree.GetSelection())
        # set the relation between page_id and model_id or opt_id
        # model_page_id = model_id * 4 -0 and opt_page_id = model_id *4-1
        # gen_data_page_id = model_id * 4 -2 and explore_page_id = model_id *4-3
        page_id = self.model_id * 4 - flag
        for x in range(self.GetPageCount()):
            if page_id == self.GetPage(x).GetId():
                page = self.GetPage(x)
                page.SetFocus()
                self.Refresh()
                return False
        return True

    def get_model_name(self):
        return Sql.selectSql(args=(self.model_id,), sql=Sql.selectModel)

    def show_modeling_page(self):
        if self.is_new_page(flag=0):
            new_panel = MetaPanel.MetaPanel(self, self.model_id)
            model_name = self.get_model_name()
            page_title = "%s%s" % (model_name[0][0], u" 建模")
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_opt_page(self):
        if self.is_new_page(flag=1):
            new_panel = OptPanel.OptPanel(self, self.model_id)
            model_name = self.get_model_name()
            page_title = "%s%s" % (model_name[0][0], u" 优化")
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_view_page(self):
        if self.is_new_page(flag=2):
            new_panel = ModelReviewPanel.ModelReviewPanel(self, self.model_id)
            model_name = self.get_model_name()
            page_title = "%s%s" % (model_name[0][0], u" 仿真模型")
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)

    def show_explore_page(self):
        if self.is_new_page(flag=3):
            new_panel = ExplorePanel.ExplorePanel(self, self.model_id)
            model_name = self.get_model_name()
            page_title = "%s%s" % (model_name[0][0], u" 试验设计")
            self.AddPage(new_panel, page_title, True, wx.NullBitmap)
