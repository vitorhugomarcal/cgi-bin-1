#!/usr/bin/python
import cgi, cgitb, MySQLdb, datetime

print "Content-type:text/html\r\n\r\n"
print "<html>"

arg = cgi.FieldStorage()
id_controladora = arg.getvalue("controladora")
num_leitor = arg.getvalue("leitor")
id_dvr = arg.getvalue("dvr")
num_canal = arg.getvalue("camera")

print "ID Controladora: " + str(id_controladora) + "<br>"
print "Leitor: " + str(num_leitor) + "<br>"
print "ID DVR: " + str(id_dvr) + "<br>"
print "Camera: " + str(num_canal) + "<br>"


db = MySQLdb.connect("127.0.0.1","root","161879","wfp")
cursor = db.cursor()
sql="insert into link_camera_leitor (id_controladora, num_leitor, id_dvr, num_canal, datref) values ("+id_controladora+","+num_leitor+","+id_dvr+","+num_canal+",now())"
print sql
cursor.execute(sql)
db.commit()
cursor.close()
db.close()

print "<br><a href='/cadastro_link_camera_leitor.php'>Voltar</a>"
print "</html>"
