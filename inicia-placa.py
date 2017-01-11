#!/usr/bin/python
import socket, time, cgi, os, websocket, json, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"



print "<pre>"

ws=websocket.WebSocket()
ws.connect("ws://127.0.0.1:8479")

args=os.environ["QUERY_STRING"]
ip=args.split("=")[1]

#print "Carga iniciada para placa " + ip + "<br><br>"
ws.send(json.dumps({"text":"Carga iniciada para placa: "+ip}))

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (ip,3001)
tcp.connect(dest)

#print "Inciando carga do Painel..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Iniciando a Carga do Painel"}))

#print "Etapa 1/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 1/9..."}))
tcp.send(" I=1 N\r")
time.sleep(1)

#print "Etapa 2/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 2/9..."}))
tcp.send(" I=1 0\r")
time.sleep(1)

#print "Etapa 3/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 3/9..."}))
tcp.send(" I=1 B M OH Z 0\r")
time.sleep(1)

#print "Etapa 4/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 4/9..."}))
tcp.send(" R=1 p\r")
time.sleep(1)

#print "Etapa 5/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 5/9..."}))
tcp.send(" F=1 1 26 S 1 D 1 B1 B2 B3 B4\r")
time.sleep(1)

#print "Etapa 6/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 6/9..."}))
tcp.send(" F=1 2 32 S 0 D 0 B1 B2 B3 B4\r")
time.sleep(1)

#print "Etapa 7/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 7/9..."}))
tcp.send(" F=1 3 34 S 1 D 1 B1 B2 B3 B4\r")
time.sleep(1)

#print "Etapa 8/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 8/9..."}))
tcp.send(" F=1 4 0 S 0 D 0 B0 B0 B0 B0\r")
time.sleep(1)

#print "Etapa 9/9..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 9/9..."}))
tcp.send(" R=1 o\r")
time.sleep(1)

#print "Inciando carga dos TimeZones..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Inciando carga dos Timezones..."}))

#print "Etapa 1/4..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 1/4..."}))

tcp.send(" L=1 1 06:50-18:00 1 2 3 4 5;63\r")
time.sleep(1)

#print "Etapa 2/4..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 2/4..."}))
tcp.send(" L=1 2 00:00-23:59 1 2 3 4 5;62\r")
time.sleep(1)

#print "Etapa 3/4..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 3/4..."}))
tcp.send(" L=1 3 00:00-23:59 1 2 3 4 5 6 7 0;0\r")
time.sleep(1)

#print "Etapa 4/4..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Etapa 4/4..."}))
tcp.send(" L=1 4 00:00-00:00;0\r")
time.sleep(1)


#print "Carga de Data e Hora..."
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Finalizando com a carga de Data e Hora..."}))

#print "Inserindo a data correta..."
tcp.send(" D=1 12/09 6 2016\r")
time.sleep(1)
#print tcp.recv(1024)

#print "Inserindo a hora correta..."
tcp.send(" T=1 07:09\r")
time.sleep(1)
#print tcp.recv(1024)

time.sleep(1)
#tcp.send(" M=1 X\r")


print "Carga Completa !"
ws.send(json.dumps({"text":"<b>" + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))+"</b> - Carga Completa!!!"}))


#print "Gravando o cracha: 2893980231"
#tcp.send(" C=1 2893980231 3 3 3 3 1 2 3 4\r")
#time.sleep(2)
#print tcp.recv(1024)

tcp.close()
ws.close()
print "</pre>"
print "</html>"
