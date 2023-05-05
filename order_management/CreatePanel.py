# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os
import wx.xrc
import wx.lib.newevent
import random
import numpy as np


class CreatePanel(wx.Panel):

    def __init__(self, parent, order_path=None):
        wx.Panel.__init__(self, parent, 0, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        ''' 第一行：选择路径按钮 '''
        file_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_file_name = wx.StaticText(file_panel, wx.ID_ANY, u"名称:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_file_name = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(100, 25), style=wx.TE_LEFT)
        self.text_file_name.AppendText('新订单1')
        label_file_path = wx.StaticText(file_panel, wx.ID_ANY, u"路径：",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_file_path = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25), style=wx.TE_LEFT)
        self.text_file_path.AppendText('C:\\Users\\wxq\\Desktop\\ScheduleSystem-main\\orders')
        ''' 选择路径按钮 '''
        btn_selection = wx.Button(file_panel, wx.ID_ANY, u"选择", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_selection.Bind(wx.EVT_BUTTON, self.on_selection_button)
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_sizer.Add(label_file_name, 0, wx.ALL, 7)
        file_sizer.Add(self.text_file_name, 5, wx.ALL, 5)
        file_sizer.Add(label_file_path, 0, wx.ALL, 7)
        file_sizer.Add(self.text_file_path, 5, wx.ALL, 5)
        file_sizer.Add(btn_selection, 1, wx.ALL, 5)
        file_panel.SetSizer(file_sizer)

        ''' 第二行设置参数 '''
        up_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_job_num = wx.StaticText(up_panel, wx.ID_ANY, u"作业数量：",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_job_num = wx.TextCtrl(up_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25), style=wx.TE_LEFT)
        self.text_job_num.AppendText('6')
        label_machine_num = wx.StaticText(up_panel, wx.ID_ANY, u"机器数量:",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_machine_num = wx.TextCtrl(up_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25), style=wx.TE_LEFT)
        self.text_machine_num.AppendText('6')
        self.generation_method = ['自定义', '随机生成']
        label_generation = wx.StaticText(up_panel, wx.ID_ANY, u"创建方法:",
                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.combobox_generation = wx.ComboBox(up_panel, -1, size=wx.Size(80, -1),
                                        choices=self.generation_method)
        self.combobox_generation.SetSelection(1)
        self.combobox_generation.Bind(wx.EVT_COMBOBOX, self.on_select_combobox_generation)

        label_min_time = wx.StaticText(up_panel, wx.ID_ANY, u"最小加工时长:",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_min_time = wx.TextCtrl(up_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25), style=wx.TE_LEFT)
        self.text_min_time.AppendText('1')
        label_max_time = wx.StaticText(up_panel, wx.ID_ANY, u"最大加工时长:",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_max_time = wx.TextCtrl(up_panel, wx.ID_ANY, pos=(0, 30), size=(50, 25), style=wx.TE_LEFT)
        self.text_max_time.AppendText('99')
        ''' 生成订单按钮 '''
        btn_generating = wx.Button(up_panel, wx.ID_ANY, u"生成订单",
                                 wx.DefaultPosition, wx.Size(100, 26), 0)
        btn_generating.SetBitmap(wx.Bitmap('icon/run.ico'))
        btn_generating.Bind(wx.EVT_BUTTON, self.on_generating_button)

        up_sizer = wx.BoxSizer(wx.HORIZONTAL)
        up_sizer.Add(label_job_num, 0, wx.ALL, 7)
        up_sizer.Add(self.text_job_num, 5, wx.ALL, 5)
        up_sizer.Add(label_machine_num, 0, wx.ALL, 7)
        up_sizer.Add(self.text_machine_num, 5, wx.ALL, 5)
        up_sizer.Add(label_generation, 0, wx.ALL, 7)
        up_sizer.Add(self.combobox_generation, 5, wx.ALL, 5)
        up_sizer.Add(label_min_time, 0, wx.ALL, 7)
        up_sizer.Add(self.text_min_time, 5, wx.ALL, 5)
        up_sizer.Add(label_max_time, 0, wx.ALL, 7)
        up_sizer.Add(self.text_max_time, 5, wx.ALL, 5)
        up_sizer.Add(btn_generating, 1, wx.ALL, 5)
        up_panel.SetSizer(up_sizer)

        # 表格
        grid_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.grid = wx.grid.Grid(grid_panel, id=wx.ID_ANY, size=(900, 500))
        # 创建一个100X50的电子表格
        self.grid.CreateGrid(100, 50 * 2)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.change_value)
        grid_box = wx.BoxSizer(wx.HORIZONTAL)
        grid_box.Add(self.grid, proportion=1, flag=wx.EXPAND)
        grid_panel.SetSizer(grid_box)

        # main layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(file_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(up_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(grid_panel, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)
        self.current_selection = self.generation_method[0]

    def on_select_combobox_generation(self, event):
        pos = self.combobox_generation.GetSelection()
        self.current_selection = self.generation_method[pos]

    def on_selection_button(self, event):
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_file_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def change_value(self, event):
        self.save_order()

    def on_generating_button(self, event):
        print("create")
        self.create_order()

    def create_order(self):
        job_num = int(self.text_job_num.GetLineText(0))
        machine_num = int(self.text_machine_num.GetLineText(0))
        min_time = int(self.text_min_time.GetLineText(0))
        max_time = int(self.text_max_time.GetLineText(0))
        self.job = np.zeros([job_num, machine_num*2], dtype=int)
        if self.current_selection == self.generation_method[1]:
            for j in range(job_num):
                machines = random.sample(range(1, machine_num+1), machine_num)
                print(machines)
                for i in range(machine_num):
                    self.job[j][2*i] = machines[i]
                    self.job[j][2*i+1] = round(random.uniform(min_time, max_time))

        for j in range(job_num):
            for i in range(machine_num):
                self.grid.SetCellValue(j, 2 * i, str(self.job[j][2 * i]))
                self.grid.SetCellValue(j, 2 * i + 1, str(self.job[j][2 * i + 1]))
        self.save_order()

    def save_order(self):
        dir_path = self.text_file_path.GetLineText(0)
        file_name = self.text_file_name.GetLineText(0)
        file_path = os.path.join(dir_path, file_name)
        job_num = int(self.text_job_num.GetLineText(0))
        machine_num = int(self.text_machine_num.GetLineText(0))

        file = open(file_path, mode='w')
        file.write(str(job_num) + '\t')
        file.write(str(machine_num))
        file.write('\n')
        for j in range(job_num):
            jobi = []
            for i in range(machine_num):
                machine = self.grid.GetCellValue(j, 2 * i)
                time = self.grid.GetCellValue(j, 2 * i + 1)
                jobi.append(machine)
                jobi.append('\t')
                jobi.append(time)
                jobi.append('\t')
            jobi.append('\n')
            file.writelines(jobi)
        file.close()
        # 找到OrderManagementPanel的树结构并更新
        self.Parent.Parent.Parent.order_tree.updateTree()
