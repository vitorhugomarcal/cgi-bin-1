#!/usr/bin/python
import cgi, cgitb, socket

print "Content-type:text/html\r\n\r\n"
print "<html><head>"
print "<link rel='stylesheet' href='../css/bootstrap.min.css'>"


print "<script>function showFoto(strIP) {if (strIP == '') {document.getElementById('txtlog').innerHTML ='';return;} else {if (window.XMLHttpRequest) {xmlhttp = new XMLHttpRequest();} else {xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');}xmlhttp.onreadystatechange = function() {if (this.readyState == 4 && this.status == 200) {document.getElementById('txtlog').innerHTML = this.responseText;}};xmlhttp.open('GET','inicia-placa.py?target='+strIP, true);xmlhttp.send();}}</script>"





print "</head>"
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
		#print "Placa encontrada: " + target + " <a href='/cgi-bin/inicia-placa.py?target=" + target + "'>Efetuar Carga Inicial</a><br>"
		print "Placa encontrada: " + target + " <a href='#' onclick=showFoto('"+target+"')>Efetuar Carga Inicial</a><br>"
		sock.close()

print "</pre></center>"
print "<object type='text/html' data='../web.html' style='width: 100%; height: 100%; border: 0px'></iframe>"
print "<div id='txtlog'></div>"

print "</html>"



