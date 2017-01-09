#!/usr/bin/python
import cgi, cgitb, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"
arg = cgi.FieldStorage()
formato = arg.getvalue("formato")

comando = "B M " + formato + " Z 0"

print "Comando Inicial: " + formato + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

sql = "truncate table comando_inicial"
cursor.execute(sql)
sql = "insert into comando_inicial (comando, datref) values ('" + comando + "',now())"
cursor.execute(sql)
db.commit()
cursor.close()
db.close()

print "<a href='/cadastro_comando_inicial.php'>Voltar</a>"

print "</html>"
