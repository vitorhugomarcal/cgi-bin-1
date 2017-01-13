#!/usr/bin/python
import cgi, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"

print "<head>"

print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"
print "<script src='../js/bootstrap.min.js'></script>"

print "</head>"


arg = cgi.FieldStorage()
ip_dvr = arg.getvalue("ip_dvr")
marca = arg.getvalue("marca_dvr")
nome = arg.getvalue("dvr")
canais = arg.getvalue("canais")


#print "IP DVR: " + ip_dvr + "<br>"
#print "Marca: " + marca + "<br>"
#print "Nome: " + nome + "<br>"
#print "Canais: " + canais + "<br>"


db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

try:
	sql = "insert into dvr (ip, marca, nome,canais, datref) values ('" + ip_dvr + "','" + marca + "','" + nome + "',"+ str(canais) +",now())"
	cursor.execute(sql)
	db.commit()
except:
	print "Erro ao gravar registro !"

sql = "select id, canais from dvr where ip = '" + ip_dvr + "' and nome = '" + nome + "'"
cursor.execute(sql)

resultado = cursor.fetchall()
for r in resultado:
	id = str(r[0])
	canais = r[1]

for i in range(canais):
	canal=i+1
	sql = "insert into cameras (id_dvr, num_canal, nome, datref) values (" + id + "," + str(canal) + ",'Sem Nome',now())"
	#print i
	cursor.execute(sql)

db.commit()
cursor.close()
db.close()

print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>DVR: <b>"+marca+"</b><br><br>Inserido com sucesso no Bando de Dados! <br>"
print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_dvr.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"
print "</html>"
