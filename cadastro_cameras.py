#!/usr/bin/python
import cgi, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"

print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"
print "<script src='../js/bootstrap.min.js'></script>"

print "</head>"

arg = cgi.FieldStorage()
id_dvr = arg.getvalue("dvr")
num_canal = arg.getvalue("camera")
nome = arg.getvalue("nome")

#print "ID DVR: " + id_dvr + "<br>"
#print "Camera Canal: " + num_canal + "<br>"
#print "Nome: " + nome + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()
sql = "insert into cameras (id_dvr, num_canal, nome, datref) values ('" + id_dvr + "'," + num_canal + ",'" + nome + "',now()) on duplicate key update nome='" + nome + "',datref=now()"
#print sql
cursor.execute(sql)
db.commit()
cursor.close()
db.close()



print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>O registro foi inserido com exito na base de dados !<br><br>"
print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_cameras.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"
print "</html>"
