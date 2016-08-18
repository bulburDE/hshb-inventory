# coding: utf-8
import sys
import wx
import wx.lib.intctrl
import gettext
import getpass
import ConfigParser
import io
import InventoryItemList as Inv
import InventoryLabelMaker as LM

default_config = """
[yourls]
yourlsurl = http://hshb.de/yourls-api.php
signature = none
[wiki]
wikiurl = https://wiki.hackerspace-bremen.de
user = user
[db]
dbfile = test.db
"""

inifile = "inventory.ini"

Config = ConfigParser.ConfigParser()
Config.readfp(io.BytesIO(default_config))
Config.read(inifile)

inv = Inv.InventoryItemList()
labelmaker = LM.InventoryLabelMaker()

class LoginDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(LoginDialog, self).__init__(*args, **kw)

        self.InitUi()
        self.SetSize((350, 300))

    def InitUi(self):
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)

        self.YourlsBox = wx.StaticBox(self, wx.ID_ANY, _("Yourls"))
        self.YourlsBoxSizer = wx.StaticBoxSizer(self.YourlsBox, wx.HORIZONTAL)
        self.YourlsSigLabel = wx.StaticText(self, wx.ID_ANY, _("Yourls Signature"))
        self.YourlsSigText = wx.TextCtrl(self, wx.ID_ANY, Config.get("yourls", "signature"))
        self.YourlsBoxSizer.Add(self.YourlsSigLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.YourlsBoxSizer.Add(self.YourlsSigText, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.WikiBox = wx.StaticBox(self, wx.ID_ANY, _("DokuWiki"))
        self.WikiBoxSizer = wx.StaticBoxSizer(self.WikiBox, wx.HORIZONTAL)
        self.WikiSizer = wx.GridSizer(2, 2, 5, 5)
        self.WikiUserLabel = wx.StaticText(self, wx.ID_ANY, _("Wiki Username"))
        self.WikiUserText = wx.TextCtrl(self, wx.ID_ANY, Config.get("wiki", "user"))
        self.WikiSizer.Add(self.WikiUserLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.WikiSizer.Add(self.WikiUserText, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.WikiPwLabel = wx.StaticText(self, wx.ID_ANY, _("Wiki Password"))
        self.WikiPwText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PASSWORD)
        self.WikiSizer.Add(self.WikiPwLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.WikiSizer.Add(self.WikiPwText, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.WikiBoxSizer.Add(self.WikiSizer, 1, wx.ALL|wx.EXPAND)

        self.DBBox = wx.StaticBox(self, wx.ID_ANY, _("Database"))
        self.DBBoxSizer = wx.StaticBoxSizer(self.DBBox, wx.HORIZONTAL)
        self.DBLabel = wx.StaticText(self, wx.ID_ANY, _("DB Filename"))
        self.DBText = wx.TextCtrl(self, wx.ID_ANY, Config.get("db", "dbfile"))
        self.DBBoxSizer.Add(self.DBLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.DBBoxSizer.Add(self.DBText, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.LoginButton = wx.Button(self, wx.ID_ANY, _("Login"))

        self.MainSizer.Add(self.YourlsBoxSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.WikiBoxSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.DBBoxSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.MainSizer.Add(self.LoginButton, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(self.MainSizer)

        self.Bind(wx.EVT_BUTTON, self.DoLogin, self.LoginButton)

    def DoLogin(self, event):
        try:
            inv.Setup(Config.get("yourls", "yourlsurl"), self.YourlsSigText.GetValue(), Config.get("wiki", "wikiurl"), self.WikiUserText.GetValue(), self.WikiPwText.GetValue(), self.DBText.GetValue())
        except:
            dlg = wx.MessageDialog(self, 
                                   _("Login not successful!"),
                                   _("Error"), wx.OK|wx.ICON_ERROR)
            result = dlg.ShowModal()
            dlg.Destroy()
            return
        Config.set("yourls", "signature", self.YourlsSigText.GetValue())
        Config.set("wiki", "user", self.WikiUserText.GetValue())
        Config.set("db", "dbfile", self.DBText.GetValue())
        with open("inventory.ini", 'wb') as configfile:
            Config.write(configfile)
        self.EndModal(wx.OK)

class InvFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(450,700))

        self.OverallSizer = wx.BoxSizer(wx.VERTICAL)

        self.NewEntryBox = wx.StaticBox(self, wx.ID_ANY, _("New Entry"))
        self.NewEntryBoxSizer = wx.StaticBoxSizer(self.NewEntryBox, wx.VERTICAL)

        self.NewEntrySizer = wx.GridSizer(3, 2, 5, 5)

        self.InventNumberStat = wx.StaticText(self, wx.ID_ANY, _("Inventory Number"))
        self.InventNumberText = wx.lib.intctrl.IntCtrl(self, wx.ID_ANY, max=9999)
        self.InventNumberText.Disable()
        self.TitleStat = wx.StaticText(self, wx.ID_ANY, _("Item Title"))
        self.TitleText = wx.TextCtrl(self, wx.ID_ANY)
        self.TitleText.Disable()
        self.FolderStat = wx.StaticText(self, wx.ID_ANY, _("Subfolder"))
        self.FolderCombo = wx.ComboBox(self, wx.ID_ANY)
        self.FolderCombo.Disable()

        self.NewEntrySizer.Add(self.InventNumberStat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.InventNumberText, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.TitleStat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.TitleText, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.FolderStat, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntrySizer.Add(self.FolderCombo, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.NewButton = wx.Button(self, wx.ID_ANY, _("Create new entry"))
        self.NewButton.Disable()
        self.LoginButton = wx.Button(self, wx.ID_ANY, _("Login"))
        # self.NewButton.SetToolTipString(_("Creates a new Wiki-Entry, the shortlink and the label"))

        self.NewEntryBoxSizer.Add(self.NewEntrySizer, 1, wx.ALL|wx.EXPAND)
        self.NewEntryBoxSizer.Add(self.NewButton, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.NewEntryBoxSizer.Add(self.LoginButton, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        self.OldEntryBox = wx.StaticBox(self, wx.ID_ANY, _("Existing Entries"))
        self.OldEntryBoxSizer = wx.StaticBoxSizer(self.OldEntryBox, wx.HORIZONTAL)

        self.OldEntrySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.EntryList = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.EntryList.InsertColumn(0,_("Number"))
        self.EntryList.InsertColumn(1,_("Title"))

        self.ListButtonSizer = wx.BoxSizer(wx.VERTICAL)

        self.CreateLabelButton = wx.Button(self, wx.ID_ANY, _("Create Label"))
        self.CreateLabelButton.Disable()
        self.IncrementalUpdateButton = wx.Button(self, wx.ID_ANY, _("Incremental Update"))
        self.IncrementalUpdateButton.Disable()
        self.CompleteUpdateButton = wx.Button(self, wx.ID_ANY, _("Complete Update"))
        self.CompleteUpdateButton.Disable()

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
        self.Bind(wx.EVT_BUTTON, self.Login, self.LoginButton)
        self.Bind(wx.EVT_BUTTON, self.CreateLabel, self.CreateLabelButton)
        self.Bind(wx.EVT_BUTTON, self.IncrementalUpdate, self.IncrementalUpdateButton)
        self.Bind(wx.EVT_BUTTON, self.CompleteUpdate, self.CompleteUpdateButton)

        self.Show(True)

    def Login(self, event):
        dlg = LoginDialog(None, title = _("Login"))
        retval = dlg.ShowModal()
        print retval
        dlg.Destroy()
        if retval == wx.OK:
            self.LoginButton.Disable()
            self.InventNumberText.Enable()
            self.TitleText.Enable()
            self.FolderCombo.Enable()
            self.NewButton.Enable()
            self.CreateLabelButton.Enable()
            self.IncrementalUpdateButton.Enable()
            self.CompleteUpdateButton.Enable()
            self.FolderCombo.AppendItems([x[0] for x in inv.GetFolders()])
            self.UpdateItemList()



    def NewEntry(self, event):
        inv.AddNewItem(int(self.InventNumberText.GetValue()), self.TitleText.GetValue(), self.FolderCombo.GetValue())
        self.UpdateItemList()

    def UpdateItemList(self):
        print inv.NumberOfItems()
        self.EntryList.DeleteAllItems()
        for item in inv.GetAllItems():
            self.EntryList.Append(item)
        self.EntryList.SetColumnWidth(1,wx.LIST_AUTOSIZE)

    def CreateLabel(self, event):
        item = self.EntryList.GetFirstSelected()
        if item >= 0:
            print "creating label for ", self.EntryList.GetItemText(item, 1)
            labelmaker.MakeLabel(self.EntryList.GetItemText(item, 0), self.EntryList.GetItemText(item, 1))
            while self.EntryList.GetNextSelected(item) >= 0:
                item = self.EntryList.GetNextSelected(item)
                print "creating label for ", self.EntryList.GetItemText(item, 1)
                labelmaker.MakeLabel(self.EntryList.GetItemText(item, 0), self.EntryList.GetItemText(item, 1))

    def IncrementalUpdate(self, event):
        idx = 1
        numEmpty = 0
        found = False
        pivotFound = False
        if inv.NumberOfItems() > 0:
            while not found:
                if inv.ExistsItem(idx):
                    if pivotFound:
                        if numEmpty > 7:
                            found = True
                        else:
                            pivotFound = False
                            numEmpty = 0
                    else:
                        idx += 10
                else:
                    pivotFound = True
                    numEmpty += 1
                    idx -= 1
        else:
            idx = 0
        for i in range(idx + 1, idx + 12):
            inv.RetrieveItemInfo(i)
        self.UpdateItemList()

    def CompleteUpdate(self, event):
        dlg = wx.MessageDialog(self, 
                               _("This may take a long time!"),
                               _("Are you sure?"), wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            inv.ClearDB()
            for i in range(1, 10000):
                inv.RetrieveItemInfo(i)
            self.UpdateItemList()


gettext.install('hshb-inventory', './locale', unicode=True)

app = wx.App(False)
frame = InvFrame(None, _('HSHB Inventory'))
app.MainLoop()
