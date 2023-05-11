# -*- coding: utf-8 -*-

import wx
import datetime

from model_management import ModelManagePanel
from model_optimization import OptPanel
from model_training import TrainPanel
from order_management import OrderManagePanel
from simulation import SimulationPanel
from visualization import VisualizationPanel


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
        x, y = self.GetSize()
        self.userPanel = wx.Panel(self.main_panel, wx.ID_ANY, (x-200, 0), (200, 30), wx.TAB_TRAVERSAL)
        # 用户显示栏
        self.userText = wx.StaticText(self.userPanel, wx.ID_ANY, "Administrator", (0, 10), (-1, 30), 0)
        self.userText.SetFont(wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL, False))
        # 注销按钮
        self.logoffBtn = wx.Button(self.userPanel, wx.ID_ANY, u"注 销", (100, 3), (-1, 28), 0)
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
        self.panel_model_management = ModelManagePanel.ModelManagePanel(self.NaviPage)
        self.panel_simulation = SimulationPanel.SimulationPanel(self.NaviPage)
        self.panel_train = TrainPanel.TrainPanel(self.NaviPage)
        self.panel_opt = OptPanel.OptPanel(self.NaviPage)
        self.panel_visualization = VisualizationPanel.VisualizationPanel(self.NaviPage)

        self.NaviPage.AddPage(self.panel_order_management, u"订单管理", True)
        self.NaviPage.AddPage(self.panel_model_management, u"模型管理", False)
        self.NaviPage.AddPage(self.panel_simulation, u"仿真运行", False)
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

    def OnReSize(self, event):
        # 在绑定的size事件中使右上角用户panel右对齐
        x, y = self.GetSize()
        self.userPanel.SetPosition((x - 220, 0))
        self.Refresh()
        self.main_panel.Layout()

    def Logoff(self, event):
        # 注销操作
        self.Destroy()
        self.UpdateUI(0)

    def update_order_tree(self):
        self.panel_order_management.order_tree.updateTree()
        self.panel_model_management.order_tree.updateTree()
        self.panel_simulation.order_tree.updateTree()
        self.panel_train.order_tree.updateTree()
        self.panel_opt.order_tree.updateTree()
        self.panel_visualization.order_tree.updateTree()

    def update_model_tree(self):
        self.panel_order_management.model_tree.updateTree()
        self.panel_model_management.model_tree.updateTree()
        self.panel_simulation.model_tree.updateTree()
        self.panel_train.model_tree.updateTree()
        self.panel_opt.model_tree.updateTree()
        self.panel_visualization.model_tree.updateTree()
