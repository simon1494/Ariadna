import os
from tkinter import messagebox
from tkinter import filedialog


class Mensajes:
    DIRECTORIO_PADRE = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )

    @staticmethod
    def mostrar_mensaje_info(mensaje):
        messagebox.showinfo("Información", mensaje)

    @staticmethod
    def mostrar_mensaje_advertencia(mensaje):
        messagebox.showwarning("Advertencia", mensaje)

    @staticmethod
    def mostrar_mensaje_error(mensaje):
        messagebox.showerror("Error", mensaje)

    @staticmethod
    def mostrar_mensaje_pregunta(mensaje):
        respuesta = messagebox.askyesno("¿Desea...?", mensaje)
        return respuesta

    @classmethod
    def seleccionar_archivo(cls, carpeta_abierta_por_default):
        ruta_del_archivo = filedialog.askopenfilename(
            initialdir=cls.DIRECTORIO_PADRE + carpeta_abierta_por_default
        )
        return ruta_del_archivo

    @classmethod
    def seleccionar_carpeta(cls, carpeta_abierta_por_default):
        ruta_de_la_carpeta = filedialog.askdirectory(
            initialdir=cls.DIRECTORIO_PADRE + carpeta_abierta_por_default
        )
        return ruta_de_la_carpeta
