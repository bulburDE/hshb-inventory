# coding: utf-8
import sys
import wx
import wx.lib.intctrl
import gettext
import getpass
import InventoryItemList as Inv


yourlsurl = 'http://hshb.de/yourls-api.php'
with open('yourls-signature.txt','r') as s:
    sig = s.read().strip()

wikiurl = 'https://wiki.hackerspace-bremen.de'
user = 'heth'
pw = getpass.getpass('Passwort: ')

inv = Inv.InventoryItemList(yourlsurl, sig, wikiurl, user, pw, "test.db")

class InvFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,300))

        self.OverallSizer = wx.BoxSizer(wx.VERTICAL)

        self.NewEntryBox = wx.StaticBox(self, wx.ID_ANY, _("New Entry"))
        self.NewEntryBoxSizer = wx.StaticBoxSizer(self.NewEntryBox, wx.VERTICAL)

        self.NewEntrySizer = wx.GridSizer(3, 2, 5, 5)

        self.InventNumberStat = wx.StaticText(self, wx.ID_ANY, _("Inventory Number"))
        self.InventNumberText = wx.lib.intctrl.IntCtrl(self, wx.ID_ANY, max=9999)
        self.TitleStat = wx.StaticText(self, wx.ID_ANY, _("Item Title"))
        self.TitleText = wx.TextCtrl(self, wx.ID_ANY)
        self.FolderStat = wx.StaticText(self, wx.ID_ANY, _("Subfolder"))
        self.FolderCombo = wx.ComboBox(self, wx.ID_ANY, choices=[x[0] for x in inv.GetFolders()])

        self.NewEntrySizer.Add(self.InventNumberStat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.InventNumberText, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.TitleStat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.TitleText, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.FolderStat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.FolderCombo, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.NewButton = wx.Button(self, wx.ID_ANY, _("Create new entry"))

        self.NewEntryBoxSizer.Add(self.NewEntrySizer, 1, wx.ALL|wx.EXPAND)
        self.NewEntryBoxSizer.Add(self.NewButton, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.OldEntryBox = wx.StaticBox(self, wx.ID_ANY, _("Existing Entries"))
        self.OldEntryBoxSizer = wx.StaticBoxSizer(self.OldEntryBox, wx.HORIZONTAL)

        self.OldEntrySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.EntryList = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.EntryList.InsertColumn(0,_("Number"))
        self.EntryList.InsertColumn(1,_("Title"))
        for item in inv.GetAllItems():
            self.EntryList.Append(item)
        self.EntryList.SetColumnWidth(1,wx.LIST_AUTOSIZE)

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

        self.OverallSizer.Add(self.NewEntryBoxSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.OverallSizer.Add(self.OldEntryBoxSizer, 1, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(self.OverallSizer)
        self.NewEntrySizer.RecalcSizes()

        self.Bind(wx.EVT_BUTTON, self.NewEntry, self.NewButton)

        self.Show(True)

    def NewEntry(self, event):
        inv.AddNewItem(int(self.InventNumberText.GetValue()), self.TitleText.GetValue(), self.FolderCombo.GetValue())

gettext.install('hshb-inventory', './locale', unicode=True)

app = wx.App(False)
frame = InvFrame(None, _('HSHB Inventory'))
app.MainLoop()
