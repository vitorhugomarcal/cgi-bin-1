#!/usr/bin/python
import socket, time, MySQLdb, glob, os, sys

ip=sys.argv[1]

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (ip,3001)
tcp.connect(dest)

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

lista=[]

contador = 1

while True:

#########Inicio do Processo de Fila
	files = glob.glob("fila/"+ip+"-fila-*.txt")
	files.sort(key=os.path.getmtime)
	for name in files:
		print "Nome: ***** ",name
		with open(name) as f:
			content = f.read().splitlines()
			for w in content:
				#reg = " C=0 " + w.replace("\r\n","") + " 3 3 3 3 1 2 3 4\r"
				reg = w.replace("\r\n","") + "\r"
				print " Inserindo registro na placa: ",reg
				tcp.send(reg)
				time.sleep(0.5)
				print tcp.recv(4096)

		print "Removendo arquivo :",name
		os.remove(name)
#########Fim do Processo de Fila

#########Inicio do Processo de UnBuffer
	print "Comando M=1 R"
	tcp.send(" M=1 R\r")
	time.sleep(0.5)
	lista=tcp.recv(8128)

	for x in lista.split("\x03\x02"):
		for i in x.split("*"):

			if "RD#" in i:
				l=i.replace("\x03\x20M=1 R OK","")
				l=l.replace("\x02","")
				l=l.replace("\x03","")
				leitor = l[8:9]
				print "Esse e o l full: "+l
				if l[1:6] == "RD#01":
					print "IF ",l
					
					#####Tratando o numero do leitor "Vazio = 1", "X = 2", "3 e 4 ja recebem o numero 3 ou 4 nao precisa tratar"
					if (leitor==" "):
						leitor=1
					elif (leitor=="X"):
						leitor=2
					#####Fim do tratamento dos leitores

					sql = "insert into log select " + l[11:23] + ",'" + l[25:27] + "','"+ ip +"',"+str(leitor)+", now()"
					cursor.execute(sql)
					db.commit()
				elif l[19:24] == "RD#01":
					print "ELSEIF----> ",l[29:41]
					

					try:
						if "ALARM" in l[29:41]:
							print "**** ENTROU NA ROTINA DE ALARME IDENTIFICANDO OUTPUT ACIONADO"

							output = l[27:29]
			
							sql = "insert into log select 0,'ALARME','"+ ip +"',"+str(output)+", now()"
							print sql
							cursor.execute(sql)
							db.commit()
						
						else:
							print "**** ENTROU NA ROTINA NORMAL SEM ALARME"
							
							#####Tratando o numero do leitor "Vazio = 1", "X = 2", "3 e 4 ja recebem o numero 3 ou 4 nao precisa tratar"
							leitor = l[26:27]
					
							if (leitor==" "):
								leitor=1
							elif (leitor=="X"):
								leitor=2
							#####Fim do tratamento dos leitores

							sql = "insert into log select " + l[29:41] + ",'OK','"+ ip +"',"+str(leitor)+", now()"
							cursor.execute(sql)
							db.commit()
					except:
						print "Erro inserindo registro numerico, continuando..."
				else:
					print "ELSE ",i
########Fim do processo de UnBuffer

########Inicio do processo de verificacao do servidor a cada 50 rodadas
	if(contador == 20):
		print "Entrou no loop de 20 vezes do contador"
		sql = "insert into server_status (ip, datref) values ('" + ip + "',now()) on duplicate key update datref=now()"
		cursor.execute(sql)
		db.commit()
		contador = 1
	else:
		print "Contador: " + str(contador)
########Fim do processo de verificacao do servidor a cada 50 rodadas

########Fim do Loop adicionar mais 1 ao contador e Aguardar 10 segundos para recomecar o fluxo do while 
	contador = contador + 1
	time.sleep(10)
#######Fim do Loop

cursor.close()
db.close()
tcp.close()
