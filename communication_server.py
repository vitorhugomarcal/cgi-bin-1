#!/usr/bin/python
import socket, time, MySQLdb, glob, os, sys, websocket, datetime, json

ip=sys.argv[1]



ws=websocket.WebSocket()
ws.connect("ws://127.0.0.1:8479")

ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): iniciado..."}))


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (ip,3001)
tcp.connect(dest)

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

lista=[]
lista_leitores_baixa = []


sql = "SELECT l.num_leitor FROM leitores l, controladora c WHERE l.leitor_baixa = 's' and c.ip='"+ip+"' and c.id = l.id_controladora"
cursor.execute(sql)
resultado = cursor.fetchall()
for r in resultado:
	lista_leitores_baixa.append(r[0])


contador = 1

while True:

#########Inicio do Processo de Fila
	files = glob.glob("fila/"+ip+"-fila-*.txt")
	files.sort(key=os.path.getmtime)
	for name in files:
		print "Nome: ***** ",name
		ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): Nome "+name}))

		with open(name) as f:
			content = f.read().splitlines()
			for w in content:
				#reg = " C=0 " + w.replace("\r\n","") + " 3 3 3 3 1 2 3 4\r"
				reg = w.replace("\r\n","") + "\r"
				print " Inserindo registro na placa: ",reg
				ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): Inserindo registro na placa "+reg}))

				tcp.send(reg)
				time.sleep(0.5)
				print tcp.recv(4096)

		print "Removendo arquivo :",name
		ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): Removendo arquivo "+name}))

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
					ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): Cracha: "+ l[11:23] + " Status:<font style='color:red'> Acesso Negado</font> - Leitor: #"+str(leitor)}))
					sql = "insert into log select " + l[11:23] + ",'" + l[25:27] + "','"+ ip +"',"+str(leitor)+", now()"
					
					try:
						cursor.execute(sql)
						db.commit()
						ws.send(json.dumps({"text":"Event View Atualizado..."}))
					except:
						print "Erro gravando arquivo para cracha negado"

				elif l[19:24] == "RD#01":
					print "ELSEIF----> ",l[29:41]
					

					try:
						#TRATAMENTO ROTINA DE ALARME
						if "ALARM" in l[29:41]:
							print "**** ENTROU NA ROTINA DE ALARME IDENTIFICANDO OUTPUT ACIONADO"
							
							output = l[27:29]
			
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"):<font style='color:orange'> *** Alarme Disparado ***</font> Output: #"+ str(output)}))
					
							sql = "insert into log select 0,'ALARME','"+ ip +"',"+str(output)+", now()"

							#print sql
							cursor.execute(sql)
							db.commit()
						
						#TRATAMENTO DO ERRO #17 PERDA DE CONEXAO
						elif "RD#01  #17" in l:
							print "COMUNICACAO REESTABELECIDA"
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): <font style='color:red'> Comunicacao Perdida, mas ja reestabelecida...</font>"}))
							sql = "insert into log select 0,'PERDA DE COMUNICACAO','"+ ip +"',0, now()"
							cursor.execute(sql)
							db.commit()

						elif "RD#01  #18" in l:
							print "MEMORIA DE CRACHAS CORROMPIDA"
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): <font style='color:red'> Memoria dos crachas corrompida...</font>"}))

						elif "RD#01  #19" in l:
							print "FALHA DE ALIMENTACAO PRIMARIA"
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): <font style='color:red'> Falha de alimentacao primaria, verifique a fonte de alimentacao...</font>"}))

						elif "RD#01  #20" in l:
							print "ALARME DE TAMPER GABINETE VIOLADO"
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): <font style='color:red'> Alarme de Tamper, gabinete violado...</font>"}))

						elif "RD#01  #22" in l:
							print "BAIXA VOLTAGEM Vdd 12V"
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): <font style='color:red'> Baixa Voltagem Vdd 12V os reles nao podem operar...</font>"}))

						elif "RD#01  #23" in l:
							print "BAIXA VOLTAGEM Vcc 5V"
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): <font style='color:red'> Baixa Voltagem Vcc 5V os reles nao podem operar...</font>"}))

						elif "RD#01  #17" in l:
							print "COMUNICACAO REESTABELECIDA"
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): <font style='color:red'> Comunicacao Perdida, mas ja reestabelecida...</font>"}))

						elif "RD#01  #17" in l:
							print "COMUNICACAO REESTABELECIDA"
							ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): <font style='color:red'> Comunicacao Perdida, mas ja reestabelecida...</font>"}))

						else:
							#SE TIVER RD#01 e NAO FOR ALARM
							print "**** ENTROU NA ROTINA NORMAL SEM ALARME"
							
							#####Tratando o numero do leitor "Vazio = 1", "X = 2", "3 e 4 ja recebem o numero 3 ou 4 nao precisa tratar"
							leitor = l[26:27]
					
							if (leitor==" "):
								leitor=1
							elif (leitor=="X"):
								leitor=2
							#####Fim do tratamento dos leitores

							if "NORMAL" in  l[29:41]:
								print "Sistema Normal"
							
							####ROTINA DE CRACHA OK CADASTRADO
							else:
										
								###SE ESTIVER OK E PASSAR NO LEITOR DE BAIXA/URNA
								if leitor in lista_leitores_baixa:
									print "Cracha passou no leitor de Baixa/Urna baixando do Sistema..."
									CrachaDel = int(l[29:41])
									ws.send(json.dumps({"text":"Event View Atualizado..."}))
									ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): Cracha: "+ str(CrachaDel) + " <font style='color:rgb(49,112,143)'> Baixado com Sucesso</font> - Leitor: #"+str(leitor)}))
									
									#DELETANDO DA PLACA
									tcp.send(" C=0 " + str(CrachaDel) + "\r")
									time.sleep(0.5)
									print tcp.recv(1024)

									#DELETANDO DO BANCO DE DADOS
									sql = "delete from cadastro_funcionarios where cracha=" + str(CrachaDel)
									cursor.execute(sql)
									db.commit()

									sql = "delete from cadastro_visitantes where cracha=" + str(CrachaDel)
									cursor.execute(sql)
									db.commit()

								###SE ESTIVER OK E NAOOOO PASSAR NO LEITOR DE BAIXA/URNA
								else:
									
									ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): Cracha: "+ l[29:41] + " Status:<font style='color:green'> Acesso Permitido</font> - Leitor: #"+str(leitor)}))
									sql = "insert into log select " + l[29:41] + ",'OK','"+ ip +"',"+str(leitor)+", now()"
									cursor.execute(sql)
									db.commit()
									ws.send(json.dumps({"text":"Event View Atualizado..."}))
					except:
						print "Erro inserindo registro numerico, continuando..."
				

				else:
					print "ELSE FINAL--->",l
########Fim do processo de UnBuffer

########Inicio do processo de verificacao do servidor a cada 20 rodadas
	if(contador == 20):
		#ATUALIZANDO LEITORES DE BAIXA A CADA 20 Saltos
		sql = "SELECT l.num_leitor FROM leitores l, controladora c WHERE l.leitor_baixa = 's' and c.ip='"+ip+"' and c.id = l.id_controladora"
		cursor.execute(sql)

		lista_leitores_baixa = []

		resultado = cursor.fetchall()
		for r in resultado:
			lista_leitores_baixa.append(str(r[0]))

		#Enviando um ping de On-Line
		ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Communication Server ("+ip+"): Status da Controladora: <font color='green'>On-Line</font>"}))

		#Grava no Banco a ultima atualizacao de on-line
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
ws.close()