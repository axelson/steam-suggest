#!/usr/bin/python
import re
import cgi
import urllib

print "Content-type: text/html\n\n"
print "<br><br>"

form = cgi.FieldStorage()
steamid = form.getvalue("steamid", "defaultvalue")
filter = form.getvalue("filter", "(no message)")

if steamid == "defaultvalue":
    f = open('mypage.html')
    text = f.read()
else:
    text = urllib.urlopen('http://steamcommunity.com/profiles/76561197973312035/games?tab=all').read()

games = re.findall("rgGames\[.*= '(.*)';", text)

print """

<p>Previous message: %s</p>

<p>form

<form method="post" action="site.py">
<p>steamid: <input type="text" name="steamid"/></p>
<p>filter: <input type="text" name="filter"/></p>
<input type="submit" />
</form>

</body>

</html>
""" % cgi.escape(steamid)

print "Hello, of the games you own, the following games match (" + filter + "):"
print "<br>"

for game in games :
    if re.search(filter, game) :
        print game
        print "<br>"
