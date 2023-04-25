#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx import aui
import sys
from wx.lib.mixins.listctrl import TextEditMixin


class TreeNotebook(aui.AuiNotebook):

    def __init__(self, parent=None):

        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    def RunModel(self, id):
        flag = 0
        for x in range(self.GetPageCount()):
            if 3 == self.GetPage(x).GetId():
                self.GetPage(x).SetFocus()
                self.Refresh()
                flag = 1
                return

    def OnReSize(self, event, show_panel):
        show_panel.Layout()
#         在绑定的size事件中使右下角保存panel右对齐
        x, y = show_panel.btmPanel.GetSize()
        w, h = show_panel.savePanel.GetSize()
        show_panel.savePanel.SetPosition((x - w - 25, y - h - 5))
        show_panel.Layout()

    # 点击导入模型事件
    def ClickImport(self, event):
        show_panel = self.GetCurrentPage()
        proj_name = show_panel.textCtrl1.GetValue()
        if proj_name == '':
            return
        proj_descr = show_panel.textCtrl2.GetValue()
        record = []
        if record != []:
            show_panel.staticText3.Show(show=True)
            show_panel.Layout()
            return
        show_panel.staticText3.Show(show=False)
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            show_panel.dir_text.SetValue(dlg.GetPath())
            show_panel.dir_text.Disable()
            show_panel.textCtrl1.Disable()  # 导入成功后控件变为不可编辑
            show_panel.textCtrl2.Disable()
            show_panel.button1.Disable()
            self.GetParent().GetParent().navTree.updateTree()
        dlg.Destroy()

    # 生成输出参数表
    def OutputManage(self, event):
        show_panel = self.GetCurrentPage()
        num = show_panel.output_var.GetValue()
        if num.isdigit() == True:
            show_panel.outputform.ClearAll()
            show_panel.outputform.InsertColumn(0, '变量名', width=240)
            show_panel.outputform.InsertColumn(1, '描述', width=240)
            #   show_panel.outputform.InsertColumn(2, '初始值', width=160)
            for i in range(int(num)):
                index = show_panel.outputform.InsertItem(sys.maxint, u'y' + str(i + 1))
                show_panel.outputform.SetItem(index, 1, u'输出' + str(i + 1))
            show_panel.outputform.make_editor()

    # 保存更新设置
    def SaveUpdate(self, event):
        show_panel = self.GetCurrentPage()
        proj_name = show_panel.textCtrl1.GetValue()
        if proj_name == '':
            return
        proj_descr = show_panel.textCtrl2.GetValue()
        old_id = show_panel.old_id

    # 保存新建设置
    def SaveNew(self, event):
        try:
            show_panel = self.GetCurrentPage()
            model_id = show_panel.model_id
            inputform = show_panel.inputform
            outputform = show_panel.outputform
            varsform = show_panel.varsform
            inputargs = []
            vars = []
            outputargs = []
            """保存输入参数信息到inputargs"""
            for i in range(inputform.GetItemCount()):
                temp = []
                for j in range(3):
                    temp.append(inputform.GetItemText(i, j))
                inputargs.append(temp)
    
            """保存自变量信息到vars"""
            for i in range(varsform.GetItemCount()):
                temp = []
                for j in range(3):
                    temp.append(varsform.GetItemText(i, j))
                temp.append(0)
                vars.append(temp)

            self.DeletePage(self.GetPageIndex(show_panel))
            self.Refresh()
            # 找到最高层MainUI的Frame
            self.Parent.Parent.Parent.Parent.Parent.updateTree()
        except Exception as e:
            dlg = wx.MessageBox("请先导入模型", "提示" ,wx.OK | wx.ICON_INFORMATION)


    # 关闭
    def Cancel(self, event):
        show_panel = self.GetCurrentPage()
        self.DeletePage(self.GetPageIndex(show_panel))
        self.Refresh()

    # 仿真运行
    def TryRun(self, event):
        show_panel = self.GetCurrentPage()
        model_id = show_panel.old_id
        inputform = show_panel.inputform
        varsform = show_panel.varsform
        outputform = show_panel.outputform
        inputargs = []
        vars = []
        """保存输入参数信息到inputargs"""
        for i in range(inputform.GetItemCount()):
            inputargs.append(float(inputform.GetItemText(i, 2)))

        """保存自变量信息到vars"""
        for i in range(varsform.GetItemCount()):
            vars.append(float(varsform.GetItemText(i, 2)))

        show_panel.Refresh()
        # self.DeletePage(self.GetPageIndex(show_panel))
        # self.Refresh()


class EditMixin(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)