# -*- coding: utf-8 -*-

import wx
from GuiManager import Manager


class MainAPP(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
        self.manager = None
        self.frame = None

    def OnInit(self):
        self.manager = Manager(self.UpdateUI)
        self.frame = self.manager.GetFrame(0, {})
        self.frame.Show()
        return True

    # 登录或注销时切换Frame
    def UpdateUI(self, fType, params=None):
        if params is None:
            params = {}
        self.frame.Destroy()
        self.frame = self.manager.GetFrame(fType, params)
        self.frame.Show(True)


def main():
    app = MainAPP()
    app.MainLoop()


if __name__ == '__main__':
    main()
