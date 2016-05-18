# coding: utf-8
import sys
import wx
import gettext

class InvFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,300))

        self.OverallSizer = wx.BoxSizer(wx.VERTICAL)

        self.NewEntryBox = wx.StaticBox(self, -1, _('New Entry'))
        self.NewEntryBoxSizer = wx.StaticBoxSizer(self.NewEntryBox, wx.VERTICAL)

        self.NewEntrySizer = wx.GridSizer(2, 2, 5, 5)

        self.InventNumberStat = wx.StaticText(self, wx.ID_ANY, _("Inventory Number"))
        self.InventNumberText = wx.TextCtrl(self, wx.ID_ANY)
        self.TitleStat = wx.StaticText(self, wx.ID_ANY, _("Item Title"))
        self.TitleText = wx.TextCtrl(self, wx.ID_ANY)

        self.NewEntrySizer.Add(self.InventNumberStat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.InventNumberText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.TitleStat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.TitleText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)

        self.NewEntryBoxSizer.Add(self.NewEntrySizer)
        self.OverallSizer.Add(self.NewEntryBoxSizer)

        self.SetSizer(self.OverallSizer)
        self.Show(True)

gettext.install('hshb-inventory', './locale', unicode=True)

app = wx.App(False)
frame = InvFrame(None, _('HSHB Inventory'))
app.MainLoop()
