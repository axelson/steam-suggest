#!/usr/bin/python
import re
import cgi
import urllib

print "Content-type: text/html\n\n"
print "<br><br>"

# Profiles
bostonvaulter = "76561197973312035"
jibbers = "76561197977685020"
positron = "positrons"

defaultSteamId = "defaultvalue"

form = cgi.FieldStorage()
steamid = form.getvalue("steamid", defaultSteamId)
filter = form.getvalue("filter", "(no message)")

url = "default"
if steamid == defaultSteamId:
    f = open('mypage.html')
    text = f.read()
else:
    # Need to use /profiles for numerical ids
    # Need to use /id for custon id's
    url = 'http://steamcommunity.com/profiles/' + steamid + '/games?tab=all'
    text = urllib.urlopen(url).read()

games = re.findall("rgGames\[.*= '(.*)';", text)

#if they set up their own id then use /id if they're using a profile number than use /profiles

print "Checking url: " + url
print """

<p>Checking steamid: %s</p>

<p>form

<form method="post" action="site.py">
<p>steamid: <input type="text" name="steamid"/></p>
<p>filter: <input type="text" name="filter"/></p>
<input type="submit" />
</form>

</body>

</html>
""" % cgi.escape(steamid)

print "Of the games you own, the following games match (" + filter + "):"
print "<br>"

for game in games :
    if re.search(filter, game) :
        print game
        print "<br>"
