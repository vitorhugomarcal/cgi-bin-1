#!/usr/bin/python
import cgi, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"

print "<head>"

print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"
print "<script src='../js/bootstrap.min.js'></script>"

print "</head>"

arg = cgi.FieldStorage()
formato = arg.getvalue("formato")

comando = "B M " + formato + " Z 0"

#print "Comando Inicial: " + formato + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

sql = "truncate table comando_inicial"
cursor.execute(sql)
sql = "insert into comando_inicial (comando, datref) values ('" + comando + "',now())"
cursor.execute(sql)
db.commit()
cursor.close()
db.close()

print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>Comando inserido com sucesso no Bando de Dados! <br>"
print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_comando_inicial.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"
print "</html>"

