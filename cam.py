#!/usr/bin/python
import cv

video = cv.CaptureFromFile("rtsp://admin:@192.168.0.19/user=admin&password=&channel=1&stream=0.sdp?")
cv.NamedWindow("IP Camera", cv.CV_WINDOW_AUTOSIZE)
#contador = 1
while True:
  #  img = cv.QueryFrame(video)
  #  cv.SaveImage("/var/www/html/teste.jpg",img)
    cv.GrabFrame(video)
    frame = cv.RetrieveFrame(video)
    cv.ShowImage("IP Camera", frame)
    cv.WaitKey(150)
 #   print contador
 #   contador = contador + 1
