#!/usr/bin/python
import cgi, cgitb, MySQLdb, socket, time, datetime, random

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"

print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"
print "<script src='../js/bootstrap.min.js'></script>"

print "</head>"

arg = cgi.FieldStorage()
cracha = arg.getvalue("cracha")
id = arg.getvalue("id")
nome = arg.getvalue("nome")
email = arg.getvalue("email")
rg = arg.getvalue("rg")
cpf = arg.getvalue("cpf")
ramal = arg.getvalue("ramal")
controladora = arg.getvalue("controladora")
ativo = arg.getvalue("ativo")

#print "Nome: " + nome + "<br>"
#print "Cracha: " + cracha + "<br>"
#print "Controladora: " + controladora + "<br>"
#print "Ativo: " + ativo + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

sql = "insert into cadastro_funcionarios select " + cracha + "," + id + ",'" + nome + "','" + email + "','" + rg + "','" + cpf + "','" + ramal + "','" + controladora + "','" + ativo  + "',now()"

cursor.execute(sql)
db.commit()

try:
	if (controladora=="Todas"):
		sql = "select ip from controladora"
		cursor.execute(sql)
		resultado = cursor.fetchall()
		for r in resultado:
			arq = "fila/"+ str(r[0])  +"-fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
			#print "Arquivo: " + arq + " criado com sucesso!<br>"
			f=open(arq,"w")
			f.write(cracha)
			f.close()
	else:
		arq = "fila/" + str(controladora) + "-fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
		#print "Arquivo: " + arq + " criado com sucesso!<br>"
                f=open(arq,"w")
                f.write(cracha)
                f.close()

except:
	print "Erro gravando arquivo: ", arq

cursor.close()
db.close()


print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>O registro foi inserido com exito na base de dados !<br>"

print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_funcionarios.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"



print "</html>"
