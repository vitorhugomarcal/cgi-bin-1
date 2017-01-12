#!/usr/bin/python
import cgi, cgitb, MySQLdb, socket, time, datetime, random

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"

print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"
print "<script src='../js/bootstrap.min.js'></script>"

print "</head>"

arg = cgi.FieldStorage()
crachaini = arg.getvalue("crachaini")
crachafim = arg.getvalue("crachafim")
crachaativo = arg.getvalue("crachaativo")

if (crachaativo == "A"):
	crachaativo = 1
else:
	crachaativo = 0

#print "Cracha Inicial: " + crachaini + "<br>"
#print "Cracha Final: " + crachafim + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

try:
	for c in range(int(crachaini), int(crachafim)):
		sql = "insert into visitantes select " + str(c) + ",''," + str(crachaativo) + ",now()"
		cursor.execute(sql)


	print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>O registro foi inserido com exito na base de dados !<br>"

	arq = "fila/fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
	#print arq
	f=open(arq,"w")
	for c in range(int(crachaini), int(crachafim)):
		f.write(" C=0 " + str(c) + " 3 3 3 3 1 2 3 4\r\n")

	f.close()
	print "<center><br>Arquivo "+arq+" gerado com sucesso!<br></center>"


except:
	print "<center><br><br><div style='width:50%;' class='panel panel-danger'><div class='panel-heading'>ERRO!</div><br>Erro ao Gravar no banco de dados ou arquivo na fila !<br>"

db.commit()
cursor.close()
db.close()

print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_cracha_lote.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"

print "</html>"

