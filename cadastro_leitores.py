#!/usr/bin/python
import cgi, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"

print "<head>"

print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"
print "<script src='../js/bootstrap.min.js'></script>"

print "</head>"

arg = cgi.FieldStorage()
id_controladora = arg.getvalue("controladora")
num_leitor = arg.getvalue("leitor")
baixa = arg.getvalue("baixa")
nome = arg.getvalue("nome")

#print "ID Controladora: " + id_controladora + "<br>"
#print "Leitor: " + num_leitor + "<br>"
#print "Nome: " + nome + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

if (nome==""):
	print "Entrei no IF"
	sql = "insert into leitores (id_controladora, num_leitor, leitor_baixa, datref) values ('" + id_controladora + "'," + num_leitor + ",'" + baixa + "',now()) on duplicate key update leitor_baixa='" + baixa + "',datref=now()"
else:
	print "Entrei no else"
	sql = "insert into leitores (id_controladora, num_leitor, leitor_baixa, nome, datref) values ('" + id_controladora + "'," + num_leitor + ",'" + baixa + "','" + nome + "',now()) on duplicate key update leitor_baixa='" + baixa + "',nome='" + nome + "',datref=now()"
print sql
cursor.execute(sql)
db.commit()
cursor.close()
db.close()


print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>O registro foi inserido com exito na base de dados !<br><br>ID Controladora: "+id_controladora+"<br>Leitor: "+num_leitor+"<br>Nome: "+nome+"<br>"
print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_leitores.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"
print "</html>"

