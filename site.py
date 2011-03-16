#!/usr/bin/python
import re

print "Content-type: text/html\n\n"
print "Hello, you own the following games:"

print "<br><br>"

f = open('mypage.html')
games = re.findall("rgGames\[.*= '(.*)';", f.read())

for game in games :
    print game
    print "<br>"
