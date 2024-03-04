from interfaz import DesingTop
from datetime import datetime
import tkinter as tk

class Master(DesingTop):
    """
        Clase hija del diseño de Top, aqui esta la parte logica
    """

    def __init__(self,errores):
        self.errores = errores
        super().__init__()


    def obtenerHoraYFecha(self):
        """
            Metodo para obtener la hora actual
        :return:
        """
        return datetime.now().strftime("%H:%M:%S")

    def refrescarReloj(self):
        """
            Metodo para estar actualizando el tiempo mostrado en la interfaz
        :return:
        """
        self.VariableHoraActual.set(self.obtenerHoraYFecha())
        self.MarcoSuperiorGif.after(self.INTERVALO_REFRESCO_RELOJ, self.refrescarReloj)

    def fecha(self):
        """
            Metodo para obtner la fecha actual
        :return:
        """
        return datetime.now().strftime("%d-%m-%Y")

    def refrescarFecha(self):
        """
            Metodo para estar refrescando la fecha actual si es que llegara a cambiar durante el uso de la interfaz
        :return:
        """
        self.VariableFechaActual.set(self.fecha())
        self.MarcoSuperiorGif.after(self.INTERVALO_REFRESCO_RELOJ, self.refrescarFecha)

    def mostrar_errores_machine1(self):
        self.VariableErrores.set(self.errores[0])
        self.MarcoSuperiorGif.after(self.INTERVALO_REFRESCO_RELOJ, self.mostrar_errores_machine1)
