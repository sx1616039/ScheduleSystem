# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
# import sys
# sys.path.append('E:\\pythoncode\\Uncertainty')

import wx
from ModelManage import ModelUi
from ParamModeling import ParamUi
from ModelValidate import ValidateUi
from UncertaintyPropagation import UncertaintyPropagationUi
from ModelCalibration import CalibrationPanel
from SystemManage import SystemManageUi
from ParamModeling import SpreadUi
from ParamModeling import SpeardPanel, DecisionUi
from UncertaintyValidate import UncertaintyUI

from UncertaintyPropagation import XY_Panel
import datetime


# 主界面
# noinspection PyInterpreter
class PlatformForUncertainly(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None, params={}):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"不确定性智能仿真模型校准平台",
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetIcon(wx.Icon('icon/sys.ico', wx.BITMAP_TYPE_ICO))
        self.SetSizeHints((1280, 720), wx.DefaultSize)
        self.Maximize(True)
        self.UpdateUI = UpdateUI
        self.InitUI(params)

    def InitUI(self, params):
        #         px = wx.DisplaySize()
        # 最底层panel
        self.main_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        # 最底层panel垂直布局
        bSizerforwholepanel = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(bSizerforwholepanel)

        # 右上角用户panel
        self.userPanel = wx.Panel(self.main_panel, wx.ID_ANY, wx.DefaultPosition,
                                  (200, 28), wx.TAB_TRAVERSAL)
        #         self.userPanel.SetBackgroundColour('yellow')
        # 用户显示栏
        self.userText = wx.StaticText(self.userPanel, wx.ID_ANY, params['account'],
                                      (0, 4), (-1, 28), 0)
        self.userText.SetFont(wx.Font(10.5, wx.ROMAN, wx.NORMAL, wx.NORMAL, False))
        # 注销按钮
        self.logoffBtn = wx.Button(self.userPanel, wx.ID_ANY, u"注 销",
                                   (100, 3), (-1, 26), 0)
        self.logoffBtn.SetBitmap(wx.Bitmap('icon/logoff.ico'))
        self.logoffBtn.Bind(wx.EVT_BUTTON, self.Logoff)

        # 上方导航页签
        self.statusBar = wx.Notebook(self.main_panel, wx.ID_ANY,
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.statusBar.SetPadding(wx.Size(20, 5))
        self.statusBar.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL, False))
        bSizerforwholepanel.Add(self.statusBar, 1, wx.EXPAND | wx.ALL, 5)

        # 每个页签下加入各功能模块panel
        self.model_panel = ModelUi.ModelPanel(self.statusBar)
        # self.model_panel2 = ParamUi.ParamPanel(self.statusBar)

        # self.model_panel2 = SpreadUi.SpreadPanel(self.statusBar)
        self.model_panel2 = SpeardPanel.SpreadPanel(self.statusBar)
        # self.model_panel3 = UncertaintyPropagationUi.UncertaintyPropagationPanel(self.statusBar)
        # self.model_panel3 = XY_Panel.XY_Panel(self.statusBar)

        self.model_panel4 = ValidateUi.ValidatePanel(self.statusBar)
        self.model_panel5 = CalibrationPanel.CalibrationPanel(self.statusBar)
        self.model_panel6 = SystemManageUi.SystemManegePanel(self.statusBar)
        # self.model_panel7 = DecisionUi.DecisionPanel(self.statusBar)
        self.model_panel8 = UncertaintyUI.UncertaintyPanel(self.statusBar)
        # self.welcome = wx.Panel(self.statusBar, wx.ID_ANY, wx.DefaultPosition,
        #                            wx.DefaultSize, wx.TAB_TRAVERSAL)

        self.statusBar.AddPage(self.model_panel, u"模型管理", True)
        self.statusBar.AddPage(self.model_panel2, u"建模传播", False)
        # self.statusBar.AddPage(self.model_panel3, u"不确定性传播", False)
        self.statusBar.AddPage(self.model_panel8, u"建模传播", False)
        self.statusBar.AddPage(self.model_panel4, u"验证分析", False)
        self.statusBar.AddPage(self.model_panel5, u"智能校准", False)
        self.statusBar.AddPage(self.model_panel6, u"系统管理", False)
        # self.statusBar.AddPage(self.welcome, u"欢迎使用本系统", True)

        # self.statusBar.AddPage(self.model_panel, u"模型管理", True)
        # self.statusBar.AddPage(self.model_panel2, u"数据收集", False)
        # # self.statusBar.AddPage(self.model_panel4, u"决策生成", False)
        # self.statusBar.AddPage(self.model_panel7, u"决策生成", False)
        # self.statusBar.AddPage(self.model_panel5, u"智能校准", False)
        # self.statusBar.AddPage(self.model_panel6, u"系统管理", False)

        self.main_panel.Layout()
        self.main_panel.Bind(wx.EVT_SIZE, self.OnReSize)

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在日期

        # 状态栏
        self.m_statusBar = self.CreateStatusBar()
        # 将状态栏分割为2个区域,比例为3:1
        self.m_statusBar.SetFieldsCount(2)
        self.m_statusBar.SetStatusWidths([-3, -1])
        self.m_statusBar.SetStatusText(" Version Beta 0.0.1\t", 0)
        self.m_statusBar.SetStatusText(nowTime, 1)

    #         bSizerforwholepanel.Fit(self.main_panel)

    # 欢迎页面
    # self.Welcome()

    def OnReSize(self, event):
        #       在绑定的size事件中使右上角用户panel右对齐
        x, y = self.GetSize()
        w, h = self.userPanel.GetSize()
        self.userPanel.SetPosition((x - w - 25, 0))
        self.Refresh()
        self.main_panel.Layout()

    def Logoff(self, event):
        # 注销操作
        self.Destroy()
        self.UpdateUI(0)

    def updateTree(self):
        self.model_panel.navTree.updateTree()
        self.model_panel2.navTree.updateTree()
        self.model_panel3.navTree.updateTree()
        self.model_panel4.navTree.updateTree()
        self.model_panel5.navTree.updateTree()
    #
    # # 欢迎页面
    # def Welcome(self):
    #     self.static_text_a = wx.StaticText(self.welcome, -1, label="本系统是......")
    #
    #
    #     box_sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
    #     box_sizer_a.Add(self.static_text_a)
    #
    #
    #
    #     box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
    #     box_sizer.Add(box_sizer_a)
    #
    #     self.welcome.SetSizer(box_sizer)
    #     self.Show(True)
    #     self.welcome.Layout()
    #     self.statusBar.DeletePage(self.statusBar.GetCurrentPage())


class MainApp(wx.App):
    def OnInit(self):
        self.frame = PlatformForUncertainly(params={"account": 'admin'})
        self.frame.Show()
        return True


def main():
    app = MainApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
