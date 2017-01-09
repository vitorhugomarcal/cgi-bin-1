#Packet sniffer in python for Linux
#Sniffs only incoming TCP packet
 
import socket, sys,time
from struct import *
 
global datafull, atualAck
#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
# receive a packet
while True:
    packet = s.recvfrom(65565)
#    packet = s.recvfrom(4096)
     
    #packet string from tuple
    packet = packet[0]
     
    #take first 20 characters for the ip header
    ip_header = packet[0:20]
     
    #now unpack them :)
    iph = unpack('!BBHHHBBH4s4s' , ip_header)
     
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
     
    iph_length = ihl * 4
     
    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8]);
    d_addr = socket.inet_ntoa(iph[9]);
     
    #print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
     
    tcp_header = packet[iph_length:iph_length+20]
     
    #now unpack them :)
    tcph = unpack('!HHLLBBHHH' , tcp_header)
     
    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4
     
    #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
     
    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size
     
    #get data from the packet
    data = packet[h_size:]
    time.sleep(0.5) 
    

    if (str(s_addr) == "192.168.1.244") and (len(data) > 0):

        try:
            #print "estou no try"
            atualAck
        except NameError:
            #print "Entrei no expce"
            atualAck = "oi"

            #print atualAck
        if atualAck == "oi":
            #print "Vazio"
            dataFull = data
            atualAck = str(acknowledgement)
            #print dataFull

	elif atualAck <> str(acknowledgement):
            #print "Esou no elif"
            print "___________________________________"
	    print dataFull
            dataFull = data
            atualAck = str(acknowledgement)

            #print dataFull
	
	elif atualAck == str(acknowledgement):


            #print "entrei no else"
            dataFull = dataFull + data
            atualAck = str(acknowledgement)










        



#        print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
#        print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
#        print data
        #print "ACK: " + str(acknowledgement) + " - " + data
#        print 
