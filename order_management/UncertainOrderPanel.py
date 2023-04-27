# -*- coding: utf-8 -*-

###########################################################################
# Created on 2023.5.10
###########################################################################
import os
import wx.xrc
import wx.lib.newevent
import random
import numpy as np


class UncertainOrderPanel(wx.Panel):

    def __init__(self, parent, order_path=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        ''' 第一行：选择路径按钮 '''
        file_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        label_original_path = wx.StaticText(file_panel, wx.ID_ANY, u"源路径:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_original_path = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25), style=wx.TE_LEFT)
        self.text_original_path.AppendText(order_path)
        self.text_original_path.SetEditable(False)
        label_file_path = wx.StaticText(file_panel, wx.ID_ANY, u"保存路径：",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_file_path = wx.TextCtrl(file_panel, wx.ID_ANY, pos=(0, 30), size=(200, 25), style=wx.TE_LEFT)
        self.text_file_path.AppendText('C:\\Users\\wxq\\Desktop\\ScheduleSystem-main\\orders')
        ''' 选择路径按钮 '''
        btn_selection = wx.Button(file_panel, wx.ID_ANY, u"选择路径", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_selection.Bind(wx.EVT_BUTTON, self.on_selection_button)
        ''' 生成不确定订单 '''
        btn_gen = wx.Button(file_panel, wx.ID_ANY, u"生成订单", wx.DefaultPosition, wx.Size(100, 25), 0)
        btn_gen.SetBitmap(wx.Bitmap('icon/run.ico'))
        btn_gen.Bind(wx.EVT_BUTTON, self.on_button_gen_order)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_sizer.Add(label_original_path, 0, wx.ALL, 8)
        file_sizer.Add(self.text_original_path, 2, wx.ALL, 6)
        file_sizer.Add(label_file_path, 0, wx.ALL, 8)
        file_sizer.Add(self.text_file_path, 2, wx.ALL , 6)
        file_sizer.Add(btn_selection, 1, wx.ALL, 6)
        file_sizer.Add(btn_gen, 1, wx.ALL | wx.EXPAND, 8)
        file_panel.SetSizer(file_sizer)

        ''' 第二行加工时长不确定参数设置 '''
        uncertain_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        self.check_time_uncertainty = wx.CheckBox(uncertain_panel, label='工时不确定性:')
        self.label_occurrence_time = wx.StaticText(uncertain_panel, wx.ID_ANY, u"工时改变的时刻(%):",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_occurrence_time = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25),
                                                style=wx.TE_LEFT)
        self.text_occurrence_time.AppendText('0')
        label_prob = wx.StaticText(uncertain_panel, wx.ID_ANY, u"分布类型:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.prob_type = ['均匀分布', '正态分布']
        self.combobox_prob_type = wx.ComboBox(uncertain_panel, -1, size=wx.Size(100, -1),
                                              choices=self.prob_type)
        self.combobox_prob_type.SetSelection(0)
        self.combobox_prob_type.Bind(wx.EVT_COMBOBOX, self.on_select_combobox_prob_type)
        self.label_prob_bias = wx.StaticText(uncertain_panel, wx.ID_ANY, u"偏移量(%):",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_prob_bias = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25), style=wx.TE_LEFT)
        self.text_prob_bias.AppendText('10')

        label_uncertain_rate = wx.StaticText(uncertain_panel, wx.ID_ANY, u"不确定率(%):",
                                             wx.DefaultPosition, wx.DefaultSize, 0)

        self.text_uncertain_rate = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25),
                                               style=wx.TE_LEFT)
        self.text_uncertain_rate.AppendText('25')

        time_uncertainty_sizer = wx.BoxSizer(wx.HORIZONTAL)
        time_uncertainty_sizer.Add(self.check_time_uncertainty, 1, wx.ALL | wx.EXPAND, 8)
        time_uncertainty_sizer.Add((4, 20))
        time_uncertainty_sizer.Add(self.label_occurrence_time, 0, wx.ALL | wx.EXPAND, 8)
        time_uncertainty_sizer.Add(self.text_occurrence_time, 2, wx.ALL | wx.EXPAND, 6)
        time_uncertainty_sizer.Add(label_prob, 0, wx.ALL | wx.EXPAND, 8)
        time_uncertainty_sizer.Add(self.combobox_prob_type, 1, wx.ALL | wx.EXPAND, 6)
        time_uncertainty_sizer.Add(self.label_prob_bias, 0, wx.ALL | wx.EXPAND, 8)
        time_uncertainty_sizer.Add(self.text_prob_bias, 2, wx.ALL | wx.EXPAND, 6)

        time_uncertainty_sizer.Add(label_uncertain_rate, 0, wx.ALL | wx.EXPAND, 8)
        time_uncertainty_sizer.Add(self.text_uncertain_rate, 2, wx.ALL | wx.EXPAND, 6)

        ''' 第三行工序不确定参数设置 '''
        self.check_order_uncertainty = wx.CheckBox(uncertain_panel, label='工序不确定性:')
        self.label_uncertainty_time = wx.StaticText(uncertain_panel, wx.ID_ANY, u"工序改变的时刻(%):",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_uncertainty_time = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25),
                                                style=wx.TE_LEFT)
        self.text_uncertainty_time.AppendText('0')
        label_uncertain_rate = wx.StaticText(uncertain_panel, wx.ID_ANY, u"不确定率(%):",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_uncertain_order_rate = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25),
                                                     style=wx.TE_LEFT)
        self.text_uncertain_order_rate.AppendText('25')
        order_uncertainty_sizer = wx.BoxSizer(wx.HORIZONTAL)
        order_uncertainty_sizer.Add(self.check_order_uncertainty, 1, wx.ALL, 8)
        order_uncertainty_sizer.Add((4, 20))
        order_uncertainty_sizer.Add(self.label_uncertainty_time, 0, wx.ALL | wx.EXPAND, 8)
        order_uncertainty_sizer.Add(self.text_uncertainty_time, 5, wx.ALL | wx.EXPAND, 6)
        order_uncertainty_sizer.Add(label_uncertain_rate, 0, wx.ALL | wx.EXPAND, 8)
        order_uncertainty_sizer.Add(self.text_uncertain_order_rate, 5, wx.ALL | wx.EXPAND, 6)

        ''' 第四行规模不确定参数设置 '''
        self.check_scale_uncertainty = wx.CheckBox(uncertain_panel, label='规模不确定性:')
        label_arrive_time = wx.StaticText(uncertain_panel, wx.ID_ANY, u" 新作业到达时刻(%):",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_arrive_time = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25),
                                            style=wx.TE_LEFT)
        self.text_arrive_time.AppendText('0')
        label_job_num = wx.StaticText(uncertain_panel, wx.ID_ANY, u"新作业数量:",
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_job_num = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25),
                                        style=wx.TE_LEFT)
        self.text_job_num.AppendText('1')
        label_machine_num = wx.StaticText(uncertain_panel, wx.ID_ANY, u"机器数量:",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_machine_num = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25), style=wx.TE_LEFT)
        self.text_machine_num.AppendText('6')

        label_min_time = wx.StaticText(uncertain_panel, wx.ID_ANY, u"最小加工时长:",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_min_time = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25), style=wx.TE_LEFT)
        self.text_min_time.AppendText('1')
        label_max_time = wx.StaticText(uncertain_panel, wx.ID_ANY, u"最大加工时长:",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_max_time = wx.TextCtrl(uncertain_panel, wx.ID_ANY, pos=(0, 30), size=(30, 25), style=wx.TE_LEFT)
        self.text_max_time.AppendText('99')

        scale_uncertainty_sizer = wx.BoxSizer(wx.HORIZONTAL)
        scale_uncertainty_sizer.Add(self.check_scale_uncertainty, 1, wx.ALL | wx.EXPAND, 8)
        scale_uncertainty_sizer.Add(label_arrive_time, 0, wx.ALL | wx.EXPAND, 8)
        scale_uncertainty_sizer.Add(self.text_arrive_time, 1, wx.ALL | wx.EXPAND, 6)
        scale_uncertainty_sizer.Add(label_job_num, 0, wx.ALL | wx.EXPAND, 8)
        scale_uncertainty_sizer.Add(self.text_job_num, 1, wx.ALL | wx.EXPAND, 6)
        scale_uncertainty_sizer.Add(label_machine_num, 0, wx.ALL | wx.EXPAND, 8)
        scale_uncertainty_sizer.Add(self.text_machine_num, 1, wx.ALL | wx.EXPAND, 6)
        scale_uncertainty_sizer.Add(label_min_time, 0, wx.ALL | wx.EXPAND, 8)
        scale_uncertainty_sizer.Add(self.text_min_time, 1, wx.ALL | wx.EXPAND, 6)
        scale_uncertainty_sizer.Add(label_max_time, 0, wx.ALL | wx.EXPAND, 8)
        scale_uncertainty_sizer.Add(self.text_max_time, 1, wx.ALL | wx.EXPAND, 6)

        uncertain_sizer = wx.BoxSizer(wx.VERTICAL)
        uncertain_sizer.Add(time_uncertainty_sizer, 0, wx.ALL, 5)
        uncertain_sizer.Add(order_uncertainty_sizer, 0, wx.ALL, 5)
        uncertain_sizer.Add(scale_uncertainty_sizer, 0, wx.ALL, 5)
        uncertain_panel.SetSizer(uncertain_sizer)

        ''' 不确定性订单的表格显示 '''
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
        main_sizer.Add(uncertain_panel, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(grid_panel, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)
        basename = os.path.basename(order_path)
        self.new_instance_path = os.path.join(self.text_file_path.GetLineText(0), basename)
        self.job_num = 0
        self.machine_num = 0
        self.read_order(order_path)

    def on_selection_button(self, event):
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.text_file_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_select_combobox_prob_type(self, event):
        pos = self.combobox_prob_type.GetSelection()
        print(pos)
        if pos == 0:
            self.label_prob_bias.SetLabel('偏移量(%):')
            self.text_prob_bias.SetValue('10')
        elif pos == 1:
            self.label_prob_bias.SetLabel('方差:')
            self.text_prob_bias.SetValue('1')
        else:
            return

    def on_button_gen_order(self, event):
        origin_path = self.text_original_path.GetLineText(0)
        if os.path.isdir(origin_path):
            for file_name in os.listdir(origin_path):
                self.gen_uncertain_order(os.path.join(origin_path, file_name))
        else:
            self.gen_uncertain_order(origin_path)

    def gen_uncertain_order(self, path):
        job_num, machine_num, job = self.read_order(path)
        if self.check_time_uncertainty.GetValue() == 1:  # 考虑加工时长不确定性
            job = self.gen_time_uncertainty(job_num, machine_num, job)
        if self.check_order_uncertainty.GetValue() == 1:  # 考虑工序不确定性
            job = self.gen_order_uncertainty(job_num, machine_num, job)
        if self.check_scale_uncertainty.GetValue() == 1:  # 考虑规模不确定性
            job_num, machine_num, job = self.gen_scale_uncertainty(job_num, machine_num, job)
        self.save_order(path, job_num, machine_num, job)
        self.job_num = job_num
        self.machine_num = machine_num

    def gen_time_uncertainty(self, job_num, machine_num, job):
        prob_type = self.combobox_prob_type.GetSelection()
        bias = 0
        sigma = 0
        if prob_type == 0:
            bias = float(self.text_prob_bias.GetLineText(0))/100
        else:
            sigma = float(self.text_prob_bias.GetLineText(0))

        change_rate = float(self.text_uncertain_rate.GetLineText(0))/100
        for j in range(job_num):
            for i in range(machine_num):
                if random.random() < change_rate:
                    process_time = job[j][i * 2 + 1]
                    if prob_type == 0:
                        new_process_time = round(process_time * random.uniform(1 - bias, 1 + bias))
                    else:
                        new_process_time = round(random.gauss(process_time, sigma))
                    job[j][i * 2 + 1] = new_process_time
        return job

    def gen_order_uncertainty(self, job_num, machine_num, job):
        exchange_rate = float(self.text_uncertain_order_rate.GetLineText(0)) / 100
        exchange_cnt = int(job_num * machine_num * exchange_rate)
        for j in range(exchange_cnt):
            job_id = random.randint(0, job_num - 1)
            op1, op2 = random.sample(range(0, machine_num - 1), 2)
            if op1 >= machine_num - 1 or op2 >= machine_num - 1:
                print("hello")
            process_time1 = job[job_id][op1 * 2 + 1]
            machine1 = job[job_id][op1 * 2]
            job[job_id][op1 * 2 + 1] = job[job_id][op2 * 2 + 1]
            job[job_id][op1 * 2] = job[job_id][op2 * 2]
            job[job_id][op2 * 2 + 1] = process_time1
            job[job_id][op2 * 2] = machine1
        return job

    def gen_scale_uncertainty(self, job_num, machine_num, job):
        new_job_num = int(self.text_job_num.GetLineText(0))
        new_machine_num = int(self.text_machine_num.GetLineText(0))
        min_time = float(self.text_min_time.GetLineText(0))
        max_time = float(self.text_max_time.GetLineText(0))
        new_job = np.zeros([new_job_num + job_num, max(new_machine_num, machine_num)*2], int)
        # 复制原任务
        for j in range(job_num):
            for i in range(max(new_machine_num, machine_num)):
                new_job[j][i * 2] = job[j][i * 2]
                new_job[j][i * 2 + 1] = job[j][i * 2 + 1]
        # 添加新任务
        for j in range(new_job_num):
            machines = random.sample(range(1, machine_num + 1), machine_num)
            for i in range(new_machine_num):
                new_process_time = round(random.uniform(min_time, max_time))
                new_job[j+job_num][2 * i] = machines[i]
                new_job[j+job_num][i * 2 + 1] = new_process_time
        return new_job_num + job_num, new_machine_num, new_job

    def read_order(self, file_path):
        with open(file_path, 'r') as f:
            user_line = f.readline()
            data = user_line.split('\t')
            m_n = list(map(int, data))
            data = f.read()
            data = str(data).replace('\n', '\t')
            data = str(data).split('\t')
            while data.__contains__(""):
                data.remove("")
            job = list(map(int, data))
            job = np.array(job).reshape(m_n[0], m_n[1] * 2)
        f.close()
        job_num = m_n[0]
        machine_num = m_n[1]
        self.job_num = m_n[0]
        self.machine_num = m_n[1]
        for j in range(self.job_num):
            for i in range(self.machine_num):
                self.grid.SetCellValue(j, 2 * i, str(job[j][2 * i]))
                self.grid.SetCellValue(j, 2 * i + 1, str(job[j][2 * i + 1]))
        return job_num, machine_num, job

    def change_value(self, event):
        self.save_order_from_grid()

    def save_order(self, file_path, job_num, machine_num, job):
        output_path = self.text_file_path.GetLineText(0)
        model_name = os.path.basename(file_path).split('.')[0]
        new_instance_name = os.path.join(output_path, model_name) + "_"
        if self.check_time_uncertainty.GetValue() == 1:  # 考虑加工时长不确定性
            sigma = self.text_prob_bias.GetLineText(0)
            change_rate = self.text_uncertain_rate.GetLineText(0)
            new_instance_name = new_instance_name + 'a_' + sigma + '_' +change_rate + '_'
        if self.check_order_uncertainty.GetValue() == 1:  # 考虑工序不确定性
            rate = self.text_uncertain_order_rate.GetLineText(0)
            new_instance_name = new_instance_name + 'b_' + rate + '_'
        if self.check_scale_uncertainty.GetValue() == 1:  # 考虑规模不确定性
            new_job = self.text_job_num.GetLineText(0)
            new_machine = self.text_machine_num.GetLineText(0)
            min_time = self.text_min_time.GetLineText(0)
            max_time = self.text_max_time.GetLineText(0)
            new_instance_name = new_instance_name + 'c_' + new_job + '_' + new_machine + '_' + min_time + '_' + max_time + '_'
        new_instance_name = new_instance_name + ".txt"
        self.new_instance_path = new_instance_name
        file = open(new_instance_name, mode='w')
        file.write(str(job_num) + '\t')
        file.write(str(machine_num))
        file.write('\n')
        for j in range(job_num):
            jobi = []
            for i in range(machine_num):
                time = job[j][i * 2 + 1]
                machine = job[j][i * 2]
                jobi.append(str(machine))
                jobi.append('\t')
                jobi.append(str(time))
                jobi.append('\t')
            jobi.append('\n')
            file.writelines(jobi)
        file.close()

        for j in range(self.job_num):
            for i in range(self.machine_num):
                self.grid.SetCellValue(j, 2 * i, str(job[j][2 * i]))
                self.grid.SetCellValue(j, 2 * i + 1, str(job[j][2 * i + 1]))
        # 找到OrderManagementPanel的树结构并更新
        self.Parent.Parent.Parent.navTree.updateTree()

    def save_order_from_grid(self):
        file = open(self.new_instance_path, mode='w')
        file.write(str(self.job_num) + '\t')
        file.write(str(self.machine_num))
        file.write('\n')
        for j in range(self.job_num):
            jobi = []
            for i in range(self.machine_num):
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
        self.Parent.Parent.Parent.navTree.updateTree()