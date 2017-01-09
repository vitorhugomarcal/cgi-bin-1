#!/usr/bin/python
import cgi, cgitb, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"
arg = cgi.FieldStorage()
ip_controladora = arg.getvalue("ip_controladora")
nome = arg.getvalue("nome")

print "IP Controladora: " + ip_controladora + "<br>"
print "Nome: " + nome + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

sql = "insert into controladora (ip, nome, datref) values ('" + ip_controladora + "','" + nome + "',now())"
cursor.execute(sql)
db.commit()

sql = "select id from controladora where ip = '" + ip_controladora + "' and nome = '" + nome + "'"
cursor.execute(sql)
resultado = cursor.fetchall()
for r in resultado:
	id = str(r[0])

for i in range(4):
	leitor=i+1
	sql = "insert into leitores (id_controladora, num_leitor, nome, datref) values (" + id + "," + str(leitor) + ",'Sem Nome',now())"
	cursor.execute(sql)

db.commit()
cursor.close()
db.close()


print "</html>"
