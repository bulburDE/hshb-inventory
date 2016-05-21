# coding: utf-8
import sys
import wx
import gettext

class InvFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,300))

        self.OverallSizer = wx.BoxSizer(wx.VERTICAL)

        self.NewEntryBox = wx.StaticBox(self, wx.ID_ANY, _("New Entry"))
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

        self.NewButton = wx.Button(self, wx.ID_ANY, _("Create new entry"))

        self.NewEntryBoxSizer.Add(self.NewEntrySizer)
        self.NewEntryBoxSizer.Add(self.NewButton, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.OldEntryBox = wx.StaticBox(self, wx.ID_ANY, _("Existing Entries"))
        self.OldEntryBoxSizer = wx.StaticBoxSizer(self.OldEntryBox, wx.HORIZONTAL)

        self.OldEntrySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.EntryList = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.EntryList.InsertColumn(0,_("Number"))
        self.EntryList.InsertColumn(1,_("Title"))

        self.ListButtonSizer = wx.BoxSizer(wx.VERTICAL)

        self.CreateLabelButton = wx.Button(self, wx.ID_ANY, _("Create Label"))
        self.IncrementalUpdateButton = wx.Button(self, wx.ID_ANY, _("Incremental Update"))
        self.CompleteUpdateButton = wx.Button(self, wx.ID_ANY, _("Complete Update"))

        self.ListButtonSizer.Add(self.CreateLabelButton, 0, wx.ALL|wx.EXPAND)
        self.ListButtonSizer.Add(self.IncrementalUpdateButton, 0, wx.ALL|wx.EXPAND)
        self.ListButtonSizer.Add(self.CompleteUpdateButton, 0, wx.ALL|wx.EXPAND)

        self.OldEntrySizer.Add(self.EntryList, 1, wx.ALL|wx.EXPAND)

        self.OldEntryBoxSizer.Add(self.OldEntrySizer, 1, wx.ALL|wx.EXPAND)
        self.OldEntryBoxSizer.Add(self.ListButtonSizer, 0, wx.ALL|wx.EXPAND)

        self.OverallSizer.Add(self.NewEntryBoxSizer, 0, wx.ALL|wx.EXPAND)
        self.OverallSizer.Add(self.OldEntryBoxSizer, 1, wx.ALL|wx.EXPAND)

        self.SetSizer(self.OverallSizer)
        self.Show(True)

gettext.install('hshb-inventory', './locale', unicode=True)

app = wx.App(False)
frame = InvFrame(None, _('HSHB Inventory'))
app.MainLoop()
