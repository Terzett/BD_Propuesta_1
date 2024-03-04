import tkinter as tk
import matplotlib.pyplot as plt
from importlib import reload

from sympy.physics.control.control_plots import matplotlib

plt = reload(plt)
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
from tkinter import messagebox as MessageBox, filedialog
from Camara import reproducir_con_mp, inicia_pdf
from datetime import datetime
from libs import canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2 as cv
import threading


class DesingTop:
    """
    Clase principal de la interfaz.
    """

    def __init__(self):
        """
        Diccionarios para la identificación de la maquina y la ruta de muestra.
        """
        self.lecturaDemaquinaVideos = \
            {1: r"C:\Users\Terzett Technologix\Documents\PropuestaBD\BD_Propuesta_1\Registros de video\Machine1",
             2: r"C:\Users\Alexis Castillo\PycharmProjects\BD_Propuesta_1\Registros de video\Machine2",
             3: r"C:\Users\Alexis Castillo\PycharmProjects\BD_Propuesta_1\Registros de video\Machine3",
             4: r"C:\Users\Alexis Castillo\PycharmProjects\BD_Propuesta_1\Registros de video\Machine4"}
        self.lecturaDeMaquinasFallos = \
            {1: r"C:\Users\Alexis Castillo\PycharmProjects\BD_Propuesta_1\RegistroDeFallos\Machine1",
             2: r"C:\Users\Alexis Castillo\PycharmProjects\BD_Propuesta_1\RegistroDeFallos\Machine2",
             3: r"C:\Users\Alexis Castillo\PycharmProjects\BD_Propuesta_1\RegistroDeFallos\Machine3",
             4: r"C:\Users\Alexis Castillo\PycharmProjects\BD_Propuesta_1\RegistroDeFallos\Machine4"}

        self.INTERVALO_REFRESCO_RELOJ = 300
        self.INTERVALO_REFRESCO_FECHA = 360000
        self.venta_raiz = tk.Tk()
        self.w = self.venta_raiz.winfo_screenheight()
        self.h = self.venta_raiz.winfo_screenheight()
        self.venta_raiz.state("zoomed")
        self.venta_raiz.title("Video Recording System")
        self.venta_raiz.iconbitmap("BD\icons8-red-50.ico")

        """
        Inicio de menu flotante de la interfaz.
        """
        self.MenuPrincipal = tk.Menu(self.venta_raiz)
        self.SubMenu = tk.Menu(self.MenuPrincipal, tearoff=False, activebackground="#004593")
        self.MenuPrincipal.add_cascade(menu=self.SubMenu, label="Configuración", font="sans-serif")
        self.SubMenu.add_command(label="Salir", command=lambda: [self.mensaje_advertencia()])
        self.SubMenu.add_command(label="Network", command=lambda: [self.ipNetwork()])
        self.SubMenu.add_command(label="Parametros", command=lambda: [self.parametros()])
        self.venta_raiz.config(menu=self.MenuPrincipal)

        """
        Generar reporte 
        """
        self.SubMenu2 = tk.Menu(self.MenuPrincipal, tearoff=False, activebackground="#004593")
        self.MenuPrincipal.add_cascade(menu=self.SubMenu2, label="Generar reporte", font="sans-serif")
        self.SubMenu2.add_command(label="Maquina 1")
        self.SubMenu2.add_command(label="Maquina 2")
        self.SubMenu2.add_command(label="Maquina 3")
        self.SubMenu2.add_command(label="Maquina 4")
        self.SubMenu2.add_command(label="Generar todo los reportes")
        """
        Fin de menu flotante de la interfaz
        """

        """
        Marco superior
        """
        self.MarcoSuperior = tk.Frame(self.venta_raiz, background="#FFFFFF",
                                      highlightthickness=1,
                                      highlightbackground="#000000")
        self.MarcoSuperior.place(relheight=0.1, relwidth=.6, relx=.2)
        TextoInicial = tk.Label(self.MarcoSuperior, text="ORION_TECH",
                                background="#FFFFFF", foreground="#000000",
                                font="sans-serif 18 bold")
        TextoInicial.place(anchor="center", relx=0.5, rely=0.2)
        TextoInicial2 = tk.Label(self.MarcoSuperior, text="VERSION 1.0 DEMO",
                                 background="#FFFFFF", foreground="#000000",
                                 font="sans-serif 10 bold")
        TextoInicial2.place(anchor="center", relx=0.5, rely=0.5)
        TextoInicial3 = tk.Label(self.MarcoSuperior, text="Developed by Terzett Technologix",
                                 background="#FFFFFF", foreground="#000000",
                                 font="sans-serif 10 bold")
        TextoInicial3.place(anchor="center", relx=0.5, rely=0.8)

        """
        Marco seperior gif
        """
        self.MarcoSuperiorGif = tk.Frame(self.venta_raiz, background="#FFFFFF",
                                         highlightthickness=1, highlightbackground="#000000")
        self.MarcoSuperiorGif.place(relheight=0.1, relwidth=0.2, relx=0.8)
        # Animacion de arbol
        gifImage = r"BD/IA1.gif"
        openImage = Image.open(gifImage)

        frames = openImage.n_frames
        imageObject = [PhotoImage(file=gifImage, format=f"gif -index {i}") for i in range(frames)]
        count = 0
        showAnimation = None

        def animation(count):
            global showAnimation
            newImage = imageObject[count]
            gif_Label.configure(image=newImage)
            count += 1
            if count == frames:
                count = 0
            showAnimation = self.MarcoSuperiorGif.after(70, lambda: animation(count))

        gif_Label = Label(self.MarcoSuperiorGif, image="", background="#FFFFFF")
        gif_Label.place(anchor="n", relx=0.2, rely=0.05)

        animation(count)
        # Fin de animacion

        """
        HORA
        """
        self.VariableHoraActual = tk.StringVar(self.MarcoSuperiorGif, value=self.obtenerHoraYFecha())
        HoraPrincipal = tk.Label(self.MarcoSuperiorGif, textvariable=self.VariableHoraActual, background="#FFFFFF",
                                 foreground="#000000", font=f"sans-serif 10 bold")
        HoraPrincipal.place(anchor="center", relx=0.7, rely=0.3)
        TextoHoraPrincipal = tk.Label(self.MarcoSuperiorGif, text="Hora:", background="#FFFFFF", foreground="#000000",
                                      font="sans-serif 10 bold")
        TextoHoraPrincipal.place(anchor="center", relx=0.49, rely=0.3)

        """
        Fecha
        """
        self.VariableFechaActual = tk.StringVar(self.MarcoSuperiorGif, value=self.fecha())
        FechaPrincipal = tk.Label(self.MarcoSuperiorGif, textvariable=self.VariableFechaActual, background="#FFFFFF",
                                  foreground="#000000", font=f"sans-serif 10 bold")
        FechaPrincipal.place(anchor="center", relx=0.72, rely=0.7)
        TextoHoraPrincipal = tk.Label(self.MarcoSuperiorGif, text="Fecha:", background="#FFFFFF", foreground="#000000",
                                      font="sans-serif 10 bold")
        TextoHoraPrincipal.place(anchor="center", relx=0.5, rely=0.7)

        """
        Marco superior logo Terzett
        """
        self.MarcoSuperiorLogo = tk.Frame(self.venta_raiz, background="#FFFFFF", highlightthickness=1,
                                          highlightbackground="#000000")
        self.MarcoSuperiorLogo.place(relheight=0.1, relwidth=0.2, relx=0)

        img0 = tk.PhotoImage(file=r"BD/BD1.png")
        imglogo0 = tk.Label(self.MarcoSuperiorLogo, image=img0, background="#FFFFFF")
        imglogo0.image = img0
        imglogo0.place(anchor="n", relx=0.28, rely=0.2)
        TextoBd = tk.Label(self.MarcoSuperiorLogo, text="Becton Dickinson",
                           background="#FFFFFF", foreground="#000000",
                           font="sans-serif 8 bold")
        TextoBd.place(anchor="center", relx=0.28, rely=0.8)

        img1 = tk.PhotoImage(file=r"BD/TerzettB.png")
        imglogo1 = tk.Label(self.MarcoSuperiorLogo, image=img1, background="#FFFFFF")
        imglogo1.image = img1
        imglogo1.place(anchor="n", relx=0.7, rely=0.1)

        """
        Marco central maquina 1
        """

        self.MarcoCentralMach1 = tk.Frame(self.venta_raiz, background="#FFFFFF", highlightthickness=1,
                                          highlightbackground="#000000")
        self.MarcoCentralMach1.place(relheight=0.45, relwidth=0.5, rely=0.1)

        self.MarcoContFallos1 = tk.Frame(self.MarcoCentralMach1, background="#FFFFFF", highlightthickness=1, highlightbackground="#000000")
        self.MarcoContFallos1.place(relheight=0.1, relwidth=0.2, relx=0.7, rely=0.05)
        self.VariableErrores = tk.StringVar(self.MarcoContFallos1, value=self.fecha())
        self.FechaPrincipal = tk.Label(self.MarcoContFallos1, textvariable=self.VariableErrores, background="#FFFFFF",
                                  foreground="#000000", font=f"sans-serif 10 bold")
        self.FechaPrincipal.place(anchor="center", relx=0.72, rely=0.7)

        # Animacion de REC
        gifImage1 = r"BD/rec.gif"
        openImage1 = Image.open(gifImage1)

        frames = openImage1.n_frames
        imageObject1 = [PhotoImage(file=gifImage1, format=f"gif -index {i}") for i in range(frames)]
        count = 0
        showAnimation = None

        def animationrec1(count):
            global showAnimation
            newImage1 = imageObject1[count]
            gif_Label1.configure(image=newImage1)
            count += 1
            if count == frames:
                count = 0
            showAnimation = self.MarcoCentralMach1.after(70, lambda: animationrec1(count))

        gif_Label1 = Label(self.MarcoCentralMach1, image="", background="#FFFFFF")
        gif_Label1.place(anchor="n", relx=0.45, rely=0.2)

        animationrec1(count)
        # Fin de animacion

        """
        Grafica de fallos
        """
        self.MarcoGrafica1 = tk.Frame(self.MarcoCentralMach1, background="#FFFFFF", highlightthickness=1,
                                      highlightbackground="#000000")
        self.MarcoGrafica1.pack(expand=True, fill=tk.BOTH)
        self.MarcoGrafica1.place(relheight=0.6, relwidth=0.4, relx=0.55, rely=0.2)

        # Inicio de grafica
        self.fig = plt.figure(figsize=(5, 2.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.MarcoGrafica1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        self.draw_graph_mach1()
        # fin de grafica

        img2 = tk.PhotoImage(file=r"BD/Form1.png")
        imgMach1 = tk.Label(self.MarcoCentralMach1, image=img2, background="#FFFFFF")
        imgMach1.image = img2
        imgMach1.place(anchor="n", relx=0.2, rely=0.3)
        TextoForm1a = tk.Label(self.MarcoCentralMach1, text="Formadora 1",
                               background="#FFFFFF", foreground="#000000",
                               font="sans-serif 12 bold")
        TextoForm1a.place(anchor="center", relx=0.1, rely=0.2)
        TextoForm1b = tk.Label(self.MarcoCentralMach1, text="Número de fallos:",
                               background="#FFFFFF",
                               foreground="#000000", font="sans-serif")
        TextoForm1b.place(anchor="center", relx=0.6, rely=0.1)
        self.btnMach1Videos = tk.Button(self.MarcoCentralMach1, text="Registros de video",
                                        command=lambda: [reproducir_con_mp(self.RegistroVideosMach1(1))],
                                        width=30, background="#004593",
                                        activebackground="green", foreground="#FFFFFF", border=0, font="sans-serif")
        self.btnMach1Videos.place(anchor="center", relx=0.6, rely=0.9)
        self.btnMach1Registros = tk.Button(self.MarcoCentralMach1,
                                           command=lambda: [inicia_pdf(self.RegistroFalloMach1(1))],
                                           text="Registros de fallo", width=30,
                                           background="#004593", activebackground="green",
                                           foreground="#FFFFFF",
                                           border=0, font="sans-serif")
        self.btnMach1Registros.place(anchor="center", relx=0.3, rely=0.9)

        """
        Marco central maquina 2
        """
        self.MarcoCentralMach2 = tk.Frame(self.venta_raiz, background="#FFFFFF",
                                          highlightthickness=1,
                                          highlightbackground="#000000")
        self.MarcoCentralMach2.place(relheight=0.45, relwidth=0.5, rely=0.55)
        self.MarcoContFallos2 = tk.Frame(self.MarcoCentralMach2, background="#FFFFFF",
                                         highlightthickness=1,
                                         highlightbackground="#000000")
        self.MarcoContFallos2.place(relheight=0.1, relwidth=0.2, relx=0.7, rely=0.05)

        # Animacion de REC
        gifImage2 = r"BD/rec.gif"
        openImage2 = Image.open(gifImage2)

        frames = openImage2.n_frames
        imageObject2 = [PhotoImage(file=gifImage2, format=f"gif -index {i}") for i in range(frames)]
        count = 0
        showAnimation = None

        def animationrec2(count):
            global showAnimation
            newImage2 = imageObject2[count]
            gif_Label2.configure(image=newImage2)
            count += 1
            if count == frames:
                count = 0
            showAnimation = self.MarcoCentralMach2.after(70, lambda: animationrec2(count))

        gif_Label2 = Label(self.MarcoCentralMach2, image="", background="#FFFFFF")
        gif_Label2.place(anchor="n", relx=0.45, rely=0.2)

        animationrec2(count)
        # Fin de animacion

        """
        Grafica de fallos
        """
        self.MarcoGrafica2 = tk.Frame(self.MarcoCentralMach2, background="#FFFFFF",
                                      highlightthickness=1,
                                      highlightbackground="#000000")
        self.MarcoGrafica2.place(relheight=0.6, relwidth=0.4, relx=0.55, rely=0.2)

        # Inicio de grafica
        self.fig = plt.figure(figsize=(5, 2.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.MarcoGrafica2)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        self.draw_graph_mach2()
        # Fin de frafica

        imgMach2 = tk.Label(self.MarcoCentralMach2, image=img2, background="#FFFFFF")
        imgMach2.image = img2
        imgMach2.place(anchor="n", relx=0.2, rely=0.3)
        TextoForm2a = tk.Label(self.MarcoCentralMach2, text="Formadora 2",
                               background="#FFFFFF",
                               foreground="#000000",
                               font="sans-serif 12 bold")
        TextoForm2a.place(anchor="center", relx=0.1, rely=0.2)
        TextoForm2b = tk.Label(self.MarcoCentralMach2,
                               text="Número de fallos:",
                               background="#FFFFFF",
                               foreground="#000000", font="sans-serif")
        TextoForm2b.place(anchor="center", relx=0.6, rely=0.1)
        self.btnMach2Videos = tk.Button(self.MarcoCentralMach2,
                                        text="Registros de video",
                                        command=lambda: [reproducir_con_mp(self.RegistroVideosMach1(2))],
                                        width=30,
                                        background="#004593", activebackground="green",
                                        foreground="#FFFFFF", border=0,
                                        font="sans-serif")
        self.btnMach2Videos.place(anchor="center", relx=0.6, rely=0.9)
        self.btnMach2Registros = tk.Button(self.MarcoCentralMach2, text="Registros de fallo",
                                           command=lambda: [inicia_pdf(self.RegistroFalloMach1(2))],
                                           width=30,
                                           background="#004593", activebackground="green", foreground="#FFFFFF",
                                           border=0, font="sans-serif")
        self.btnMach2Registros.place(anchor="center", relx=0.3, rely=0.9)

        """
        Marco central maquina 3
        """
        self.MarcoCentralMach3 = tk.Frame(self.venta_raiz, background="#FFFFFF", highlightthickness=1,
                                          highlightbackground="#000000")
        self.MarcoCentralMach3.place(relheight=0.45, relwidth=0.5, relx=0.5, rely=0.1)
        self.MarcoContFallos3 = tk.Frame(self.MarcoCentralMach3, background="#FFFFFF", highlightthickness=1,
                                         highlightbackground="#000000")
        self.MarcoContFallos3.place(relheight=0.1, relwidth=0.2, relx=0.7, rely=0.05)

        # Animacion de REC
        gifImage3 = r"BD/rec.gif"
        openImage3 = Image.open(gifImage3)

        frames = openImage3.n_frames
        imageObject3 = [PhotoImage(file=gifImage3, format=f"gif -index {i}") for i in range(frames)]
        count = 0
        showAnimation = None

        def animationrec3(count):
            global showAnimation
            newImage3 = imageObject3[count]
            gif_Label3.configure(image=newImage3)
            count += 1
            if count == frames:
                count = 0
            showAnimation = self.MarcoCentralMach3.after(70, lambda: animationrec3(count))

        gif_Label3 = Label(self.MarcoCentralMach3, image="", background="#FFFFFF")
        gif_Label3.place(anchor="n", relx=0.45, rely=0.2)

        animationrec3(count)
        # Fin de animacion

        """
        Grafica de fallos
        """
        self.MarcoGrafica3 = tk.Frame(self.MarcoCentralMach3, background="#FFFFFF",
                                      highlightthickness=1,
                                      highlightbackground="#000000")
        self.MarcoGrafica3.place(relheight=0.6, relwidth=0.4, relx=0.55, rely=0.2)

        # Inicio de grafica
        self.fig = plt.figure(figsize=(5, 2.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.MarcoGrafica3)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        self.draw_graph_mach3()
        # Fin de frafica

        imgMach3 = tk.Label(self.MarcoCentralMach3, image=img2, background="#FFFFFF")
        imgMach3.image = img2
        imgMach3.place(anchor="n", relx=0.2, rely=0.3)
        TextoForm3a = tk.Label(self.MarcoCentralMach3, text="Formadora 3", background="#FFFFFF", foreground="#000000",
                               font="sans-serif 12 bold")
        TextoForm3a.place(anchor="center", relx=0.1, rely=0.2)
        TextoForm3b = tk.Label(self.MarcoCentralMach3, text="Número de fallos:", background="#FFFFFF",
                               foreground="#000000", font="sans-serif")
        TextoForm3b.place(anchor="center", relx=0.6, rely=0.1)
        self.btnMach3Videos = tk.Button(self.MarcoCentralMach3, text="Registros de video",
                                        command=lambda: [reproducir_con_mp(self.RegistroVideosMach1(3))], width=30,
                                        background="#004593", activebackground="green", foreground="#FFFFFF", border=0,
                                        font="sans-serif")
        self.btnMach3Videos.place(anchor="center", relx=0.6, rely=0.9)
        self.btnMach3Registros = tk.Button(self.MarcoCentralMach3, text="Registros de fallo",
                                           command=lambda: [inicia_pdf(self.RegistroFalloMach1(3))],
                                           width=30,
                                           background="#004593", activebackground="green", foreground="#FFFFFF",
                                           border=0, font="sans-serif")
        self.btnMach3Registros.place(anchor="center", relx=0.3, rely=0.9)

        """
        Marco central maquina 4
        """
        self.MarcoCentralMach4 = tk.Frame(self.venta_raiz, background="#FFFFFF", highlightthickness=1,
                                          highlightbackground="#000000")
        self.MarcoCentralMach4.place(relheight=0.45, relwidth=0.5, relx=0.5, rely=0.55)
        self.MarcoContFallos4 = tk.Frame(self.MarcoCentralMach4, background="#FFFFFF", highlightthickness=1,
                                         highlightbackground="#000000")
        self.MarcoContFallos4.place(relheight=0.1, relwidth=0.2, relx=0.7, rely=0.05)
        # # Animacion de REC
        gifImage4 = r"BD/rec.gif"
        openImage4 = Image.open(gifImage4)

        frames = openImage4.n_frames
        imageObject4 = [PhotoImage(file=gifImage4, format=f"gif -index {i}") for i in range(frames)]
        count = 0
        showAnimation = None

        def animationrec4(count):
            global showAnimation
            newImage4 = imageObject4[count]
            gif_Label4.configure(image=newImage4)
            count += 1
            if count == frames:
                count = 0
            showAnimation = self.MarcoCentralMach4.after(70, lambda: animationrec4(count))

        gif_Label4 = Label(self.MarcoCentralMach4, image="", background="#FFFFFF")
        gif_Label4.place(anchor="n", relx=0.45, rely=0.2)

        animationrec4(count)
        # Fin de animacion

        """
        Grafica de fallos
        """
        self.MarcoGrafica4 = tk.Frame(self.MarcoCentralMach4, background="#FFFFFF", highlightthickness=1,
                                      highlightbackground="#000000")
        self.MarcoGrafica4.place(relheight=0.6, relwidth=0.4, relx=0.55, rely=0.2)

        # Inicio de grafica
        self.fig = plt.figure(figsize=(5, 2.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.MarcoGrafica4)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        self.draw_graph_mach4()
        # Fin de frafica

        imgMach4 = tk.Label(self.MarcoCentralMach4, image=img2, background="#FFFFFF")
        imgMach4.image = img2
        imgMach4.place(anchor="n", relx=0.2, rely=0.3)
        TextoForm4a = tk.Label(self.MarcoCentralMach4, text="Formadora 4", background="#FFFFFF", foreground="#000000",
                               font="sans-serif 12 bold")
        TextoForm4a.place(anchor="center", relx=0.1, rely=0.2)
        TextoForm4b = tk.Label(self.MarcoCentralMach4, text="Número de fallos:", background="#FFFFFF",
                               foreground="#000000", font="sans-serif")
        TextoForm4b.place(anchor="center", relx=0.6, rely=0.1)
        self.btnMach4Videos = tk.Button(self.MarcoCentralMach4, text="Registros de video",
                                        command=lambda: [reproducir_con_mp(self.RegistroVideosMach1(4))], width=30,
                                        background="#004593", activebackground="green", foreground="#FFFFFF", border=0,
                                        font="sans-serif")
        self.btnMach4Videos.place(anchor="center", relx=0.6, rely=0.9)
        self.btnMach4Registros = tk.Button(self.MarcoCentralMach4, text="Registros de fallo",
                                           command=lambda: [inicia_pdf(self.RegistroFalloMach1(4))], width=30,
                                           background="#004593", activebackground="green", foreground="#FFFFFF",
                                           border=0, font="sans-serif")
        self.btnMach4Registros.place(anchor="center", relx=0.3, rely=0.9)

        """
        Bucle de ventana principal
        """
        self.refrescarReloj()
        self.refrescarFecha()
        self.mostrar_errores_machine1()
        self.venta_raiz.mainloop()

    def mensaje_advertencia(self):
        """
            Ventana de advertencia para el usaurio
        """
        resultado = MessageBox.askquestion("Salir", "¿Genero el reporte de resultados antes de salir?")
        if resultado == "yes":
            self.venta_raiz.destroy()

    def obtenerHoraYFecha(self):
        pass

    def refrescarReloj(self):
        pass

    def refrescarFecha(self):
        pass

    def fecha(self):
        pass

    def mostrar_errores_machine1(self):
        pass

    def draw_graph_mach1(self):
        # detos de ejemplo para la grafica
        x = [1, 2, 3, 2]
        y = [2, 3, 5, 2]

        # Limpieza de cualquier grafico anterior
        plt.clf()

        # Dibuja la grafica
        plt.plot(x, y)
        plt.title("Duracion del fallo")
        plt.legend("T")
        plt.xlabel('Error', loc="center")
        plt.ylabel('Tiempo de duración', loc="center")

        self.canvas.draw()

    def draw_graph_mach2(self):
        # detos de ejemplo para la grafica
        x = [1, 2, 3, 3, 3, 4, 4]
        y = [2, 3, 5, 2, 1, 1, 2]

        # Limpieza de cualquier grafico anterior
        plt.clf()

        # Dibuja la grafica
        plt.plot(x, y)
        plt.title("Duracion del fallo")
        plt.legend("T")
        plt.xlabel('Error', loc="center")
        plt.ylabel('Tiempo de duración', loc="center")
        self.canvas.draw()

    def draw_graph_mach3(self):
        # detos de ejemplo para la grafica
        x = [1, 2, 3, 2, 0, 1]
        y = [2, 3, 5, 2, 1, 1]

        # Limpieza de cualquier grafico anterior
        plt.clf()

        # Dibuja la grafica
        plt.plot(x, y)
        plt.title("Duracion del fallo")
        plt.legend("T")
        plt.xlabel('Error', loc="center")
        plt.ylabel('Tiempo de duración', loc="center")

        self.canvas.draw()

    def draw_graph_mach4(self):
        # detos de ejemplo para la grafica
        x = [1, 2, 3, 2, 7, 8]
        y = [2, 3, 5, 2, 9, 9]

        # Limpieza de cualquier grafico anterior
        plt.clf()

        # Dibuja la grafica
        plt.plot(x, y)
        plt.title('Duracion del fallo')
        plt.legend("T")
        plt.xlabel('Error', loc="center")
        plt.ylabel('Tiempo de duración', loc="center")

        self.canvas.draw()

    def RegistroVideosMach1(self, identificadorMach):
        # print(self.lecturaDemaquinaVideos[identificadorMach])

        self.archivo1 = filedialog.askopenfilename(title="Machine 1 Video Logs",
                                                   initialdir=self.lecturaDemaquinaVideos[identificadorMach],
                                                   filetypes=(("Archivo de video", "*.avi"), ("Archivos pdf", "*.pdf"),
                                                              ("Todos los archivos", "*.*")))
        return (self.archivo1)

    def RegistroFalloMach1(self, identificadorMachFallo):
        self.pdf1 = filedialog.askopenfilename(title="Machine 1 Register Logs",
                                               initialdir=self.lecturaDeMaquinasFallos[identificadorMachFallo],
                                               filetypes=(("Archivos pdf", "*.pdf"), ("Todos los archivos", "*.*")))
        return (self.pdf1)

    def ipNetwork(self):
        """
            Ventana emergente para revisar la ip asignada a la camara
        :return:
        """
        self.ventana_ip = tk.Toplevel()
        self.ventana_ip.geometry("400x300")
        self.ventana_ip.resizable(0, 0)
        self.ventana_ip.title("IP NETWORK")
        self.ventana_ip.iconbitmap("BD\Cam.ico")
        marcoiP = tk.Frame(self.ventana_ip, border=0, background="#F5F5F5", highlightthickness=1,
                           highlightbackground="#000000")
        marcoiP.place(relheight=0.5, relwidth=0.8, relx=0.1, rely=0.3)
        etiqueta = tk.Label(self.ventana_ip, text="Direccion IP asignadas a los dispositivos de vision:")
        etiqueta1 = tk.Label(self.ventana_ip, text="3", background="#F5F5F5")
        etiqueta11 = tk.Label(self.ventana_ip, text="CAM 1:", background="#F5F5F5")
        etiqueta.place(anchor="center", relx=0.5, rely=0.12)
        etiqueta1.place(anchor="center", relx=0.5, rely=0.45)
        etiqueta11.place(anchor="center", relx=0.3, rely=0.45)

    def parametros(self):
        self.ventana_par = tk.Toplevel()
        self.ventana_par.geometry("400x300")
        self.ventana_par.resizable(0, 0)
        self.ventana_par.title("System Parameters")
        self.ventana_par.iconbitmap("BD\Ajustes.ico")
        marcoPar = tk.Frame(self.ventana_par, border=0, background="#F5F5F5", highlightthickness=1,
                            highlightbackground="#000000")
        marcoPar.place(relheight=0.5, relwidth=0.8, relx=0.1, rely=0.3)
        etiqueta2 = tk.Label(self.ventana_par, text="Visualization of applied parameters.")
        etiqueta22 = tk.Label(self.ventana_par, text="****************", background="#F5F5F5")
        etiqueta222 = tk.Label(self.ventana_par, text="***************", background="#F5F5F5")
        etiqueta2.place(anchor="center", relx=0.5, rely=0.12)
        etiqueta22.place(anchor="center", relx=0.5, rely=0.45)
        etiqueta222.place(anchor="center", relx=0.3, rely=0.45)
