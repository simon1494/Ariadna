import os
from tkinter import messagebox
from tkinter import filedialog
import calendar
import re


class Mensajeador:
    DIRECTORIO_PADRE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

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

    @classmethod
    def obtener_directorio_github(cls, subcarpeta=None):
        # Obtenemos el directorio actual del script
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        # Vamos subiendo de nivel según el número especificado
        for _ in range(3):
            directorio_actual = os.path.dirname(directorio_actual)

        if subcarpeta:
            return os.path.join(directorio_actual, subcarpeta)

        return directorio_actual

    @classmethod
    def es_formato_mm_dd(cls, cadena):
        # Expresión regular para detectar formato "mm-dd" con valores válidos
        patron = r"^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        return bool(re.match(patron, cadena))

    @classmethod
    def distribuir_archivos(cls, carpeta_destino, archivo):
        print(archivo)
        match carpeta_destino.lower():
            case "cr":
                ruta_base = cls.DIRECTORIO_PADRE + "/Exportaciones/Crudos/NORMAL/"
            case "ns":
                ruta_base = (
                    cls.DIRECTORIO_PADRE + "/Exportaciones/No segmentados/NORMAL/"
                )
            case "seg":
                ruta_base = cls.DIRECTORIO_PADRE + "/Exportaciones/Segmentados/NORMAL/"

        # Detectar mes del archivo (primeros 2 caracteres son el mes)
        if not cls.es_formato_mm_dd(archivo):
            mes_numero = int(archivo[5:7])
        else:
            mes_numero = int(archivo[0:2])

        # Convertir el número del mes al nombre completo en español
        nombre_mes = f"{mes_numero} {calendar.month_name[mes_numero].capitalize()}"
        # Crear el path completo de la carpeta del mes
        carpeta_mes = os.path.join(ruta_base, nombre_mes)

        # Si la carpeta no existe, crearla
        if not os.path.exists(carpeta_mes):
            os.makedirs(carpeta_mes)

        # Retornar el path de la carpeta del mes
        return carpeta_mes
