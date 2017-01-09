#!/usr/bin/python
import cgi, cgitb, MySQLdb, socket

print "Content-type:text/html\r\n\r\n"
print "<html>"

arg = cgi.FieldStorage()
nome = arg.getvalue("nome")
cracha = arg.getvalue("cracha")

print "Nome: " + nome + "<br>"
print "Cracha: " + cracha + "<br>"

print "</html>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()
sql = "insert into cracha select " + cracha + ",'" + nome + "'"
cursor.execute(sql)
db.commit()
cursor.close()
db.close()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = ("192.168.1.245",3001)
tcp.connect(dest)
tcp.send(" C=1 " + cracha + " 3 3 3 3 1 2 3 4\r")
tcp.close()


