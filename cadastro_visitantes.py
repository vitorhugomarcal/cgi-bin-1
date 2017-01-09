#!/usr/bin/python
import cgi, cgitb, MySQLdb, socket, time, datetime, random

print "Content-type:text/html\r\n\r\n"
print "<html>"
arg = cgi.FieldStorage()
nome = arg.getvalue("nome")
cracha = arg.getvalue("cracha")
controladora = arg.getvalue("controladora")
ativo = arg.getvalue("ativo")

print "Nome: " + nome + "<br>"
print "Cracha: " + cracha + "<br>"
print "Controladora: " + controladora + "<br>"
print "Ativo: " + ativo + "<br>"


db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()
sql = "insert into cadastro_visitantes select " + cracha + ",'" + nome + "',1,'" + ativo + "',now()"
cursor.execute(sql)
db.commit()

try:
	if (controladora=="Todas"):
		sql = "select ip from controladora"
		cursor.execute(sql)
		resultado = cursor.fetchall()
		for r in resultado:
			arq = "fila/"+ str(r[0])  +"-fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
			print "Arquivo: " + arq + " criado com sucesso!<br>"
			f=open(arq,"w")
			f.write(cracha)
			f.close()

	else:
		arq = "fila/" + str(controladora) + "-fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
		print "Arquivo: " + arq + " criado com sucesso!<br>"
                f=open(arq,"w")
                f.write(cracha)
                f.close()

except:
	print "Erro gravando arquivo: ", arq

cursor.close()
db.close()


print "</html>"
