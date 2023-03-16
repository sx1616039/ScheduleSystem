# -*- coding: utf-8 -*-

import wx
import datetime


# 主界面
class SchedulingSystem(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None, params=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"不确定条件下生产线智能调度平台",
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.APP_EXIT = 0
        self.APP_OPEN = 1
        self.APP_CUT = 2
        self.APP_COPY = 3
        self.APP_CREATE_ORDER = 10
        self.APP_OPEN_ORDER = 11
        self.APP_CUT = 12
        self.APP_COPY = 13

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
        menu_bar = wx.MenuBar()  # 生成菜单栏

        menu_file = wx.Menu()  # 文件菜单
        open_file = wx.MenuItem(menu_file, self.APP_OPEN, "打开")  # 生成一个菜单项
        quit_sys = wx.MenuItem(menu_file, self.APP_EXIT, "退出")  # 生成一个菜单项
        quit_sys.SetBitmap(wx.Bitmap("icon/quit.ico"))  # 给菜单项前面加个小图标
        menu_file.AppendItem(open_file)  # 把菜单项加入到菜单中
        menu_file.AppendItem(quit_sys)
        menu_bar.Append(menu_file, "&文件")  # 把菜单加入到菜单栏中
        self.Bind(wx.EVT_MENU, self.OnQuit, id=self.APP_EXIT)  # 给菜单项加入事件处理

        menu_edit = wx.Menu()  # 编辑菜单
        cut = wx.MenuItem(menu_edit, self.APP_CUT, text="剪切")  # 生成一个菜单项
        copy = wx.MenuItem(menu_edit, self.APP_COPY, text="复制")
        menu_edit.AppendItem(cut)  # 把菜单项加入到菜单中
        menu_edit.AppendItem(copy)
        menu_bar.Append(menu_edit, "&编辑")  # 把菜单加入到菜单栏中

        menu_order_manage = wx.Menu()  # 训练菜单
        order_create = wx.MenuItem(menu_order_manage, self.APP_CREATE_ORDER, text="创建订单")  # 生成一个菜单项
        order_open = wx.MenuItem(menu_order_manage, self.APP_OPEN_ORDER, text="打开订单")  # 生成一个菜单项
        menu_order_manage.AppendItem(order_create)  # 把菜单项加入到菜单中
        menu_order_manage.AppendItem(order_open)  # 把菜单项加入到菜单中
        menu_bar.Append(menu_order_manage, "&订单管理")  # 把菜单加入到菜单栏中

        menu_train = wx.Menu()  # 训练菜单
        train = wx.MenuItem(menu_train, text="train")  # 生成一个菜单项
        # train.SetBitmap(wx.Bitmap("quit.ico"))  # 给菜单项前面加个小图标
        menu_train.AppendItem(train)  # 把菜单项加入到菜单中
        menu_bar.Append(menu_train, "&模型训练")  # 把菜单加入到菜单栏中

        menu_optimization = wx.Menu()  # 优化菜单
        optimization = wx.MenuItem(menu_train, text="train")  # 生成一个菜单项
        menu_bar.Append(menu_optimization, "&模型优化")  # 把菜单加入到菜单栏中
        self.SetMenuBar(menu_bar)  # 把菜单栏加入到Frame框架中

        menu_visualization = wx.Menu()  # 训练菜单
        visualization = wx.MenuItem(menu_train, text="train")  # 生成一个菜单项
        # train.SetBitmap(wx.Bitmap("quit.ico"))  # 给菜单项前面加个小图标
        menu_visualization.AppendItem(visualization)  # 把菜单项加入到菜单中
        menu_bar.Append(menu_visualization, "&可视化")  # 把菜单加入到菜单栏中
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
