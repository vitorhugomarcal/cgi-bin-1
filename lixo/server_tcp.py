import socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = ("192.168.1.105",5568)

tcp.bind(orig)
tcp.listen(1)

while True:
	con, cliente = tcp.accept()
	print "conectado: ", cliente
	while True:
		msg = con.recv(1024)
		if not msg: break
		print cliente,msg

	print "Finalizando: ", cliente
	con.close()
