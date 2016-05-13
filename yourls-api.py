# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import yourls
import getpass

baseurl = 'http://hshb.de/yourls-api.php'
# user = 'heth'
# pw = getpass.getpass('Passwort: ')
with open('yourls-signature.txt','r') as s:
    sig = s.read().strip()

# shortener = yourls.YOURLSClient(baseurl, user, pw)
shortener = yourls.YOURLSClient(baseurl, signature=sig)
print shortener.expand('g0100')
