#!/usr/bin/python
import cgi, cgitb,base64, urllib2, random, datetime
print "Content-type: text/html"
print


arg = cgi.FieldStorage()
ip = arg.getvalue("ip")
canal = arg.getvalue("canal")

#ip="191.255.154.159"
#canal="1"

request = urllib2.Request("http://"+ip+":8077/cgi-bin/snapshot.cgi?channel="+canal)
base64string = base64.encodestring('%s:%s' % ('demo', 'demo')).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

nomarq = "foto-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".jpg"

f=open("/var/www/html/fotos/"+nomarq,"w")
f.write(result.read())
f.close()

print nomarq+"<br><center><img src='../fotos/"+nomarq+"'></center>"
