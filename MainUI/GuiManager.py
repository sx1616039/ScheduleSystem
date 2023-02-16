# -*- coding: utf-8 -*-
from MainFrame import SchedulingSystem


class Manager:
    def __init__(self, updateUI):
        self.UpdateUI = updateUI

    def GetFrame(self, fType, params):
        frame = self.CreateFrame(fType, params)
        return frame

    def CreateFrame(self, fType, params):
        if fType == 0:
            return SchedulingSystem(parent=None, id=fType, UpdateUI=self.UpdateUI, params=params)



