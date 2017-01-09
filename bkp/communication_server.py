#!/usr/bin/python
import socket, time, MySQLdb, glob, os, sys

ip=sys.argv[1]

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (ip,3001)
tcp.connect(dest)

db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()

lista=[]

while True:


	files = glob.glob("fila/"+ip+"-fila-*.txt")
	files.sort(key=os.path.getmtime)
	for name in files:
		print "Nome: ***** ",name
  		with open(name) as f:
        	        content = f.read().splitlines()
                	for w in content:
       	                	reg = " C=0 " + w.replace("\r\n","") + " 3 3 3 3 1 2 3 4\r"
       	                	print " Inserindo registro na placa: ",reg
                        	tcp.send(reg)
                        	time.sleep(0.5)
                        	print tcp.recv(4096)

        	print "Removendo arquivo :",name
        	os.remove(name)

	print "Comando M=1 R"
	tcp.send(" M=1 R\r")
	time.sleep(0.5)
	lista=tcp.recv(8128)

	for x in lista.split("\x03\x02"):
		for i in x.split("*"):
			### Falta gravar o cracha que esta com acesso OK

			if "RD#" in i:
				l=i.replace("\x03\x20M=1 R OK","")
				l=l.replace("\x02","")
				l=l.replace("\x03","")
				if l[1:6] == "RD#01":
					print "IF ",l
					sql = "insert into log select " + l[11:23] + ",'" + l[25:27] + "','"+ ip +"', now()"
					print sql
					cursor.execute(sql)
					db.commit()
				elif l[19:24] == "RD#01":
					print "ELSEIF ",l[29:41]
					try:
						sql = "insert into log select " + l[29:41] + ",'OK','"+ ip  +"', now()"
                                        	print sql
						cursor.execute(sql)
                                        	db.commit()
					except: 
						print "Erro inserindo registro numerico, continuando..."
				else:
					print "ELSE ",i

	time.sleep(10)

cursor.close()
db.close()
tcp.close()
