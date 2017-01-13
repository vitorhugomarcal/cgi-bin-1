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


#print "Formato: " + formato + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()
sql = "insert into cardformat (cardformat, datref) values ('" + formato + "',now())"
cursor.execute(sql)
db.commit()
cursor.close()
db.close()


print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>Formato inserido com sucesso no Bando de Dados! <br>"
print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_cardformat.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"
print "</html>"
