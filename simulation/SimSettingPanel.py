# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os
import wx.xrc
import wx.lib.newevent
import random
import numpy as np
import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element


class SimSettingPanel(wx.Panel):

    def __init__(self, parent, order_path, model_path, page_id):
        wx.Panel.__init__(self, parent, page_id, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.model_path = model_path
        ''' 第一行：订单路径按钮 '''
        file_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_file_name = wx.StaticText(file_panel, wx.ID_ANY, u"订单路径:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_file_path = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25), style=wx.TE_LEFT)
        self.text_file_path.AppendText(order_path)
        btn_select_order = wx.Button(file_panel, wx.ID_ANY, u"选择", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_select_order.Bind(wx.EVT_BUTTON, self.on_button_select_order)

        ''' 运行按钮 '''
        btn_save = wx.Button(file_panel, wx.ID_ANY, u"运行", wx.DefaultPosition, wx.Size(100, 26), 0)
        btn_save.SetBitmap(wx.Bitmap('icon/run.ico'))
        btn_save.Bind(wx.EVT_BUTTON, self.on_button_run)

        order_sizer = wx.BoxSizer(wx.HORIZONTAL)
        order_sizer.Add(label_file_name, 0, wx.ALL, 7)
        order_sizer.Add(self.text_file_path, 5, wx.ALL, 5)
        order_sizer.Add(btn_select_order, 1, wx.ALL, 5)
        order_sizer.Add(btn_save, 1, wx.ALL, 5)
        file_panel.SetSizer(order_sizer)

        self.model_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_model_type = wx.StaticText(self.model_panel, wx.ID_ANY, u"调度模型：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.model_type = ['PDR', 'DRL']
        self.combobox_model_type = wx.ComboBox(self.model_panel, -1, size=wx.Size(100, -1),
                                               choices=self.model_type)
        self.combobox_model_type.SetSelection(0)
        self.combobox_model_type.Bind(wx.EVT_COMBOBOX, self.on_select_combobox_model)
        self.PDR_type = ['None', 'SPT', 'MWKR', 'FDD/MWKR', 'MOPNR', 'LRM ', 'FIFO ',
                                 'LPT', 'LWKR', 'FDD/LWKR', 'LOPNR', 'SRM ', 'FILO ']
        self.combobox_PDR_type = wx.ComboBox(self.model_panel, -1, size=wx.Size(100, -1),
                                               choices=self.PDR_type)
        self.combobox_PDR_type.SetSelection(1)

        label_path = wx.StaticText(self.model_panel, wx.ID_ANY, u"模型路径：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_model_path = wx.TextCtrl(self.model_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25),
                                           style=wx.TE_LEFT)
        self.text_model_path.AppendText(self.model_path)
        ''' 选择路径按钮 '''
        btn_select_model = wx.Button(self.model_panel, wx.ID_ANY, u"选择", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_select_model.Bind(wx.EVT_BUTTON, self.on_button_select_model)

        self.model_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.model_sizer.Add(label_model_type, 0, wx.ALL, 7)
        self.model_sizer.Add(self.combobox_model_type, 1, wx.ALL, 5)
        self.model_sizer.Add(self.combobox_PDR_type, 1, wx.ALL, 5)
        self.model_sizer.Add(label_path, 0, wx.ALL, 7)
        self.model_sizer.Add(self.text_model_path, 5, wx.ALL, 5)
        self.model_sizer.Add(btn_select_model, 1, wx.ALL, 5)
        self.model_panel.SetSizer(self.model_sizer)

        # main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(file_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.model_panel, 0, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def on_button_select_order(self, event):
        dlg = wx.FileDialog(self, u"选择订单", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_file_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_button_select_model(self, event):
        dlg = wx.FileDialog(self, u"选择模型", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_model_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_select_combobox_model(self, event):
        pos = self.combobox_model_type.GetSelection()
        if pos == 0:
            self.combobox_PDR_type.SetSelection(1)
        else:
            self.combobox_PDR_type.SetSelection(0)

    def on_button_run(self, event):
        print("opt")
