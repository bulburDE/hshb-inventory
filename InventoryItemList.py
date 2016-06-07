# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import yourls
import sqlite3
import getpass
import dokuwiki
import re


class InventoryItemList:
    def __init__(self, yourlsurl, yourlssig, wikiurl, wikiuser, wikipw, dbname):
        self.prefix = "g"
        self.wiki_basefolder = "geraetschaften"
        self.wikiurl = wikiurl
        self.h1regex = re.compile("={6}\s(.+?)\s={6}")
        self.yourls = yourls.YOURLSClient(yourlsurl, signature=yourlssig)
        self.db = sqlite3.connect(dbname)
        self.dbcursor = self.db.cursor()
        self.dbcursor.execute("""CREATE TABLE IF NOT EXISTS Inventory 
                              (Number INT UNIQUE NOT NULL, Title TEXT NOT NULL, Folder TEXT)""")
        self.db.commit()

        self.wiki = dokuwiki.DokuWiki(wikiurl, wikiuser, wikipw)

    def RetrieveItemInfo(self, number):
        shorturl = self.prefix + format(number, "04")
        print shorturl
        try:
            wikiurl = self.yourls.expand(shorturl)
            print wikiurl
        except:
            print "shorturl not found"
            return
        try:
            (pagename, folder) = self.NamespaceFromUrl(wikiurl)
            print pagename
            print folder
            if self.wiki.pages.info(pagename):
                page = self.wiki.pages.get(pagename)
                print page[:20]
            else:
                raise
        except Exception as e:
            print "wiki url not well formed or page does not exist"
            print e
            return
        try:
            title = self.h1regex.match(page).group(1)
            print title
        except:
            print "page title not found. wiki page not formated correctly."
            return
        try:    
            self.dbcursor.execute("INSERT INTO Inventory VALUES (?, ?, ?)", (number, title, folder))
            self.db.commit()
        except sqlite3.IntegrityError:
            print "adding failed, most likely entry already exists. trying to update"
            try:
                self.dbcursor.execute("UPDATE Inventory SET Title = ?, Folder = ? WHERE Number = ?", (title, folder, number)) 
                self.db.commit()
            except Exception as e:
                print "Update failed"

    def NamespaceFromUrl(self, url):
        parts = url.split('/')[3:]
        if len(parts) > 2:
            folder = parts[1:-1]
        else:
            folder = []
        print parts, folder
        return (':'.join(parts), ':'.join(folder))

    def ClearDB(self):
        self.dbcursor.execute("DELETE FROM Inventory")

    def GetAllItems(self):
        self.dbcursor.execute("SELECT Number, Title FROM Inventory ORDER BY Number")
        return self.dbcursor.fetchall()

    def GetFolders(self):
        self.dbcursor.execute("SELECT DISTINCT Folder FROM Inventory ORDER BY Folder")
        return self.dbcursor.fetchall()

    def ExistsItem(self, number):
        self.dbcursor.execute("SELECT count(*) FROM Inventory WHERE Number = ?", (number,))
        count = self.dbcursor.fetchone()[0]
        return count != 0

    def AddNewItem(self, number, title, subfolder):
        shorturl = self.prefix + format(number, "04")
        print_re = re.compile('[\W_]+')#, re.UNICODE)
        try:
            self.yourls.expand(shorturl)
            urlexists = True
        except:
            urlexists = False
        if not urlexists:
            with open('wiki-template.txt','r') as s:
                template = s.read()
            template = template.replace("%title%", title)
            template = template.replace("%number%", shorturl)
            wikified_title = print_re.sub("_", title).lower()
            if wikified_title[-1] == "_":
                wikified_title = wikified_title[:-1]
            new_wiki_name = ":".join(["playground", self.wiki_basefolder, subfolder, wikified_title])
            print new_wiki_name
            if not self.wiki.pages.info(new_wiki_name):
                self.wiki.pages.set(new_wiki_name, template)
                new_wiki_url = "/".join([self.wikiurl, new_wiki_name.replace("::",":").replace(":","/")])
                print new_wiki_url
                self.yourls.shorten(new_wiki_url, shorturl)
                self.RetrieveItemInfo(number)
            else:
                print "page ", new_wiki_name, "already exists"


if __name__ == "__main__":
    yourlsurl = 'http://hshb.de/yourls-api.php'
    with open('yourls-signature.txt','r') as s:
        sig = s.read().strip()

    wikiurl = 'https://wiki.hackerspace-bremen.de'
    user = 'heth'
    pw = getpass.getpass('Passwort: ')

    inv = InventoryItemList(yourlsurl, sig, wikiurl, user, pw, "test.db")
    for i in range(1, 110):
        inv.RetrieveItemInfo(i)
    inv.RetrieveItemInfo(1234)
    inv.RetrieveItemInfo(1235)
    print inv.GetAllItems()
    print inv.GetFolders()
