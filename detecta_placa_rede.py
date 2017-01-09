#!/usr/bin/python
import cgi, cgitb, socket

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<center>"
print "<h1>Scanner de Placas na rede</h1>"
print "<pre>"

arg = cgi.FieldStorage()
iprange = arg.getvalue("iprange")

ipini = 243
ipfim = 246

print "Range de IP: " + iprange + "." + str(ipini) + " ate " + iprange + "." + str(ipfim) + "<br>"

for c in range(ipini,ipfim):
	target = str(iprange) +  "." +  str(c)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((target, 3001))
	if result == 0:
		print "Placa encontrada: " + target + " <a href='/cgi-bin/inicia-placa.py?target=" + target + "'>Efetuar Carga Inicial</a><br>"
		sock.close()

print "</pre></center></html>"
