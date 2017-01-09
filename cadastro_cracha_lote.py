#!/usr/bin/python
import cgi, cgitb, MySQLdb, socket, time, datetime, random

print "Content-type:text/html\r\n\r\n"
print "<html>"

arg = cgi.FieldStorage()
crachaini = arg.getvalue("crachaini")
crachafim = arg.getvalue("crachafim")
crachaativo = arg.getvalue("crachaativo")

if (crachaativo == "A"):
	crachaativo = 1
else:
	crachaativo = 0

print "Cracha Inicial: " + crachaini + "<br>"
print "Cracha Final: " + crachafim + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

try:
	for c in range(int(crachaini), int(crachafim)):
		sql = "insert into visitantes select " + str(c) + ",''," + str(crachaativo) + ",now()"
		cursor.execute(sql)
	print "Registros gravados com Sucesso !"
except:
	print "Erro gravando banco de dados!"

db.commit()
cursor.close()
db.close()

try:
	arq = "fila/fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
	print arq
	f=open(arq,"w")
	for c in range(int(crachaini), int(crachafim)):
		f.write(str(c)+"\r\n")

	f.close()
	print "Arquivo: ", arq, " criando com sucesso !"
except:
	print "Erro gravando arquivo: ", arq


print "</html>"
