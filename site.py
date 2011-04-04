#!/usr/bin/python
import re
import cgi
import urllib
from BeautifulSoup import BeautifulSoup

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
"""
# Profiles
print "profiles:<br>"
print 'bostonvaulter = <a href="http://steamcommunity.com/profiles/76561197973312035/games?tab=all">76561197973312035</a><br>'
bostonvaulter = "76561197973312035"
print 'jibbers = 76561197977685020<br>'
jibbers = "76561197977685020"
print 'positron = positrons<br>'
positron = "positrons"

defaultSteamId = "defaultvalue"



#oneGameText = urllib.urlopen('http://store.steampowered.com/app/15520').read()
oneGameText = open('gravityGame.html')
oneGameSoup = BeautifulSoup(oneGameText)

def getGenres( soup ):
    gameDetails = soup.findAll("div", { "class" : "game_area_details_specs" })

    genres = []
    detailsBlock = soup.find(text='Genre:').parent.parent
    genreTags = detailsBlock.findAll(href=re.compile('genre'))
    for genre in genreTags :
        genres.append( genre )

    return genres

def getBadges( soup ):
    """Get the badges/icons that represent features of a game"""
    gameDetails = soup.findAll("div", { "class" : "game_area_details_specs" })

    images = []
    for detail in gameDetails :
        images.append(detail.img)

    return images

def getGameName( soup ):
    gameDetails = soup.findAll("div", { "class" : "game_area_details_specs" })

    title = soup.find(text='Title:').next
    return title

def printGameDetails( soup ):
    print getGameName( soup ) + ": "
    print getBadges( soup )
    print getGenres( soup )

class Game:
    def __init__(self, name):
        self.name = name
        self.hoursPlayed = 0
    def sayHi(self):
        print 'Hi there, this is' + self.name
    def printDetails(self):
        print "%s: %s hours" % (self.name, self.hoursPlayed)


def parseGameList( allGameSoup ):
    """Get the time played for each game from the all games page/tab"""
    print "start parseGameList"
    games = []
    gamesTagList = allGameSoup.findAll("div", { "class" : "gameListRowItem" })
    for gameTag in gamesTagList:
        print "\n"
        gameName = gameTag.h4.text
        game = Game(gameName)
        hoursPlayedStr = gameTag.h5.text
        index = hoursPlayedStr.find(' hrs')
        if( index != -1 ):
            hoursPlayed = float(hoursPlayedStr[:index])
            game.hoursPlayed = hoursPlayed
        games.append(game)
    return games


printGameDetails( oneGameSoup )
print "<br>"
braidSoup = BeautifulSoup(open('braid.html'))
printGameDetails( braidSoup )
print "<br>"


form = cgi.FieldStorage()
steamid = form.getvalue("steamid", defaultSteamId)

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

soup = BeautifulSoup(text)
parseGameList( soup )
gameTagList = soup.findAll("div", { "class" : "gameListRow" }, limit=3)
for gameTag in gameTagList :
    print gameTag.renderContents()
#if they set up their own id then use /id if they're using a profile number than use /profiles

print "Checking url: " + url
print """

<p>Checking steamid: %s</p>

<p>form

<form method="post" action="site.py">
<p>steamid: <input type="text" name="steamid"/></p>
<input type="submit" />
</form>

""" % cgi.escape(steamid)

print """

    <p>Try a few searches like 'jason' and 'wdprss'.</p>

    <form method="get">
      <div>
        <input type="text" value="" name="q" id="q" />
      </div>
    </form>

Here are the games you own:
<br>
<ul id="posts">
"""

for game in games :
    print "<li>"
    print game
    print "</li>"

print """
</ul>
</body>

</html>
"""
