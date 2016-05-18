import sys
import getpass
# from dokuwiki import DokuWiki, DokuWikiError
import dokuwiki

baseurl = 'https://wiki.hackerspace-bremen.de'
user = 'heth'
pw = getpass.getpass('Passwort: ')

try:
    wiki = dokuwiki.DokuWiki(baseurl, user, pw)
except (dokuwiki.DokuWikiError, Exception) as err:
    print 'unable to connect: ' , err
    sys.exit(1)

print wiki.version # => 'Release 2012-10-13 "Adora Belle"'
# print wiki.pages.list() # list all pages of the wiki
print wiki.pages.list('geraetschaften:infrastruktur') # list all pages in the given namespace
print wiki.pages.get('geraetschaften:infrastruktur:dymo') # print the content of the page


with open('wiki-template.txt','r') as s:
    template = s.read()

wiki.pages.set('playground:neuerordner:inventartest',template)
print wiki.pages.info('playground:neuerordner:inventartest')
if wiki.pages.info('playground:neuerordner:inventartestttt'):
    print "existiert"
else:
    print "existiert nicht"

