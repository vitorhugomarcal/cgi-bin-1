#!/usr/bin/python
import socket, time, cgi, os, websocket, json, datetime, MySQLdb

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

print "Content-type:text/html\r\n\r\n"
print "<html>"



print "<pre>"


ws=websocket.WebSocket()
ws.connect("ws://127.0.0.1:8479")

args=os.environ["QUERY_STRING"]
ip=args.split("=")[1]

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (ip,3001)
tcp.connect(dest)


tcp.send(" I=1 N\r")
time.sleep(1)
tcp.send(" I=1 0\r")
time.sleep(1)

try:
	ws.send(json.dumps({"text":"UnBuffer: "+tcp.recv(1024)}))
except:
	print "Problemas com UnBuffer"

ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Iniciando a Carga do Painel"}))

ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 1/6 - (Comando Inicial)..."}))

sql = "SELECT comando FROM comando_inicial"
cursor.execute(sql)
resultado = cursor.fetchall()
for r in resultado:
	ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Comando Inicial "+str(r[0])}))
	tcp.send(" I=1 " + str(r[0]) + "\r")
	time.sleep(0.5)
	ws.send(json.dumps({"text":tcp.recv(1024)}))




ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 2/6 - (Formato do Cartao)..."}))

sql = "SELECT id,cardformat FROM cardformat"
cursor.execute(sql)
resultado = cursor.fetchall()
for r in resultado:
	ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Formato do Cartao "+str(r[0])+ " - "+str(r[1])}))
	tcp.send(" F=1 " + str(r[0]) + " " + str(r[1]) + "\r")
	time.sleep(0.5)
	ws.send(json.dumps({"text":tcp.recv(1024)}))



ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 3/6 - TimeZones..."}))


sql = "SELECT id,timezones FROM timezones"
cursor.execute(sql)
resultado = cursor.fetchall()
for r in resultado:
	ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Timezones "+str(r[0])+ " - "+str(r[1])}))
	tcp.send(" L=1 " + str(r[0]) + " " + str(r[1]) + " 1 2 3 4 5 6 7 0;0\r")
	time.sleep(0.5)
	ws.send(json.dumps({"text":tcp.recv(1024)}))



ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 4/6 - Data Atual..."}))
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Data Atual: "+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().day)+ " " + str(datetime.datetime.today().weekday()+1) + " " + str(datetime.datetime.now().year)}))
tcp.send(" D=1 "+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().day)+ " " + str(datetime.datetime.today().weekday()+1) + " " + str(datetime.datetime.now().year) +"\r")
time.sleep(0.5)
ws.send(json.dumps({"text":tcp.recv(1024)}))

ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 5/6 - Hora Atual..."}))
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Hora Atual: "+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)}))
tcp.send(" T=1 "+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+"\r")
time.sleep(0.5)
ws.send(json.dumps({"text":tcp.recv(1024)}))

####EM ANDAMENTO
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 6/6 - Crachas..."}))
#
#
sql = "SELECT f.cracha, t.id as timezone, sum(case a.num_leitor when 1 then 1 else 0 end) as leitor1, sum(case a.num_leitor when 2 then 2 else 0 end) as leitor2, sum(case a.num_leitor when 3 then 3 else 0 end) as leitor3, sum(case a.num_leitor when 4 then 4 else 0 end) as leitor4 FROM wfp.controladora c,wfp.cadastro_funcionarios f,wfp.timezones t,wfp.areas a where f.id_timezones = t.id and f.nome_area = a.nome_area and a.id_controladora = c.id and c.ip='"+ip+"' group by f.cracha, t.id"
cursor.execute(sql)
resultado = cursor.fetchall()

if len(resultado)>0:
	for r in resultado:
		ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Cracha "+str(r[0])+ " - Timezones: "+str(r[1]) + "Leitores: "+str(r[2])+" "+str(r[3])+" "+str(r[4])+" "+str(r[5])}))
		timezone = " "+str(r[1])
		cracha = str(r[0])

		if (str(r[2])=="1"):
			l1 = " 1"
		else:
			l1 = " "
		if (str(r[3])=="2"):
			l2 = " 2"
		else:
			l2 = " "
		if (str(r[4])=="3"):
			l3 = " 3"
		else:
			l3 = " "
		if (str(r[5])=="4"):
			l4 = " 4"
		else:
			l4 = " "

		ws.send(json.dumps({"text":" C=0 "+cracha+" "+timezone+timezone+timezone+timezone+l1+l2+l3+l4}))

		tcp.send(" C=0 "+cracha+timezone+timezone+timezone+timezone+l1+l2+l3+l4+"\r")
		time.sleep(0.5)
		ws.send(json.dumps({"text":tcp.recv(1024)}))

else:
	ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Base de Crachas Vazia no Banco de Dados !"}))




ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Carga Completa!!!"}))

cursor.close()
db.close()
tcp.close()
ws.close()
print "</pre>"
print "</html>"
