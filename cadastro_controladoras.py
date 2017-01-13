#!/usr/bin/python
import cgi, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"

print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"
print "<script src='../js/bootstrap.min.js'></script>"

print "</head>"



arg = cgi.FieldStorage()
ip_controladora = arg.getvalue("ip_controladora")
nome = arg.getvalue("nome")

#print "IP Controladora: " + ip_controladora + "<br>"
#print "Nome: " + nome + "<br>"

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

print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>Controladora: <b>"+nome+ "</b><br> IP: <b>"+ip_controladora+"</b><br><br>Inserida com sucesso no Bando de Dados! <br>"
print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_controladoras.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"
print "</html>"

