#!/usr/bin/python
import cgi, cgitb, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"
arg = cgi.FieldStorage()
formato = arg.getvalue("formato")


print "Timezone: " + formato + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()
sql = "insert into timezones (timezones, datref) values ('" + formato + "',now())"
cursor.execute(sql)
db.commit()
cursor.close()
db.close()

print "<a href='/cadastro_timezones.php'>Voltar</a>"

print "</html>"
