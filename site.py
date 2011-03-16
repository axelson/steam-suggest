#!/usr/bin/python
import re
import cgi

print "Content-type: text/html\n\n"
print "Hello, you own the following games:"

print "<br><br>"

f = open('mypage.html')
games = re.findall("rgGames\[.*= '(.*)';", f.read())

for game in games :
    a = 1
    #print game
    #print "<br>"

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
