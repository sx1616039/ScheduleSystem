# -*- coding: utf-8 -*-

import wx
import datetime


# 主界面
class SchedulingSystem(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None, params=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"不确定条件下生产线智能调度平台",
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.APP_EXIT = 0
        self.main_panel = None
        self.statusBar = None
        if params is None:
            params = {}
        self.SetIcon(wx.Icon('icon/sys.ico', wx.BITMAP_TYPE_ICO))
        self.SetSizeHints((1280, 720), wx.DefaultSize)
        self.Maximize(True)
        self.UpdateUI = UpdateUI
        self.InitUI(params)

    def InitUI(self, params):
        menuBar = wx.MenuBar()  # 生成菜单栏
        fileMenu = wx.Menu()  # 文件菜单

        quit = wx.MenuItem(fileMenu, self.APP_EXIT, "Quit")  # 生成一个菜单项
        # quit.SetBitmap(wx.Bitmap("quit.ico"))  # 给菜单项前面加个小图标
        fileMenu.AppendItem(quit)  # 把菜单项加入到菜单中
        menuBar.Append(fileMenu, "&File")  # 把菜单加入到菜单栏中

        self.Bind(wx.EVT_MENU, self.OnQuit, id=self.APP_EXIT)  # 给菜单项加入事件处理
        editMenu = wx.Menu()  # 编辑菜单
        back = wx.MenuItem(editMenu, text="Cut")  # 生成一个菜单项
        # back.SetBitmap(wx.Bitmap("quit.ico"))  # 给菜单项前面加个小图标
        editMenu.AppendItem(back)  # 把菜单项加入到菜单中
        menuBar.Append(editMenu, "&Edit")  # 把菜单加入到菜单栏中

        trainMenu = wx.Menu()  # 训练菜单
        train = wx.MenuItem(trainMenu, text="train")  # 生成一个菜单项
        # train.SetBitmap(wx.Bitmap("quit.ico"))  # 给菜单项前面加个小图标
        trainMenu.AppendItem(train)  # 把菜单项加入到菜单中
        menuBar.Append(trainMenu, "&Train")  # 把菜单加入到菜单栏中
        trainMenu = wx.Menu()  # 训练菜单
        self.SetMenuBar(menuBar)  # 把菜单栏加入到Frame框架中
        # 最底层panel
        self.main_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        # 最底层panel垂直布局
        main_layout = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(main_layout)

        # 上方导航页签
        self.statusBar = wx.Notebook(self.main_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.statusBar.SetPadding(wx.Size(20, 5))
        self.statusBar.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL, False))
        main_layout.Add(self.statusBar, 1, wx.EXPAND | wx.ALL, 5)
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
