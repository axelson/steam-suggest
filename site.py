#!/usr/bin/python
import re

print "Content-type: text/html\n\n"
print "Hello world"

print "<br><br>"

f = open('mypage.html')
m = re.findall("rgGames\[.*= '(.*)';", f.read())

print m
