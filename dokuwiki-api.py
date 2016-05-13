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

# import xmlrpclib
# import base64
# from urllib import urlencode
# from urllib2 import urlopen
# from urllib2 import HTTPError


# script = '/lib/exe/xmlrpc.php'

# print urlopen(baseurl + script +'?').read()

# url = ''.join([ baseurl, script, '?',urlencode({'u': user, 'p':pw}) ])

# xmlrpclib.Transport.user_agent = 'Thomas'
# xmlrpclib.SafeTransport.user_agent = 'Thomas'

# proxy = xmlrpclib.ServerProxy(url)

# proxy.dokuwiki.getVersion()
