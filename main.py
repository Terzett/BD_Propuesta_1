from interfaz import DesingTop
from logicaInterfaz import Master
import time

import cv2
import threading
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from pylogix import PLC

banderas = set()
cantidad_paros = [0]
fallos = [0]


def plc_lectura():
    global cantidad_paros
    with PLC() as com:
        # Comunicacion con PLC//AB
        com.IPAddress = "192.168.1.100"  # IP del PLC, puede variar
    while True:
        #print("1")
        # time.sleep(3)
        # start_rec()
        # print("4")
        # time.sleep(5)
        # stop_rec()
        emergency_sign = com.Read("Alarm.0", count=1)
        if emergency_sign.Value == True and 1 not in banderas:
            print("entro")
            banderas.add(1)
            start_rec()
            cantidad_paros[0] = cantidad_paros[0] + 1
            fallos[0] = fallos[0] + 1
            # time.sleep(10)
        if emergency_sign.Value == False and 2 not in banderas and 1 in banderas:
            print("salio")
            banderas.add(2)
            stop_rec()
            banderas.remove(2)
            banderas.remove(1)
            print(cantidad_paros[0])


def stop_rec():
    global running
    running = False

    # start_button.config(state="normal")
    # stop_button.config(state="disabled")


def start_capture():
    global capture, last_frame
    now = str(datetime.now())
    nombre = now.split(" ")[1].split(".")[1]
    nombre = f"Registros de video/Machine1/Machine1-{nombre}.avi"
    capture = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc("X", "V", "I", "D")
    video_writer = cv2.VideoWriter(nombre, fourcc, 30.0, (640, 480))

    while running:
        rect, frame = capture.read()

        if rect:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            last_frame = Image.fromarray(cv2image)
            video_writer.write(frame)

    capture.release()
    video_writer.release()


# def update_frame():
#     if last_frame is not None:
#         tk_img = ImageTk.PhotoImage(master=video_label, image=last_frame)
#         video_label.config(image=tk_img)
#         video_label.tk_img = tk_img
#
#     if running:
#         root.after(10, update_frame)


def start_rec():
    global running

    running = True
    thread = threading.Thread(target=start_capture, daemon=True)
    thread.start()
    #update_frame()

    # start_button.config(state="disabled")
    # stop_button.config(state="normal")


# def closeWindow():
#     stop_rec()
#     root.destroy()


running = False
after_id = None
last_frame = None

# root = tk.Tk()
# root.protocol("WM_DELETE_WINDOW", closeWindow)
#
# video_label = tk.Label()
# video_label.pack(expand=True, fill="both")

thread1 = threading.Thread(target=plc_lectura, daemon=True)
thread1.start()

Master(fallos)
