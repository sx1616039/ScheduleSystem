# -*- coding: utf-8 -*-
import os
import wx


class OrderTree(wx.TreeCtrl):
    def __init__(self, parent=None):
        wx.TreeCtrl.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                             wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS)
        self.updateTree()
        
    # 更新导航栏树
    def updateTree(self):
        default_path = "..\\orders"
        self.DeleteAllItems()
        """左侧树状图"""
        root = self.AddRoot('订单', data=0)
        tree = [0] * 1000
        treeMap = {default_path: root}
        i = 0
        for roots, dirs, files in os.walk(default_path):
            for dir_name in dirs:
                dir_path = os.path.join(roots, dir_name)
                tree[i] = self.AppendItem(treeMap[roots], dir_name, data=dir_path)
                treeMap[dir_path] = tree[i]
                i += 1
            for file in files:
                file_path = os.path.join(roots, file)
                tree[i] = self.AppendItem(treeMap[roots], file, data=file_path)
                i += 1
