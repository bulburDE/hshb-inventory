# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import yourls
import sqlite3

baseurl = 'http://hshb.de/yourls-api.php'
with open('yourls-signature.txt','r') as s:
    sig = s.read().strip()

class InventoryItemList:
    def __init__(self, baseurl, signature, dbname):
        self.prefix = "g"
        self.yourls = yourls.YOURLSClient(baseurl, signature=signature)
        self.db = sqlite3.connect(dbname)
        self.dbcursor = self.db.cursor()
        self.dbcursor.execute("""CREATE TABLE IF NOT EXISTS Inventory 
                              (Number INT NOT NULL, Title TEXT NOT NULL, ShortUrl TEXT NOT NULL, WikiUrl TEXT NOT NULL)""")
        self.db.commit()

    def Add(self, number):
        pass

if __name__ == "__main__":
    inv = InventoryItemList(baseurl, sig, "test.db")
