import numpy as np
import cv2 as cv
import threading
import subprocess

def reproducir_con_mp(ruta_video):
    mp_path = r'C:\Program Files (x86)\Windows Media Player\wmplayer.exe'  # Cambia esta ruta según la ubicación de tu instalación de MP
    comando = [mp_path, ruta_video]
    subprocess.Popen(comando)

def inicia_pdf(ruta_pdf):
    comando1 = ['start', '', ruta_pdf]
    subprocess.Popen(comando1, shell=True)




# def videocap():
#     media = vlc.MediaPlayer("video.mp4")
#     media.play()
    # cap = cv.VideoCapture(read)
    # if not cap.isOpened():
    #     print("Cannot open camera")
    #     exit()
    # while True:
    #     # Capture frame-by-frame
    #     ret, frame = cap.read()
    #     # if frame is read correctly ret is True
    #     if not ret:|
    #         print("Can't receive frame (stream end?). Exiting ...")
    #         break
    #     # Our operations on the frame come here
    #     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #     # Display the resulting frame
    #     cv.imshow('frame', gray)
    #     if cv.waitKey(1) == ord('q'):
    #         break
    # # When everything done, release the capture
    # cap.release()
    # cv.destroyAllWindows()

# def videoStream(lectura):
#
#     cap = cv.VideoCapture(lectura)
#     if not cap.isOpened():
#         print("Cannot open camera")
#         exit()
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         # if frame is read correctly ret is True
#         if not ret:
#             print("Can't receive frame (stream end?). Exiting ...")
#             break
#         # Our operations on the frame come here
#         gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#         # Display the resulting frame
#         cv.imshow('frame', gray)
#         if cv.waitKey(1) == ord('q'):
#             break
#     # When everything done, release the capture
#     cap.release()
#     cv.destroyAllWindows()
# #
# #
# hilostream = threading.Thread(target=videoStream, args=(0,))
# # # hilovideo = threading.Thread(target=videocap, args=("Registros de video/Machine1/video.mp4",))
# hilostream.start()
# # # hilovideo.start()
# hilostream.join()
# # # hilovideo.join()