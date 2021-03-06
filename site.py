#!/usr/bin/python
import re
import cgi
import urllib
import shelve
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
    genreBlock = soup.find(text='Genre:')
    if(genreBlock == None):
        return genres
    detailsBlock = genreBlock.parent.parent
    genreTags = detailsBlock.findAll(href=re.compile('genre'))
    for genre in genreTags :
        genres.append( genre )

    return genres

def getBadges( soup ):
    """Get the badges/icons that represent features of a game"""
    gameDetails = soup.findAll("div", { "class" : "game_area_details_specs" })

    badges = []
    for detail in gameDetails :
        image = detail.img
        description = detail.find("div", { "class" : "name" }).text
        badge = Badge(image, description)
        badges.append(badge)

    return badges

def getGameName( soup ):
    gameDetails = soup.findAll("div", { "class" : "game_area_details_specs" })

    title = soup.find(text='Title:').next
    return title

def printGameDetails( soup ):
    print getGameName( soup ) + ": "
    for badge in getBadges( soup ):
        print badge.image
    print getGenres( soup )

class Badge:
    def __init__(self, image, description):
        self.image = image
        self.description = description
        self.image["title"] = description

class Game:
    def __init__(self, name):
        self.name = name
        self.hoursPlayed = 0
    def sayHi(self):
        print 'Hi there, this is' + self.name
    def printDetails(self):
        print "%s: %s hours" % (self.name, self.hoursPlayed)
    def addInfo(self):
        print "adding info to game: " + self.name + "<br>"
        html = getGameHtml(self)
        if(html == None):
            return
        soup = BeautifulSoup( html )
        self.genres = getGenres( soup )
        self.badges = getBadges( soup )

def parseGameList( allGameSoup ):
    """Get the time played for each game from the all games page/tab"""
    print "start parseGameList"
    games = []
    gamesTagList = allGameSoup.findAll("div", { "class" : "gameListRowItem" })
    for gameTag in gamesTagList:
        print "\n"
        gameName = gameTag.h4.text
        game = Game(gameName)
        game.logo = gameTag.parent.img
        game.href = gameTag.parent.a['href']
        game.addInfo()
        hoursPlayedStr = gameTag.h5.text
        index = hoursPlayedStr.find(' hrs')
        if( index != -1 ):
            hoursPlayed = float(hoursPlayedStr[:index])
            game.hoursPlayed = hoursPlayed
        games.append(game)
    return games

def getGameHtml( game ):
    print "Getting html for game: " + game.name + "<br>"
    print "Getting html for url: " + game.href + "<br>"
    # Convert to ascii
    url = game.href.encode('ascii', 'ignore')
    print "Getting html for url: " + url + "<br>"
    gameCache = shelve.open("gameCache")
    if( gameCache.has_key(url) ):
        print "cached html<br>"
        html = gameCache[url]
    else:
        print "downloading html<br>"
        urlObj = urllib.urlopen(url)
        if(urlObj.geturl() != url):
            print " We now need to pass the age verification"
            print "new url: " + urlObj.geturl()
            form = dict(ageDay="1", ageMonth="January", ageYear="1970")
            htmlUrl = urllib.urlopen(urlObj.geturl(), urllib.urlencode(form))
            html = htmlUrl.read()
            html = None
        else:
            html = urlObj.read()
            gameCache[url] = html


    #soup = BeautifulSoup(html)
    #if(len(soup.findAll(text="Please enter your birth date to continue:")) > 0):
    #    print "stuck behind date wall"
    gameCache.close()
    return html

print "About to print game details<br>"
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

soup = BeautifulSoup(text)

gameList = parseGameList( soup )
print "<br>href: " + gameList[0].href + "<br><br>"

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

for game in gameList :
    print "<li>"
    print game.logo
    print game.name
    print "</li>"

print """
</ul>
</body>

</html>
"""
