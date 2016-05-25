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
        self.h1regex = re.compile("={6}\s(.+?)\s={6}")
        self.yourls = yourls.YOURLSClient(yourlsurl, signature=yourlssig)
        self.db = sqlite3.connect(dbname)
        self.dbcursor = self.db.cursor()
        self.dbcursor.execute("""CREATE TABLE IF NOT EXISTS Inventory 
                              (Number INT UNIQUE NOT NULL, Title TEXT NOT NULL)""")
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
            pagename = self.NamespaceFromUrl(wikiurl)
            print pagename
            if self.wiki.pages.info(pagename):
                page = self.wiki.pages.get(pagename)
                print page[:20]
            else:
                raise
        except:
            print "wiki url not well formed or page does not exist"
            return
        try:
            title = self.h1regex.match(page).group(1)
            print title
        except:
            print "page title not found. wiki page not formated correctly."
            return
        try:    
            self.dbcursor.execute("INSERT INTO Inventory VALUES (?, ?)", (number, title))
            self.db.commit()
        except sqlite3.IntegrityError:
            print "adding failed, most likely entry already exists"

    def NamespaceFromUrl(self, url):
        return ':'.join(url.split('/')[3:])

    def GetAllItems(self):
        self.dbcursor.execute("SELECT * FROM Inventory ORDER BY Number")
        return self.dbcursor.fetchall()

    def AddNewItem(self, number, title):
        shorturl = self.prefix + format(number, "04")
        try:
            self.yourls.expand(shorturl)
            urlexists = True
        except:
            urlexists = False
        if not urlexists:
            with open('wiki-template.txt','r') as s:
                template = s.read()
            template.replace("%title%", title)
            template.replace("%number%", shorturl)
            pass


if __name__ == "__main__":
    yourlsurl = 'http://hshb.de/yourls-api.php'
    with open('yourls-signature.txt','r') as s:
        sig = s.read().strip()

    wikiurl = 'https://wiki.hackerspace-bremen.de'
    user = 'heth'
    pw = getpass.getpass('Passwort: ')

    inv = InventoryItemList(yourlsurl, sig, wikiurl, user, pw, "test.db")
    # for i in range(1, 110):
    #     inv.RetrieveItemInfo(i)
    # inv.RetrieveItemInfo(1234)
    # inv.RetrieveItemInfo(1235)
    print inv.GetAllItems()
