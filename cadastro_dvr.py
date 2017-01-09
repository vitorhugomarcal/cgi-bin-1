#!/usr/bin/python
import cgi, cgitb, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"
arg = cgi.FieldStorage()
ip_dvr = arg.getvalue("ip_dvr")
marca = arg.getvalue("marca_dvr")
nome = arg.getvalue("dvr")
canais = arg.getvalue("canais")


print "IP DVR: " + ip_dvr + "<br>"
print "Marca: " + marca + "<br>"
print "Nome: " + nome + "<br>"
print "Canais: " + canais + "<br>"


db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

sql = "insert into dvr (ip, marca, nome,canais, datref) values ('" + ip_dvr + "','" + marca + "','" + nome + "',"+ str(canais) +",now())"
cursor.execute(sql)
db.commit()

sql = "select id, canais from dvr where ip = '" + ip_dvr + "' and nome = '" + nome + "'"
cursor.execute(sql)

resultado = cursor.fetchall()
for r in resultado:
	id = str(r[0])
	canais = r[1]

for i in range(canais):
	canal=i+1
	sql = "insert into cameras (id_dvr, num_canal, nome, datref) values (" + id + "," + str(canal) + ",'Sem Nome',now())"
	print i
	cursor.execute(sql)

db.commit()
cursor.close()
db.close()

print "<br><a href='/cadastro_dvr.php'>Voltar</a>"
print "</html>"
