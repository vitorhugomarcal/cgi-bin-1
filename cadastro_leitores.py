#!/usr/bin/python
import cgi, cgitb, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"

arg = cgi.FieldStorage()
id_controladora = arg.getvalue("controladora")
num_leitor = arg.getvalue("leitor")
nome = arg.getvalue("nome")

print "ID Controladora: " + id_controladora + "<br>"
print "Leitor: " + num_leitor + "<br>"
print "Nome: " + nome + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()
sql = "insert into leitores (id_controladora, num_leitor, nome, datref) values ('" + id_controladora + "'," + num_leitor + ",'" + nome + "',now()) on duplicate key update nome='" + nome + "',datref=now()"
print sql
cursor.execute(sql)
db.commit()
cursor.close()
db.close()

print "<br><a href='/cadastro_leitores.php'>Voltar</a>"
print "</html>"
