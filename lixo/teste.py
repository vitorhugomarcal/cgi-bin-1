#!/usr/bin/python
import socket, time

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = ("192.168.0.19",554)
tcp.connect(dest)

#while True:
print "OPTIONS rtsp://video.foocorp.com:554 RTSP/1.0"
tcp.send("DESCRIBE rtsp://192.168.0.19:554/stream=0.sdp RTSP/1.0\r\n")
time.sleep(1)
print tcp.recv(8128)
