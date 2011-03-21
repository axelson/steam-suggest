#!/usr/bin/python
import re
import cgi
import urllib

print "Content-type: text/html\n\n"
print "<html>"
print "<head><title>Steam Suggest</title>"

print """

    <link rel="stylesheet" href="jquery/common.css" type="text/css" media="screen" />
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
    <script type="text/javascript" src="jquery/quicksilver.js"></script>
    <script type="text/javascript" src="jquery/jquery.livesearch.js"></script>
    <script type="text/javascript" charset="utf-8">
      $(document).ready(function() {
          $('#q').liveUpdate('#posts').focus();
          });
    </script>

</head>
<body>

  <div id="wrapper">
    <p><a href="http://orderedlist.com/articles/live-search-with-quicksilver-style/">&laquo; Back to Article</a> - <a href="http://orderedlist.com/demos/quicksilverjs/">See Prototype Version</a></p>

    <h1>jQuery Live Search with Quicksilver Style</h1>

    <p>Try a few searches like 'jason' and 'wdprss'.</p>

    <form method="get">
      <div>
        <input type="text" value="" name="q" id="q" />
      </div>
    </form>
"""
# Profiles
print "profiles:<br>"
print 'bostonvaulter = 76561197973312035<br>'
bostonvaulter = "76561197973312035"
print 'jibbers = 76561197977685020<br>'
jibbers = "76561197977685020"
print 'positron = positrons<br>'
positron = "positrons"

defaultSteamId = "defaultvalue"
defaultFilter = "defaultFilter"

form = cgi.FieldStorage()
steamid = form.getvalue("steamid", defaultSteamId)
filter = form.getvalue("filter", defaultFilter)

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

""" % cgi.escape(steamid)

print """

Of the games you own, the following games match %(filter)s:
<br>
<ul id="posts">

""" % {"filter": filter }


for game in games :
    if re.search(filter, game) :
        print "<li>"
        print game
        print "</li>"
    elif filter == defaultFilter:
        print "<li>"
        print game
        print "</li>"

print """
</ul>
</body>

</html>
"""
