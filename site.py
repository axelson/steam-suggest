#!/usr/bin/python
import re
import cgi

print "Content-type: text/html\n\n"
print "<br><br>"

f = open('mypage.html')
games = re.findall("rgGames\[.*= '(.*)';", f.read())

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

print """

<p>Previous message: %s</p>

<p>form

<form method="post" action="site.py">
<p>message: <input type="text" name="message"/></p>
</form>

</body>

</html>
""" % cgi.escape(message)

print "Hello, of the games you own, the following games match (" + message + "):"
print "<br>"

for game in games :
    if re.search(message, game) :
        print game
        print "<br>"
