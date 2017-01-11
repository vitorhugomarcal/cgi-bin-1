#!/usr/bin/python
import cgi, MySQLdb, time, datetime, random

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"

print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"
print "<script src='../js/bootstrap.min.js'></script>"

print "</head>"

arg = cgi.FieldStorage()
cracha = arg.getvalue("d")

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

sql = "delete from cadastro_funcionarios where cracha=" + cracha;

cursor.execute(sql)
db.commit()



try:
	sql = "select ip from controladora"
	cursor.execute(sql)
	resultado = cursor.fetchall()
	for r in resultado:
		arq = "fila/"+ str(r[0])  +"-fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
		#print "Arquivo: " + arq + " criado com sucesso!<br>"
		f=open(arq,"w")
		f.write(" C=0 " + cracha)
		f.close()


	print "<div class='alert alert-success' style='width: 90%' role='alert'>"
	print "<span class='glyphicon glyphicon-ok' aria-hidden='true'></span> Registro Deletado com Sucesso !"
	print "</div>"

except:
	print "Erro gravando arquivo: ", arq

cursor.close()
db.close()

print "</html>"

