# -*- coding: utf-8 -*-

import wx
import datetime

from MainUI import OrderManagePanel, TrainPanel, VisualizationPanel, OptPanel
from MainUI.NavTree import NavTree
from  ShowNotebook import ShowNotebook


class SchedulingSystem(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None, params=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"不确定条件下生产线智能调度平台",
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.APP_FILE_EXIT = 0
        self.APP_FILE_OPEN = 1
        self.APP_EDIT_CUT = 10
        self.APP_EDIT_COPY = 11
        self.APP_EDIT_PASTE = 12
        self.APP_ORDER_CREATE = 20
        self.APP_ORDER_OPEN = 21
        self.APP_RUN = 30
        self.APP_RUN_CONFIG = 31
        self.APP_TRAIN_CONFIG = 40
        self.APP_OPT_CONFIG = 50
        self.APP_VISUAL_REWARD = 60

        self.main_panel = None
        self.statusBar = None
        if params is None:
            params = {}
        self.SetIcon(wx.Icon('icon/sys.ico', wx.BITMAP_TYPE_ICO))
        self.SetSizeHints((1280, 720), wx.DefaultSize)
        self.Maximize(True)
        self.UpdateUI = UpdateUI
        self.init_ui(params)

    def init_ui(self, params):
        # 最底层panel
        self.main_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        # # 整个模块布局,最底层panel垂直布局
        main_layout = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(main_layout)

        # 右上角用户panel
        self.userPanel = wx.Panel(self.main_panel, wx.ID_ANY, wx.DefaultPosition,
                                  (200, 28), wx.TAB_TRAVERSAL)
        #         self.userPanel.SetBackgroundColour('yellow')
        # 用户显示栏
        self.userText = wx.StaticText(self.userPanel, wx.ID_ANY, "Administrator",
                                      (0, 4), (-1, 28), 0)
        self.userText.SetFont(wx.Font(10.5, wx.ROMAN, wx.NORMAL, wx.NORMAL, False))
        # 注销按钮
        self.logoffBtn = wx.Button(self.userPanel, wx.ID_ANY, u"注 销",
                                   (100, 3), (-1, 26), 0)
        self.logoffBtn.SetBitmap(wx.Bitmap('icon/logoff.ico'))
        self.logoffBtn.Bind(wx.EVT_BUTTON, self.Logoff)

        # 上方导航页签
        self.NaviPage = wx.Notebook(self.main_panel, wx.ID_ANY,
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.NaviPage.SetPadding(wx.Size(20, 5))
        self.NaviPage.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL, False))
        main_layout.Add(self.NaviPage, 1, wx.EXPAND | wx.ALL, 5)

        # 每个页签下加入各功能模块panel
        self.panel_order_management = OrderManagePanel.OrderManagePanel(self.NaviPage)
        self.panel_train = TrainPanel.TrainPanel(self.NaviPage)
        self.panel_opt = OptPanel.OptPanel(self.NaviPage)
        self.panel_visualization = VisualizationPanel.VisualizationPanel(self.NaviPage)

        self.NaviPage.AddPage(self.panel_order_management, u"订单管理", True)
        self.NaviPage.AddPage(self.panel_train, u"模型训练", False)
        self.NaviPage.AddPage(self.panel_opt, u"模型优化", False)
        self.NaviPage.AddPage(self.panel_visualization, u"可视化", False)

        # 状态栏
        self.status_bar = self.CreateStatusBar()
        # 将状态栏分割为2个区域,比例为3:1
        self.status_bar.SetFieldsCount(2)
        self.status_bar.SetStatusWidths([-3, -1])
        self.status_bar.SetStatusText(" Version Beta 0.0.1\t", 0)
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在日期
        self.status_bar.SetStatusText(nowTime, 1)

        self.main_panel.Layout()
        self.main_panel.Bind(wx.EVT_SIZE, self.OnReSize)
        self.Show(True)  # 显示框架

    def OnQuit(self, e):  # 自定义函数　响应菜单项　　
        self.Close()


        # 每个页签下加入各功能模块panel
        # self.model_panel = ModelUi.ModelPanel(self.statusBar)
        # # self.model_panel2 = ParamUi.ParamPanel(self.statusBar)
        #
        # # self.model_panel2 = SpreadUi.SpreadPanel(self.statusBar)
        # self.model_panel2 = SpeardPanel.SpreadPanel(self.statusBar)
        # # self.model_panel3 = UncertaintyPropagationUi.UncertaintyPropagationPanel(self.statusBar)
        # # self.model_panel3 = XY_Panel.XY_Panel(self.statusBar)
        #
        # self.model_panel4 = ValidateUi.ValidatePanel(self.statusBar)
        # self.model_panel5 = CalibrationPanel.CalibrationPanel(self.statusBar)
        # self.model_panel6 = SystemManageUi.SystemManegePanel(self.statusBar)
        # # self.model_panel7 = DecisionUi.DecisionPanel(self.statusBar)
        # self.model_panel8 = UncertaintyUI.UncertaintyPanel(self.statusBar)
        # self.welcome = wx.Panel(self.statusBar, wx.ID_ANY, wx.DefaultPosition,
        #                            wx.DefaultSize, wx.TAB_TRAVERSAL)

        # self.statusBar.AddPage(self.model_panel, u"模型管理", True)
        # self.statusBar.AddPage(self.model_panel2, u"建模传播", False)
        # # self.statusBar.AddPage(self.model_panel3, u"不确定性传播", False)
        # self.statusBar.AddPage(self.model_panel8, u"建模传播", False)
        # self.statusBar.AddPage(self.model_panel4, u"验证分析", False)
        # self.statusBar.AddPage(self.model_panel5, u"智能校准", False)
        # self.statusBar.AddPage(self.model_panel6, u"系统管理", False)
        # # self.statusBar.AddPage(self.welcome, u"欢迎使用本系统", True)

        # self.statusBar.AddPage(self.model_panel, u"模型管理", True)
        # self.statusBar.AddPage(self.model_panel2, u"数据收集", False)
        # # self.statusBar.AddPage(self.model_panel4, u"决策生成", False)
        # self.statusBar.AddPage(self.model_panel7, u"决策生成", False)
        # self.statusBar.AddPage(self.model_panel5, u"智能校准", False)
        # self.statusBar.AddPage(self.model_panel6, u"系统管理", False)

        # self.main_panel.Layout()
        # self.main_panel.Bind(wx.EVT_SIZE, self.OnReSize)
        #
        # nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在日期
        #
        # # 状态栏
        # self.m_statusBar = self.CreateStatusBar()
        # # 将状态栏分割为2个区域,比例为3:1
        # self.m_statusBar.SetFieldsCount(2)
        # self.m_statusBar.SetStatusWidths([-3, -1])
        # self.m_statusBar.SetStatusText(" Version Beta 0.0.1\t", 0)
        # self.m_statusBar.SetStatusText(nowTime, 1)

    #         bSizerforwholepanel.Fit(self.main_panel)

    # 欢迎页面
    # self.Welcome()

    def OnReSize(self, event):
        print("hello")
        # 在绑定的size事件中使右上角用户panel右对齐
        # x, y = self.GetSize()
        # w, h = self.userPanel.GetSize()
        # self.userPanel.SetPosition((x - w - 25, 0))
        # self.Refresh()
        # self.main_panel.Layout()

    def Logoff(self, event):
        # 注销操作
        self.Destroy()
        self.UpdateUI(0)

    def updateTree(self):
        print("hello")
