import cv2
from pylogix import PLC
import threading
import time

class PLC_AB():
    def __init__(self, ip):
        self.ip = ip

    def conexion(self):
        with PLC() as com:
            com.IPAddress = self.ip
        while True:
            alarma = com.Read("Alarm.0")
            print(alarma.Value)
            if alarma.Value == True:
                salida.iniciae_Video()
            else:
                salida.detener_video()
                print("Termino de grabar")


class Camara:
    def __init__(self, lecturacam, iprstp =""):
        self.lecturacam = lecturacam
        self.iprstp = iprstp
        self.cap = cv2.VideoCapture(self.lecturacam)

    def __str__(self):
        return "Camara maquina 1"

    def stream_video(self):
       while (self.cap.isOpened()):
           ret, frame = self.cap.read()
           cv2.imshow('Camara 1', frame)
           if (cv2.waitKey(1) == ord('s')):
               break
       self.cap.release()
       cv2.destroyAllWindows()

class Video():
    def __init__(self, camara, filename, fourcc, fps, framesize):
        self.camara = camara
        self.filename =filename
        self.fourcc = fourcc
        self.fps = fps
        self.framesize = framesize
        self.output = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*self.fourcc), self.fps, self.framesize)
        self.detener = False

    def grabar_video(self):
        while not self.detener:
            ret, frame = self.camara.cap.read()
            cv2.imshow('Frame', frame)
            self.output.write(frame)
            if(cv2.waitKey(1) == ord('s')):
                break
    def iniciae_Video(self):
        self.detener = False
    def detener_video(self):
        self.detener = True

#***********************************************************************************************
cam = Camara(1)
ipPlc = PLC_AB('192.168.1.100')
salida = Video(cam, 'Maquina 1.avi','XVID', 30, (640,480))
#***********************************************************************************************

hilo = threading.Thread(target = salida.grabar_video)
hilo.start()

ipPlc.conexion()