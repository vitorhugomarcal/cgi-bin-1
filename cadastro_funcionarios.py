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
id_func = arg.getvalue("id")
nome = arg.getvalue("nome")
email = arg.getvalue("email")
rg = arg.getvalue("rg")
cpf = arg.getvalue("cpf")
ramal = arg.getvalue("ramal")
#controladora = arg.getvalue("controladora")
ativo = arg.getvalue("ativo")
area = arg.getvalue("area")
timezone = arg.getvalue("timezone")


#print "Nome: " + nome + "<br>"
#print "Cracha: " + cracha + "<br>"
#print "Controladora: " + controladora + "<br>"
#print "Ativo: " + ativo + "<br>"

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

sql = "insert into cadastro_funcionarios select " + cracha + "," + id_func + ",'" + nome + "','" + email + "','" + rg + "','" + cpf + "','" + ramal + "','" + area + "'," + timezone + ",'" + ativo  + "',now()"
cursor.execute(sql)
db.commit()

#try:
if (area=="Todas"):
	sql = "select ip from controladora"
	cursor.execute(sql)
	resultado = cursor.fetchall()
	for r in resultado:
		arq = "fila/"+ str(r[0])  +"-fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
		f=open(arq,"w")
		f.write(" C=0 "+cracha+" "+timezone+" "+timezone+" "+timezone+" "+timezone+" 1 2 3 4")
		f.close()
else:
	sql="select a.ip_controladora,replace(sum(a.leitor1),0,'') as leitor1,replace(sum(a.leitor2),0,'') as leitor2,replace(sum(a.leitor3),0,'') as leitor3,replace(sum(a.leitor4),0,'') as leitor4 from (select c.ip as ip_controladora, (case a.num_leitor when 1 then 1 else '' end) as leitor1, (case a.num_leitor when 2 then 2 else '' end) as leitor2, (case a.num_leitor when 3 then 3 else '' end) as leitor3, (case a.num_leitor when 4 then 4 else '' end) as leitor4 from controladora c, areas a where a.id_controladora = c.id and a.nome_area = '"+area+"') as a group by ip_controladora"
	#print sql
	cursor.execute(sql)
	resultado = cursor.fetchall()
	for r in resultado:
		if (str(r[1])=="1"):
			t1 = " "+timezone
			l1 = " 1"
		else:
			t1 = "" 
			l1 = ""

		if (str(r[2])=="2"):
			t2 = " "+timezone
			l2 = " 2"
		else:
			t2 = "" 
			l2 = ""

		if (str(r[3])=="3"):
			t3 = " "+timezone
			l3 = " 3"
		else:
			t3 = "" 
			l3 = ""

		if (str(r[4])=="4"):
			t4 = " "+timezone
			l4 = " 4"
		else:
			t4 = "" 
			l4 = ""

		arq = "fila/" + str(r[0]) + "-fila-" + str(random.randint(1,999999)) + str(datetime.datetime.now()) + ".txt"
		f=open(arq,"w")
		f.write(" C=0 "+cracha+t1+t2+t3+t4+l1+l2+l3+l4)
		f.close()

#except:
#	print "Erro gravando arquivo: ", arq

cursor.close()
db.close()


print "<center><br><br><div style='width:50%;' class='panel panel-primary'><div class='panel-heading'>Sucesso!</div><br>O registro foi inserido com exito na base de dados !<br>"

print "<nav><ul class='pager'><li class='previous'><a href='../cadastro_funcionarios.php'><span>&larr;</span> Voltar</a></li></ul></nav></div></center>"



print "</html>"
