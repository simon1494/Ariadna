import sys

sys.path.append("../ariadna")
sys.path.append("../ariadna/modelos")

import mysql.connector
import locale
import datetime
import os
import copy
import pandas as pd
import tkinter as tk
import checkpoints as ck
from tkinter import ttk
from tkinter.font import Font
from modelos.separador import Separador
from modelos.formateador import Formateador
from modelos.administrador import Administrador
from modelos.testeador import Tester
from modelos.procesadores_principales import Inicial
from modelos.procesadores_principales import Segmentado
from modelos.procesadores_secundarios import Addendum
from modelos.cuadros_de_mensajes import Mensajes

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


def ocultar_y_mostrar(func):
    def wrapper(self, *args, **kwargs):
        self.ventana_top.withdraw()  # Oculta la ventana
        result = func(self, *args, **kwargs)  # Ejecuta el método
        try:
            self.ventana_top.deiconify()  # Muestra la ventana nuevamente
        except Exception:
            ...
        return result

    return wrapper


class Ventana_Base(Mensajes, Administrador):
    usuario = None
    color_botones = "#D0F2EF"
    botones_iniciales = "#F2F2F2"
    botones_segmentado = "#F2F2F2"
    botones_subir = "#F2F2F2"
    amarillo = "#EBDD04"
    rojo = "#EA3830"
    verde = "#27EA00"
    color_back = "#2493BF"

    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y-100}"


class Ventana_Principal(Ventana_Base):
    def __init__(self, master, version, usuario):
        self.crear_directorio_de_exportaciones()
        self.usuario = usuario
        self.version = version
        self.ventana = master
        self.ventana.title(f"ARIADNA -- {self.version}")
        self.ventana.ancho = 900
        self.ventana.alto = 250
        self.ventana.geometry(
            self.centrar_ventana(self.ventana, self.ventana.ancho, self.ventana.alto)
        )
        self.ventana.configure(bg=self.color_back)

        self.menu_inicial = [
            {
                "nombre": "uno",
                "texto": "Procesar Uno",
                "callback": lambda: self.procesar_inicial(),
            },
            {
                "nombre": "varios",
                "texto": "Procesar Varios",
                "callback": lambda: self.procesar_crudos(),
            },
            {
                "nombre": "errores",
                "texto": "Corregir Crudos",
                "callback": lambda: self.abrir_ventana_top_intermedia(
                    self.ventana_top, Ventana_errores
                ),
            },
            {
                "nombre": "separar",
                "texto": "Mapear archivos",
                "callback": lambda: self.mapear_archivos(),
            },
        ]
        self.menu_segmentado = [
            {
                "nombre": "uno",
                "texto": "Procesar Uno",
                "callback": lambda: self.procesar_final(),
            },
            {
                "nombre": "varios",
                "texto": "Procesar Varios",
                "callback": lambda: self.evaluar_si_todos_unos(),
            },
            {
                "nombre": "indices",
                "texto": "Setear Índices",
                "callback": lambda: self.abrir_ventana_top_intermedia(
                    self.ventana_top, Ventana_indices, indices=self.indices
                ),
            },
            {
                "nombre": "compilar",
                "texto": "Compilar archivos",
                "callback": lambda: self.compilar_archivos(),
            },
        ]
        self.menu_subir = [
            {
                "nombre": "conectar",
                "texto": "Conectar con base",
                "callback": lambda: self.abrir_ventana_top_intermedia(
                    self.ventana_top, Ventana_conectar
                ),
            },
            {
                "nombre": "testear",
                "texto": "Testear integridad",
                "callback": lambda: self.chequear_integridad(self.ventana_top),
            },
            {
                "nombre": "subir",
                "texto": "Subir a Base",
                "callback": lambda: self.subir_a_base(self.ventana_top),
            },
        ]

        self.loguear_info("")
        self.loguear_info("")
        self.loguear_info("")
        self.loguear_info(
            "------------------------ NUEVO INICIO DE SISTEMA ------------------------"
        )
        self.loguear_info(f"Versión de la app: {self.version}")
        self.loguear_info(f"Usuario logueado: {self.usuario}")
        self.imprimir_con_color(f"Bienvenido/a, {usuario}", "azul", loguear=False)
        print("\n")
        self.setear_indices()
        self.crear_botones()

    def crear_botones(self):
        x_pos = 50
        y_pos = int(self.ventana.alto / 2)
        estilo_fuente = ("Palatino Linotype", 16)
        b_alto = 75
        b_ancho = 200
        bg_color = self.color_botones

        separacion = 100

        boton_inicial = tk.Button(
            self.ventana,
            text="INICIAL",
            bg=bg_color,
            fg="black",
            font=estilo_fuente,
            command=lambda: self.abrir_ventana_intermedia(
                self.menu_inicial, "PROCESAR CRUDOS", self.botones_iniciales
            ),
        )
        boton_inicial.place(
            x=x_pos,
            y=y_pos - (b_alto / 2),
            width=b_ancho,
            height=b_alto,
        )

        boton_segmentado = tk.Button(
            self.ventana,
            text="SEGMENTADO",
            bg=bg_color,
            fg="black",
            font=estilo_fuente,
            command=lambda: self.abrir_ventana_intermedia(
                self.menu_segmentado, "PROCESAR FINALES", self.botones_segmentado
            ),
        )
        boton_segmentado.place(
            x=x_pos + separacion + b_ancho,
            y=y_pos - (b_alto / 2),
            width=b_ancho,
            height=b_alto,
        )

        boton_subir = tk.Button(
            self.ventana,
            text="SUBIR A BASE",
            bg=bg_color,
            fg="black",
            font=estilo_fuente,
            command=lambda: self.abrir_ventana_intermedia(
                self.menu_subir, "SUBIR ARCHIVO A BASE", self.botones_subir
            ),
        )
        boton_subir.place(
            x=x_pos + (separacion + b_ancho) * 2,
            y=y_pos - (b_alto / 2),
            width=b_ancho,
            height=b_alto,
        )

    def setear_indices(self):
        self.id_hechos = tk.IntVar()
        self.id_calificaciones = tk.IntVar()
        self.id_automotores = tk.IntVar()
        self.id_armas = tk.IntVar()
        self.id_objetos = tk.IntVar()
        self.id_secuestros = tk.IntVar()
        self.id_involucrados = tk.IntVar()

        self.id_hechos.set(1)
        self.id_calificaciones.set(1)
        self.id_automotores.set(1)
        self.id_armas.set(1)
        self.id_objetos.set(1)
        self.id_secuestros.set(1)
        self.id_involucrados.set(1)

        self.indices = (
            self.id_hechos,
            self.id_calificaciones,
            self.id_armas,
            self.id_automotores,
            self.id_objetos,
            self.id_secuestros,
            self.id_involucrados,
        )

    @ocultar_y_mostrar
    def procesar_inicial(self):
        #::::::::::::::::::::::::procesado inicial:::::::::::::::::::::::::::
        self.ventana_top.withdraw()
        try:
            path = self.seleccionar_archivo("/Exportaciones/Crudos/")

            nombre_archivo = os.path.splitext(os.path.basename(path))[0]

            formateador = Formateador()
            archivo = self._cargar(path)
            tester = Tester(archivo)
            if len(tester.errores) > 0:
                log_errores = self._convertir_inicial(
                    tester.errores,
                    ["indice", "n° registro", "para enmendar"],
                    nombre=nombre_archivo,
                    error=True,
                )
                self.imprimir_con_color(
                    "Hubo errores en los listados.Se ha generado un registro errores.",
                    "amarillo",
                )
                self.mostrar_mensaje_advertencia(
                    "Hubo errores en los listados.\nSe ha generado un registro errores.",
                )
                os.startfile(log_errores)
            else:
                self.imprimir_con_color(f"Procesando {nombre_archivo}...", "lila")
                archivo, identificadores = formateador._formatear(archivo, ck.cp_iden)
                inicial = Inicial(archivo, identificadores)
                path = self._convertir_inicial(
                    inicial.sin_duplicados, ck.general, nombre=nombre_archivo
                )
                self.imprimir_con_color(f"{nombre_archivo} listo.", "verde")
                self.mostrar_mensaje_info(
                    "El archivo fue procesado correctamente.",
                )
                if self.mostrar_mensaje_pregunta(
                    "¿Desea proceder a segmentar el archivo?"
                ):
                    self.procesar_final(path)
        except FileNotFoundError:
            self.mostrar_mensaje_advertencia("No se ha seleccionado ningún archivo.")

        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    @ocultar_y_mostrar
    def procesar_final(self, path=False):
        if not self.todos_unos(self.indices):
            indices = list(map(lambda var: var.get(), self.indices))
            self._cargar_no_segmentado(path, indices)
        else:
            self.mostrar_mensaje_info("Antes de segmentar, primero setee los indices.")
            self.abrir_ventana_top_intermedia(
                self.ventana_top, Ventana_indices, self.indices
            )
            indices = list(map(lambda var: var.get(), self.indices))
            self.ventana_top.withdraw()
            self._cargar_no_segmentado(path, indices)

    def _cargar_no_segmentado(self, path, indices):
        try:
            if path is False:
                path_archivo = self.seleccionar_archivo(
                    "/Exportaciones/No segmentados/"
                )
                archivo1 = self._cargar(
                    path_archivo,
                    no_tiene_encabezados=False,
                )
                nombre_archivo = os.path.splitext(os.path.basename(path_archivo))[0]
                segmentado = Segmentado(archivo1, indices)
                try:
                    self.imprimir_con_color(f"Procesando {nombre_archivo}...", "lila")
                    self._convertir_segmentado(
                        segmentado.final, nombre=nombre_archivo.replace(" (ns)", "")
                    )
                    self.imprimir_con_color(
                        f"El proceso se completo correctamente",
                        "verde",
                    )
                    mensaje = Formateador.comprobar_salida(segmentado.final)
                    if mensaje != "":
                        self.mostrar_mensaje_advertencia(mensaje)
                        self.imprimir_con_color(f"{mensaje}", "amarillo")
                    self.mostrar_mensaje_info("El proceso se completo correctamente.")
                except AttributeError:
                    self.mostrar_mensaje_advertencia(
                        "El proceso de segmentado se ha abortado."
                    )
                    ventana_errores = Ventana_addendum(
                        self.ventana, archivo=segmentado.errores
                    )
                except Exception as error:
                    self.imprimir_con_color(f"{error}", "rojo")
            else:
                nombre_archivo = os.path.splitext(os.path.basename(path))[0]
                archivo1 = self._cargar(path, no_tiene_encabezados=False)
                segmentado = Segmentado(archivo1, indices)
                try:
                    self.imprimir_con_color(f"Procesando {nombre_archivo}...", "lila")
                    self._convertir_segmentado(
                        segmentado.final, nombre=nombre_archivo.replace(" (ns)", "")
                    )
                    self.imprimir_con_color(
                        f"El proceso se completo correctamente",
                        "verde",
                    )
                    mensaje = Formateador.comprobar_salida(segmentado.final)
                    if mensaje != "":
                        self.mostrar_mensaje_advertencia(mensaje)
                        self.imprimir_con_color(f"{mensaje}", "amarillo")
                    self.mostrar_mensaje_info("El proceso se completo correctamente.")
                except AttributeError:
                    self.mostrar_mensaje_advertencia(
                        "El proceso de segmentado se ha abortado."
                    )
                    ventana_errores = Ventana_addendum(
                        self.ventana, archivo=segmentado.errores
                    )
                except Exception as error:
                    self.imprimir_con_color(f"{error}", "rojo")
        except FileNotFoundError:
            self.mostrar_mensaje_advertencia("No se ha seleccionado ningún archivo.")

    @ocultar_y_mostrar
    def procesar_crudos(self, path=False):
        try:
            carpeta = self.seleccionar_carpeta("/Exportaciones/Crudos/")
            archivos = os.listdir(carpeta)
            formateador = Formateador()

            for archivo in archivos:
                path = os.path.join(
                    carpeta, archivo
                )  # Obtener la ruta completa del archivo
                if os.path.isfile(path):  # Comprobar si es un archivo (no una carpeta)
                    try:
                        nombre_archivo = os.path.splitext(os.path.basename(path))[0]
                        archivo0 = self._cargar(path)
                        try:
                            tester = Tester(archivo0)
                            try:
                                if len(tester.errores) > 0:
                                    log_errores = self._convertir_inicial(
                                        tester.errores,
                                        ["indice", "n° registro", "para enmendar"],
                                        nombre=nombre_archivo,
                                        error=True,
                                    )
                                else:
                                    archivo0, identificadores = formateador._formatear(
                                        archivo0, ck.cp_iden
                                    )
                                    inicial = Inicial(archivo0, identificadores)
                                    path = self._convertir_inicial(
                                        inicial.sin_duplicados,
                                        ck.general,
                                        nombre=nombre_archivo,
                                    )
                            except Exception as error:
                                self.imprimir_con_color(
                                    f"({archivo}) Error en etapa de procesado del archivo: {error}",
                                    "rojo",
                                )
                        except Exception as error:
                            self.imprimir_con_color(
                                f"({archivo}) Error en etapa de testeo de información entrante: {error}",
                                "rojo",
                            )
                    except Exception as error:
                        self.imprimir_con_color(
                            f"({archivo}) Error en etapa de carga del archivo crudo: {error}",
                            "rojo",
                        )
                self.imprimir_con_color(f"Listo {archivo}", "verde")
            self.mostrar_mensaje_info(
                "El procesado de crudos ha sido completado.",
            )
        except FileNotFoundError:
            self.mostrar_mensaje_advertencia("No se ha seleccionado ninguna carpeta.")

    def evaluar_si_todos_unos(self):
        if not self.todos_unos(self.indices):
            try:
                carpeta = self.seleccionar_carpeta("/Exportaciones/No segmentados/")
                archivos = os.listdir(carpeta)
                indices = list(map(lambda var: var.get(), self.indices))
                self.procesar_varios(carpeta, archivos, indices)
            except FileNotFoundError:
                self.mostrar_mensaje_advertencia(
                    "No se ha seleccionado ninguna carpeta."
                )
        else:
            try:
                self.mostrar_mensaje_info(
                    "Antes de segmentar, primero setee los indices."
                )
                self.abrir_ventana_top_intermedia(
                    self.ventana_top, Ventana_indices, self.indices
                )
                indices = list(map(lambda var: var.get(), self.indices))
                carpeta = self.seleccionar_carpeta("/Exportaciones/No segmentados/")
                archivos = os.listdir(carpeta)
                self.procesar_varios(carpeta, archivos, indices)
            except FileNotFoundError:
                self.mostrar_mensaje_advertencia(
                    "No se ha seleccionado ninguna carpeta."
                )

    @ocultar_y_mostrar
    def procesar_varios(self, carpeta, archivos, indices):
        for archivo in archivos:
            path = os.path.join(
                carpeta, archivo
            )  # Obtener la ruta completa del archivo
            if os.path.isfile(path):  # Comprobar si es un archivo (no una carpeta)
                try:
                    archivo1 = self._cargar(path, no_tiene_encabezados=False)
                    try:
                        segmentado = Segmentado(archivo1, indices, carpeta=True)
                        try:
                            mensaje = Formateador.comprobar_salida(segmentado.final)
                            if mensaje != "":
                                self.imprimir_con_color(
                                    f"Advertencia {mensaje}", "amarillo"
                                )
                            try:
                                print("\n")
                                self.imprimir_con_color(f"Preparando {archivo}", "lila")
                                self._convertir_segmentado(
                                    segmentado.final, nombre=archivo
                                )
                                try:
                                    indices_finales = self._obtener_indices(
                                        segmentado.final, indices
                                    )
                                    self.imprimir_con_color(
                                        f"Iniciales:---{str(indices)}",
                                        "blanco",
                                    )
                                    self.imprimir_con_color(
                                        f"Finales:-----{str(indices_finales)}",
                                        "blanco",
                                    )
                                    indices = list(
                                        map(lambda x: x + 1, indices_finales)
                                    )
                                    self.imprimir_con_color(
                                        f"Siguientes:--{str(indices)}", "blanco"
                                    )
                                except Exception as error:
                                    self.imprimir_con_color(
                                        f"({archivo}) Error en la obtención de índices nuevos: {error}",
                                        "rojo",
                                    )
                            except Exception as error:
                                self.imprimir_con_color(
                                    f"({archivo}) Error en conversión final a formato Excel: {error}",
                                    "rojo",
                                )
                        except AttributeError:
                            self.imprimir_con_color(
                                f"SE DETECTARON CALIFICACIONES NO EXISTENTES EN BASE",
                                "rojo",
                            )
                            ventana_errores = Ventana_addendum(
                                self.ventana, archivo=segmentado.errores
                            )
                        except Exception as error:
                            self.imprimir_con_color(
                                f"({archivo}) Error en la comprobación de datos salientes: {error}",
                                "rojo",
                            )
                    except Exception as error:
                        self.imprimir_con_color(
                            f"({archivo}) Error en etapa de procesado: {error}",
                            "rojo",
                        )
                except Exception as error:
                    self.imprimir_con_color(
                        f"({archivo}) Error en etapa de carga: {error}", "rojo"
                    )
            self.imprimir_con_color(f"Listo {archivo}", "verde")
        self.mostrar_mensaje_info(
            "Procesado completo.",
        )

    @ocultar_y_mostrar
    def compilar_archivos(self):
        carpeta = self.seleccionar_carpeta("/Exportaciones/Segmentados/")
        print("\n")
        try:
            archivos = os.listdir(carpeta)

            # Nombre del archivo final
            archivo_final = f"{carpeta}/consolidado.xlsx"

            # Leer la primera hoja de un archivo para obtener los nombres de las hojas
            primer_archivo = f"{carpeta}/{archivos[0]}"
            with pd.ExcelFile(primer_archivo) as xls:
                hojas = xls.sheet_names

            # Almacenar los datos en un diccionario por hoja
            datos = {}
            for hoja in hojas:
                datos[hoja] = pd.DataFrame()

            # Leer los archivos de Excel y almacenar los datos en el diccionario
            for archivo in archivos:
                with pd.ExcelFile(f"{carpeta}/{archivo}") as xls:
                    for hoja in hojas:
                        df = pd.read_excel(xls, sheet_name=hoja)
                        if hoja == "datos_hecho":
                            df["Latitud:"] = df["Latitud:"].astype(str)
                            df["Longitud:"] = df["Longitud:"].astype(str)
                        datos[hoja] = pd.concat([datos[hoja], df])
                self.imprimir_con_color(f"Listo {archivo}", "verde")

            # Escribir los datos consolidados en un archivo de Excel
            with pd.ExcelWriter(archivo_final) as writer:
                self.imprimir_con_color("\n")
                self.imprimir_con_color("Comenzando proceso de compilación...", "lila")
                for hoja, df in datos.items():
                    df.to_excel(writer, sheet_name=hoja, index=False)

            self.imprimir_con_color("Analizando coherencia de indexados...", "lila")
            try:
                if self.comprobar_indices(f"{carpeta}/consolidado.xlsx"):
                    self.imprimir_con_color(
                        "Chequeada coherencia de indexados sin errores", "verde"
                    )
                else:
                    self.imprimir_con_color(
                        "Se detectaron errores de coherencia en los indexados", "rojo"
                    )
            except Exception as error:
                self.imprimir_con_color(error, "rojo")
            self.imprimir_con_color(
                f"Se ha creado el archivo consolidado en: {archivo_final}", "blanco"
            )
        except FileNotFoundError:
            self.mostrar_mensaje_advertencia("Ninguna carpeta seleccionada")
        except Exception as error:
            self.mostrar_mensaje_error(f"{error}")

    @ocultar_y_mostrar
    def mapear_archivos(self):
        respuesta = self.mostrar_mensaje_pregunta("Desea procesar un archivo o una carpeta? Para archivo, presione SI. De lo controario, NO.")
        try:
            separador = Separador()
            if respuesta:
                separador.procesar_uno()
            else:
                separador.procesar_archivos()
                self.mostrar_mensaje_info("La carpeta ha sido mapeada y sus archivos separados con éxito.")
        except WindowsError:
            self.imprimir_con_color("Nada seleccionado.", "blanco")
            self.mostrar_mensaje_advertencia("Nada seleccionado.")
        except Exception as error:
            self.imprimir_con_color(f"Error inesperado: {error}", "rojo")
            self.mostrar_mensaje_error(f"Error inesperado: {error}")

    def _archivos(self):
        carpeta = self.seleccionar_archivo("/Exportaciones/Segmentados/")
        print("\n")
        archivos = os.listdir(carpeta)

        # Nombre del archivo final
        archivo_final = f"{carpeta}/consolidado.xlsx"

        # Leer la primera hoja de un archivo para obtener los nombres de las hojas
        primer_archivo = f"{carpeta}/{archivos[0]}"
        with pd.ExcelFile(primer_archivo) as xls:
            hojas = xls.sheet_names

        # Almacenar los datos en un diccionario por hoja
        datos = {}
        for hoja in hojas:
            datos[hoja] = pd.DataFrame()

        # Leer los archivos de Excel y almacenar los datos en el diccionario
        for archivo in archivos:
            with pd.ExcelFile(f"{carpeta}/{archivo}") as xls:
                for hoja in hojas:
                    df = pd.read_excel(xls, sheet_name=hoja)
                    if hoja == "datos_hecho":
                        df["Latitud:"] = df["Latitud:"].astype(str)
                        df["Longitud:"] = df["Longitud:"].astype(str)
                    datos[hoja] = pd.concat([datos[hoja], df])
            self.imprimir_con_color(f"Listo {archivo}", "verde")

        # Escribir los datos consolidados en un archivo de Excel
        with pd.ExcelWriter(archivo_final) as writer:
            print("\n")
            self.imprimir_con_color("Comenzando proceso de compilación...", "lila")
            for hoja, df in datos.items():
                df.to_excel(writer, sheet_name=hoja, index=False)

        self.imprimir_con_color("Analizando coherencia de indexados...", "lila")
        try:
            if self.comprobar_indices(f"{carpeta}/consolidado.xlsx"):
                self.imprimir_con_color(
                    "Chequeada coherencia de indexados sin errores", "verde"
                )
            else:
                self.imprimir_con_color(
                    "Se detectaron errores de coherencia en los indexados", "rojo"
                )
        except Exception as error:
            self.imprimir_con_color(error, "rojo")
        self.imprimir_con_color(
            f"Se ha creado el archivo consolidado en: {archivo_final}", "blanco"
        )

    def comprobar_indices(self, archivo):
        # Leer el archivo Excel
        xls = pd.ExcelFile(archivo)

        # Lista para almacenar las tuplas de cada hoja
        tuplas_hojas = []

        # Recorrer cada hoja del archivo

        for hoja_nombre in xls.sheet_names:
            # Leer la hoja y obtener los valores de la primera columna
            df = pd.read_excel(xls, sheet_name=hoja_nombre)
            columna = df.iloc[:, 0]  # Primera columna (index 0)

            # Convertir la columna en una tupla y agregarla a la lista
            tupla_hoja = tuple(columna.values[0:])  # Excluir el encabezado
            tuplas_hojas.append(tupla_hoja)

            # Verificar si la lista contiene enteros consecutivos en orden ascendente
            for tupla in tuplas_hojas:
                if not tupla:  # Si la lista está vacía, no se considera consecutiva
                    break

                n = tupla[0]  # Primer elemento de la lista
                for num in tupla:
                    if num != n:  # Si el número no es igual a n, no es consecutivo
                        return False
                    n += 1  # Incrementar n para verificar el siguiente número
        return True

    def comprobar_fechas(self, archivo, fecha=True):
        xls = pd.ExcelFile(archivo)
        df = pd.read_excel(xls, sheet_name="datos_hecho")
        columna = df.iloc[:, 3]
        fechas = sorted(list(set(columna.astype(str).values[0:])))
        if fecha:
            if len(fechas) == 1:
                return True, "(FECHA INDIVIDUAL) Coherencia comprobada"
            else:
                return (
                    False,
                    f"(FECHA INDIVIDUAL) Error en coherencia. Demasiadas fechas en archivo: {fechas}",
                )

        else:
            mes = []
            for fecha in fechas:
                fecha_ = datetime.datetime.strptime(fecha, "%Y-%m-%d")
                mes.append(fecha_.strftime("%B").upper())
            mes_final = list(set(mes))
            if 29 < len(fechas) < 32:
                if len(mes_final) == 1:
                    return (
                        True,
                        f"(MES) Coherencia comprobada. Fechas correspondientes a: {mes_final[0]}",
                    )
                else:
                    return (
                        False,
                        f"(MES) Error en coherencia. Demasiados meses en archivo: {mes_final}",
                    )
            elif 27 < len(fechas) < 30:
                if mes_final[0] == "FEBRERO":
                    if len(mes_final) == 1:
                        return (
                            True,
                            f"(MES) Coherencia comprobada. Fechas correspondientes a: {mes_final[0]}",
                        )
                    else:
                        return (
                            False,
                            f"(MES) Error en coherencia. Demasiados meses en archivo: {mes_final}",
                        )
                else:
                    return (
                        False,
                        f"(MES) Error en coherencia. El mes no contiene 28 o 29 días y no es febrero: {mes_final}",
                    )
            else:
                return False, f"(MES) Error en coherencia: {fechas}"

    def comprobar_nulos(self, archivo, advertencias=True):
        res2 = Formateador.comprobar_salida(archivo, advertencias=advertencias)
        return res2

    def abrir_ventana_intermedia(self, widgets, titulo, colores_botones):
        self.ventana_top = Ventana_Intermedia(
            self.ventana, widgets, titulo, colores_botones
        )
        self.cambiar_de_ventana(self.ventana, self.ventana_top)

    def abrir_ventana_top_intermedia(self, main, Clase, indices=False):
        if not indices:
            self.ventana_top_intermedia = Clase(main)
            self.cambiar_de_ventana(main, self.ventana_top_intermedia)
        else:
            self.ventana_top_intermedia = Clase(main, indices)
            self.cambiar_de_ventana(main, self.ventana_top_intermedia)

    def cambiar_de_ventana(self, main, top):
        main.withdraw()
        main.wait_window(top)
        main.deiconify()

    @ocultar_y_mostrar
    def chequear_integridad(self, ventana):
        print("\n\n")
        path = self.seleccionar_archivo("/Exportaciones/Segmentados")
        if path:
            respuesta = self.mostrar_mensaje_pregunta(
                "¿El archivo seleccionado corresponde a una fecha individual? En caso de que sea un mes, ELEGIR NO",
            )
            self.imprimir_con_color(
                "Iniciando chequeo de integridad de archivo...", "lila"
            )
            self.imprimir_con_color(f"{path}", "lila")
            # COMPROBAR FECHAS
            if respuesta:
                # COMPROBAR INDICES DE FECHA
                try:
                    if self.comprobar_indices(path):
                        self.imprimir_con_color("CHEQUEO: Indices correctos", "verde")
                        # COMPROBAR COHERENCIA DE FECHA
                        try:
                            res = self.comprobar_fechas(path)
                            if res[0]:
                                self.imprimir_con_color(f"CHEQUEO: {res[1]}", "verde")
                                # COMPROBAR INTEGRIDAD DE TABLAS Y CAMPOS NO NULOS
                                try:
                                    archivo_final = self._cargar_final(path)
                                    res2 = self.comprobar_nulos(
                                        archivo_final, advertencias=False
                                    )
                                    if res2 == "":
                                        self.imprimir_con_color(
                                            f"CHEQUEO: Comprobados campos no nulos",
                                            "verde",
                                        )
                                        self.mostrar_mensaje_info(
                                            "Comprobados índices, tablas, y campos no nulos. Integridad de archivo CORRECTA",
                                        )
                                        self.imprimir_con_color(
                                            "CHEQUEO: Comprobados índices, tablas, y campos no nulos. Integridad de archivo CORRECTA",
                                            "verde",
                                        )
                                        ventana.botones[1].config(bg=self.verde)
                                        ventana.a_subir = archivo_final
                                    else:
                                        self.mostrar_mensaje_advertencia(f"{res2}")
                                        self.imprimir_con_color(
                                            f"CHEQUEO: {res2}", "amarillo"
                                        )
                                        ventana.botones[1].config(bg=self.amarillo)
                                except Exception as error:
                                    self.mostrar_mensaje_error(
                                        f"Error al comprobar nulos: {error}"
                                    )
                                    self.imprimir_con_color(
                                        f"CHEQUEO: Error al comprobar nulos: {error}",
                                        "rojo",
                                    )
                                    ventana.botones[1].config(bg=self.rojo)
                            else:
                                self.mostrar_mensaje_advertencia(f"{res[1]}")
                                self.imprimir_con_color(
                                    f"CHEQUEO: {res[1]}", "amarillo"
                                )
                                ventana.botones[1].config(bg=self.amarillo)
                        except Exception as error:
                            self.mostrar_mensaje_error(
                                f"Error al comprobar fechas: {error}"
                            )
                            self.imprimir_con_color(
                                f"CHEQUEO: Error al comprobar fechas: {error}", "rojo"
                            )
                            ventana.botones[1].config(bg=self.rojo)
                    else:
                        self.mostrar_mensaje_advertencia(f"Indices INCORRECTOS.")
                        self.imprimir_con_color(
                            f"CHEQUEO: Indices INCORRECTOS.", "amarillo"
                        )
                        ventana.botones[1].config(bg=self.amarillo)
                except Exception as error:
                    self.mostrar_mensaje_error(f"Error al comprobar índices: {error}")
                    self.imprimir_con_color(
                        f"CHEQUEO: Error al comprobar índices: {error}", "rojo"
                    )
                    ventana.botones[1].config(bg=self.rojo)

            # COMPROBAR MES
            else:
                # COMPROBAR INDICES DE MES
                try:
                    if self.comprobar_indices(path):
                        self.imprimir_con_color("CHEQUEO: Indices correctos.", "verde")
                        # COMPROBAR COHERENCIA DE MES
                        try:
                            res = self.comprobar_fechas(path, fecha=False)
                            if res[0]:
                                self.imprimir_con_color(f"CHEQUEO: {res[1]}", "verde")
                                # COMPROBAR INTEGRIDAD DE TABLAS Y CAMPOS NO NULOS
                                try:
                                    archivo_final = self._cargar_final(path)
                                    res2 = self.comprobar_nulos(
                                        archivo_final, advertencias=False
                                    )
                                    if res2 == "":
                                        self.imprimir_con_color(
                                            f"CHEQUEO: Comprobados campos no nulos",
                                            "verde",
                                        )
                                        self.mostrar_mensaje_info(
                                            "Comprobados índices, tablas, y campos no nulos. Integridad de archivo CORRECTA",
                                        )
                                        self.imprimir_con_color(
                                            f"CHEQUEO: Comprobados índices, tablas, y campos no nulos. Integridad de archivo CORRECTA",
                                            "verde",
                                        )
                                        ventana.botones[1].config(bg=self.verde)
                                        ventana.a_subir = archivo_final
                                    else:
                                        self.mostrar_mensaje_advertencia(f"{res2}")
                                        self.imprimir_con_color(
                                            f"CHEQUEO: {res2}", "amarillo"
                                        )
                                        ventana.botones[1].config(bg=self.amarillo)
                                except Exception as error:
                                    self.mostrar_mensaje_error(
                                        f"Error al comprobar nulos: {error}"
                                    )
                                    self.imprimir_con_color(
                                        f"CHEQUEO: Error al comprobar nulos: {error}",
                                        "rojo",
                                    )
                                    ventana.botones[1].config(bg=self.rojo)
                            else:
                                self.mostrar_mensaje_advertencia(f"{res[1]}")
                                self.imprimir_con_color(
                                    f"CHEQUEO: {res[1]}", "amarillo"
                                )
                                ventana.botones[1].config(bg=self.amarillo)
                        except Exception as error:
                            self.mostrar_mensaje_error(
                                f"Error al comprobar fechas: {error}"
                            )
                            self.imprimir_con_color(
                                f"CHEQUEO: Error al comprobar fechas: {error}", "rojo"
                            )
                            ventana.botones[1].config(bg=self.rojo)
                    else:
                        self.mostrar_mensaje_advertencia("Indices INCORRECTOS.")
                        self.imprimir_con_color(
                            "CHEQUEO: Indices INCORRECTOS.", "amarillo"
                        )
                        ventana.botones[1].config(bg=self.amarillo)
                except Exception as error:
                    self.mostrar_mensaje_error(f"Error al comprobar índices: {error}")
                    self.imprimir_con_color(
                        f"CHEQUEO: Error al comprobar índices: {error}", "rojo"
                    )
                    ventana.botones[1].config(bg=self.rojo)
        else:
            self.mostrar_mensaje_advertencia("Ningún archivo seleccionado")

    @ocultar_y_mostrar
    def subir_a_base(self, ventana):
        def obtener_indices_archivo(lista_compuesta):
            primeros_elementos = []
            for lista_anidada in lista_compuesta:
                if lista_anidada:  # Comprobar si la lista anidada no está vacía
                    primera_lista_anidada = lista_anidada[0]
                    if (
                        primera_lista_anidada
                    ):  # Comprobar si la última lista anidada no está vacía
                        primer_elemento_ultima_lista = primera_lista_anidada[0]
                        primeros_elementos.append(primer_elemento_ultima_lista)
                else:
                    primeros_elementos.append(None)
            del primeros_elementos[1]
            return primeros_elementos

        def chequear_continuidad(indices_base, indices_archivo):
            for i in range(0, len(indices_base)):
                if indices_base[i] != indices_archivo[i] - 1:
                    return False
                return True

        def filtrar(lista, campos_a_recortar):
            final = [lista[i] for i in campos_a_recortar]
            final2 = [None if pd.isnull(value) else value for value in final]
            return final2

        def insertar(cursor, nombre_tabla, data, recorte, campos):
            data2 = list(map(lambda x: filtrar(x, recorte), data))
            try:
                consulta = rf"INSERT INTO {nombre_tabla} ({', '.join(campos)}) VALUES ({', '.join('%s' for _ in data2[0])})"
                self.imprimir_con_color(
                    f"Preparando '{nombre_tabla}' para inserción...", "lila"
                )
                cursor.executemany(consulta, data2)
            except Exception as error:
                self.mostrar_mensaje_error(
                    f"Error durante la inserción en {nombre_tabla}", f"{error}"
                )
                raise error

        print("\n\n")

        conexion = mysql.connector.connect(
            host=ventana.conexion[0],
            port=ventana.conexion[1],
            user=ventana.conexion[2],
            password=ventana.conexion[3],
            database=ventana.conexion[4],
            charset="utf8",
        )

        cursor = conexion.cursor()

        self.imprimir_con_color("Preparando inserción en base...", "verde")
        indices_archivo = obtener_indices_archivo(ventana.a_subir)
        self.imprimir_con_color("Chequeando continuidad de indexados...", "lila")
        if chequear_continuidad(ventana.indices, indices_archivo):
            self.imprimir_con_color(
                "CHEQUEO: continuidad de íncides correcta.", "verde"
            )
            print("\n")
            self.imprimir_con_color("Iniciando inserción de datos en base...", "lila")
            try:
                if indices_archivo[0]:
                    insertar(
                        cursor,
                        "datos_hecho",
                        ventana.a_subir[0],
                        ck.base_de_datos_recortes["datos_hecho"],
                        ck.base_de_datos["datos_hecho"],
                    )
                else:
                    self.mostrar_mensaje_advertencia(
                        "No se ha insertado la tabla 'datos_hecho' ya que no contenía registros."
                    )

                if indices_archivo[1]:
                    insertar(
                        cursor,
                        "armas",
                        ventana.a_subir[2],
                        ck.base_de_datos_recortes["elementos"],
                        ck.base_de_datos["armas"],
                    )
                else:
                    self.mostrar_mensaje_advertencia(
                        "No se ha insertado la tabla 'armas' ya que no contenía registros."
                    )

                if indices_archivo[2]:
                    insertar(
                        cursor,
                        "automotores",
                        ventana.a_subir[3],
                        ck.base_de_datos_recortes["elementos"],
                        ck.base_de_datos["automotores"],
                    )
                else:
                    self.mostrar_mensaje_advertencia(
                        "No se ha insertado la tabla 'automotores' ya que no contenía registros."
                    )

                if indices_archivo[3]:
                    insertar(
                        cursor,
                        "objetos",
                        ventana.a_subir[4],
                        ck.base_de_datos_recortes["elementos"],
                        ck.base_de_datos["elementos"],
                    )
                else:
                    self.mostrar_mensaje_advertencia(
                        "No se ha insertado la tabla 'objetos' ya que no contenía registros."
                    )

                if indices_archivo[4]:
                    insertar(
                        cursor,
                        "secuestros",
                        ventana.a_subir[5],
                        ck.base_de_datos_recortes["elementos"],
                        ck.base_de_datos["elementos"],
                    )
                else:
                    self.mostrar_mensaje_advertencia(
                        "No se ha insertado la tabla 'secuestros' ya que no contenía registros."
                    )

                if indices_archivo[5]:
                    insertar(
                        cursor,
                        "involucrados",
                        ventana.a_subir[6],
                        ck.base_de_datos_recortes["involucrados"],
                        ck.base_de_datos["involucrados"],
                    )
                else:
                    self.mostrar_mensaje_advertencia(
                        "No se ha insertado la tabla 'involucrados' ya que no contenía registros.",
                    )
                conexion.commit()
                self.mostrar_mensaje_info(
                    "Archivo insertado correctamente.",
                )
                self.imprimir_con_color("Archivo insertado correctamente.", "verde")
                ventana.destroy()
            except Exception as error:
                self.mostrar_mensaje_advertencia(
                    f"Una de las tablas tuvo problemas de inserción. Se aborta subida a base. \n\n Error: {error}",
                )
        else:
            self.mostrar_mensaje_advertencia(
                "Los índices del archivo que se intenta subir no son continuos al indexado de la base. Se aborta proceso de inserción ya que generaría problemas de coherencia de índices primarios.",
            )
            self.imprimir_con_color(
                "Los índices del archivo que se intenta subir no son continuos al indexado de la base. Se aborta proceso de inserción ya que generaría problemas de coherencia de índices primarios.",
                "amarillo",
            )
        conexion.close()

    @staticmethod
    def todos_unos(lista):
        for elemento in lista:
            if elemento.get() != 1:
                return False
        return True

    def iniciar(self):
        self.ventana.mainloop()


class Ventana_Intermedia(tk.Toplevel, Ventana_Base):
    def __init__(self, ventana_principal, widgets, titulo, color_botones):
        super().__init__(ventana_principal)
        self.widgets = widgets
        self.title(titulo)
        self.ancho = 400
        self.alto = 450
        self.geometry(self.centrar_ventana(ventana_principal, self.ancho, self.alto))
        self.configure(bg=self.color_back)
        self.crear_widgets(widgets, color_botones)

    def crear_widgets(self, wid, colores):
        widgets = copy.deepcopy(wid)
        color_botones = colores
        widgets.append(
            {
                "nombre": "volver",
                "texto": "Volver al menú",
                "callback": lambda: self.volver_a_principal(),
            }
        )

        estilo_fuente = ("Palatino Linotype", 16)
        b_alto = 50
        b_ancho = 250

        separacion = b_alto * 1.8
        x_pos = int(self.ancho / 2) - int(b_ancho / 2)
        y_pos = (self.alto / 2) - (
            ((b_alto * len(widgets)) + (separacion * (len(widgets) - 1))) / 1.5
        ) / 2

        self.botones = []

        for widget in widgets:
            widget["nombre"] = tk.Button(
                self,
                text=widget["texto"],
                bg=color_botones,
                fg="black",
                font=estilo_fuente,
                command=widget["callback"],
            )
            widget["nombre"].place(
                x=x_pos,
                y=y_pos,
                width=b_ancho,
                height=b_alto,
            )

            self.botones.append(widget["nombre"])

            y_pos += separacion

    def volver_a_principal(self):
        self.winfo_toplevel().deiconify()
        self.destroy()


class Ventana_addendum(tk.Toplevel, Ventana_Base):
    def __init__(
        self,
        ventana,
        archivo=[],
    ):
        super().__init__(ventana)
        self.title("Módulo Addendum")
        self.ancho = 400
        self.alto = 300
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.registros = archivo
        self.original = ""
        self.crear_widgets()

    def crear_widgets(self):
        # Crear treeview con 3 columnas
        self.control_entry = tk.StringVar()
        self.control_entry.set("")

        self.treeview = ttk.Treeview(self, columns=("id", "id_hecho", "calificacion"))

        # Configurar headers de las columnas
        self.treeview.heading("id", text="ID")
        self.treeview.heading("id_hecho", text="ID Hecho")
        self.treeview.heading("calificacion", text="Calificación")
        self.treeview.column("#0", minwidth=0, width=0, anchor="center")
        self.treeview.column("id", minwidth=0, width=30, anchor="center")
        self.treeview.column("id_hecho", minwidth=0, width=70, anchor="center")
        self.treeview.column("calificacion", minwidth=0, width=290, anchor="center")

        # Agregar datos al treeview (ejemplo)
        if len(self.registros) > 0:
            for registro in self.registros:
                self.treeview.insert(
                    "", "end", values=(registro[0], registro[1], registro[2])
                )

        self.treeview.bind(
            "<ButtonRelease-1>",
            lambda evento: self.seleccionar_item(self.treeview, self.control_entry),
        )
        self.treeview.pack()

        # Crear entry con label "seleccionado" al lado izquierdo
        self.entry_frame = ttk.Frame(self)
        self.entry_frame = ttk.Entry(self, textvariable=self.control_entry)
        self.entry_frame.pack()

        # Crear botón "Agregar a base"
        self.agregar_boton = ttk.Button(
            self,
            text="Agregar a base",
            command=lambda: self.agregar_a_base(self.entry_frame, self.original),
        )
        self.agregar_boton.pack(pady=10)

    def seleccionar_item(self, tree, entry):
        try:
            item_ = tree.focus()
            datos_registro = tree.item(item_)["values"][2]
            entry.set(datos_registro)
            self.original = datos_registro
        except Exception:
            ...

    def agregar_a_base(self, entry, original):
        # Lógica para agregar los datos a la base de datos
        # Leer el archivo Excel
        df = dict(
            pd.read_excel(
                rf"{self.DIRECTORIO_PADRE}\Base calificaciones\calificaciones_db.xlsx",
                header=None,
            ).values.tolist()
        )
        addendum = Addendum()
        simplificado = addendum.simplificada(original)

        # Agregar un nuevo registro
        df[simplificado] = entry.get()

        # convierto el dic en df
        df = list(df.items())
        df = pd.DataFrame(df)

        # Guardar los cambios en el archivo Excel
        df.to_excel(
            rf"{self.DIRECTORIO_PADRE}\Base calificaciones\calificaciones_db.xlsx",
            index=False,
            header=False,
        )
        self.mostrar_mensaje_info(
            "Se ha agregado la nueva carátula a la base de datos de calificaciones.",
        )


class Ventana_errores(tk.Toplevel, Ventana_Base):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.title("Módulo errores")
        self.ancho = 720
        self.alto = 200
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.corregido = None
        self.config(bg=self.color_back)
        self.crear_botones()

    def crear_botones(self):
        estilo_fuente = ("Palatino Linotype", 14)
        alto = 50
        ancho = 150
        separacion = 85
        y_pos = (self.alto / 2) - (alto / 2)
        x_pos = 50
        self.boton_original = tk.Button(
            self,
            text="Original",
            bg=self.rojo,
            width=10,
            font=estilo_fuente,
            command=lambda: self.cargar_original(),
        )
        self.boton_original.place(
            x=x_pos,
            y=y_pos,
            width=ancho,
            height=alto,
        )

        self.boton_enmendado = tk.Button(
            self,
            text="Enmendado",
            bg="#EA3830",
            width=10,
            font=estilo_fuente,
            command=lambda: self.cargar_enmendado(),
        )
        self.boton_enmendado.place(
            x=x_pos + (separacion + ancho) * 2,
            y=y_pos,
            width=ancho,
            height=alto,
        )

        self.boton_corregir = tk.Button(
            self,
            text="Corregir Original",
            font=estilo_fuente,
            bg=self.amarillo,
            command=lambda: self.corregir_original(),
        )
        self.boton_corregir.place(
            x=x_pos + (separacion + ancho),
            y=y_pos,
            width=ancho,
            height=alto,
        )

    def corregir_original(self):
        try:
            original = self._cargar(
                self.path_original,
            )
            enmendado = self._cargar(
                self.path_enmendado, no_tiene_encabezados=False, es_original=False
            )

            for error in enmendado:
                original[int(error[0])][0] = error[2]

            nombre_archivo = os.path.splitext(os.path.basename(self.path_original))[0]
            ult = pd.DataFrame(original)
            ult.to_excel(
                rf"{self.DIRECTORIO_PADRE}\Exportaciones\Corregidos\{nombre_archivo} (corregido).xlsx",
                index=False,
                header=False,
            )
            self.boton_corregir.config(bg="#27EA00")
            self.mostrar_mensaje_info("¡El archivo fue corredido correctamente!")
            return rf"{self.DIRECTORIO_PADRE}\Exportaciones\Corregidos\{nombre_archivo} (corregido).xlsx"
        except Exception as error:
            self.mostrar_mensaje_advertencia(
                f"Ha ocurrido el siguiente error:\n {error}"
            )

    def cargar_original(self):
        path = self.seleccionar_archivo("/Exportaciones/Crudos/")
        if path:
            self.path_original = path
            self.boton_original.config(bg=self.verde)
        else:
            self.mostrar_mensaje_advertencia("No se ha seleccionado ningún archivo.")

    def cargar_enmendado(self):
        path = self.seleccionar_archivo("/Exportaciones/Errores/")
        if path:
            self.path_enmendado = path
            self.boton_enmendado.config(bg="#27EA00")
        else:
            self.mostrar_mensaje_advertencia("No se ha seleccionado ningún archivo.")


class Ventana_indices(tk.Toplevel, Ventana_Base):
    def __init__(self, ventana, indices):
        super().__init__(ventana)
        self.title("Setear índices")
        self.ancho = 360
        self.alto = 300
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.configure(bg=self.color_back)
        self.crear_widgets(indices)

    def crear_widgets(self, indices):
        etiquetas = [
            "Hechos",
            "Calificaciones",
            "Armas",
            "Automotores",
            "Objetos",
            "Secuestros",
            "Involucrados",
        ]

        sep_x = 30
        sep_y = 0.5
        font_label = Font(weight="bold", size=9)
        self.etiquetas_labels = []
        self.etiquetas_entries = []

        for i, etiqueta_texto in enumerate(etiquetas):
            etiqueta = tk.Label(
                self,
                text=etiqueta_texto,
                font=font_label,
                fg="white",
                bg=self.color_back,
            )
            etiqueta.place(x=70, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_labels.append(etiqueta)

            cuadro_texto = tk.Entry(
                self,
                textvariable=indices[i],
            )
            cuadro_texto.place(x=160, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_entries.append(cuadro_texto)

        btn_base = tk.Button(
            self,
            text="Desde la Base",
            bg="orange",
            command=lambda: self.conectar_con_base(),
        )
        btn_base.place(x=155, y=250)

        btn_archivo = tk.Button(
            self,
            text="Desde archivo",
            bg="sky blue",
            command=lambda: self.conectar_con_archivo(),
        )
        btn_archivo.place(x=40, y=250)

        btn_setear_ids = tk.Button(
            self,
            text="Setear IDs",
            bg="light green",
            command=lambda: self.actualizar_indices(indices, self.etiquetas_entries),
        )
        btn_setear_ids.place(x=270, y=250)

    def actualizar_indices(self, indices, entries):
        for i, ind in enumerate(indices):
            ind.set(entries[i].get())
        self.mostrar_mensaje_info("Los índices fueron configurados correctamente")
        self.destroy()

    def conectar_con_base(self):
        try:
            indices = []

            try:
                conexion = mysql.connector.connect(
                    host="localhost", user="root", password="", database="delitos"
                )
            except Exception:
                conexion = mysql.connector.connect(
                    host="localhost",
                    port=3307,
                    user="root",
                    password="",
                    database="delitos",
                )

            # Crear un cursor para ejecutar consultas
            cursor = conexion.cursor()

            consulta = "SELECT max(id_hecho) FROM datos_hecho"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                indices.append(fila[0])

            indices.append(0)

            consulta = "SELECT max(id) FROM armas"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                indices.append(fila[0])

            consulta = "SELECT max(id) FROM automotores"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                indices.append(fila[0])

            consulta = "SELECT max(id) FROM objetos"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                indices.append(fila[0])

            consulta = "SELECT max(id) FROM secuestros"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                indices.append(fila[0])

            consulta = "SELECT max(id) FROM involucrados"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                indices.append(fila[0])

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            for i, ind in enumerate(indices):
                self.etiquetas_entries[i].delete(0, "end")
                self.etiquetas_entries[i].insert(0, ind + 1)

        except Exception as error:
            self.mostrar_mensaje_error(error)

    def conectar_con_archivo(self):
        ruta_archivo = self.seleccionar_archivo("/Exportaciones/Segmentados/")
        try:
            # Cargar el archivo Excel
            df = pd.read_excel(ruta_archivo, sheet_name=None)

            # Lista para almacenar los últimos registros
            ultimos_registros = []

            # Iterar sobre cada hoja del archivo
            for hoja, datos in df.items():
                # Obtener el último valor de la primera columna
                ultimo_registro = datos.iloc[-1, 0]
                ultimos_registros.append(ultimo_registro)

            for i, ind in enumerate(ultimos_registros):
                self.etiquetas_entries[i].delete(0, "end")
                self.etiquetas_entries[i].insert(0, ind + 1)

        except FileNotFoundError:
            self.mostrar_mensaje_info("No se ha seleccionado ningún archivo")


class Ventana_conectar(tk.Toplevel, Ventana_Base):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.title("Conectar con base")
        self.ancho = 360
        self.alto = 360
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.configure(bg=self.color_back)

        self.host = tk.StringVar()
        self.port = tk.StringVar()
        self.user = tk.StringVar()
        self.passw = tk.StringVar()
        self.base = tk.StringVar()

        self.host.set("localhost")
        self.port.set("3306")
        self.user.set("root")
        self.passw.set("")
        self.base.set("delitos")

        self.set_vars = [self.host, self.port, self.user, self.passw, self.base]

        self.indices = []

        self.crear_widgets(ventana)

    def crear_widgets(self, ventana):
        etiquetas = ["HOST: ", "PORT: ", "USER: ", "PASS: ", "DATABASE: "]

        sep_x = 30
        sep_y = 0.5
        font_label = Font(weight="bold", size=9)
        self.etiquetas_labels = []
        self.etiquetas_entries = []

        for i, etiqueta_texto in enumerate(etiquetas):
            etiqueta = tk.Label(
                self,
                text=etiqueta_texto,
                font=font_label,
                fg="white",
                bg=self.color_back,
            )
            etiqueta.place(x=70, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_labels.append(etiqueta)

            cuadro_texto = tk.Entry(
                self,
                textvariable=self.set_vars[i],
            )
            cuadro_texto.place(x=160, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_entries.append(cuadro_texto)

        self.btn_base = tk.Button(
            self,
            text="Conectar a base",
            bg=self.amarillo,
            command=lambda: self.conectar_con_base(ventana),
        )
        self.btn_base.place(x=58, y=310)

        self.crear_base_ = tk.Button(
            self,
            text="Crear base",
            bg=self.amarillo,
            command=lambda: self.crear_base(
                self.etiquetas_entries[0].get(),
                self.etiquetas_entries[1].get(),
                self.etiquetas_entries[2].get(),
                self.etiquetas_entries[3].get(),
                self.etiquetas_entries[4].get(),
            ),
        )
        self.crear_base_.place(x=200, y=310)

    def conectar_con_base(self, ventana):
        output = tk.Text(self, background=self.color_botones)
        output.config(borderwidth=2, relief="sunken")
        output.place(x=58, y=160, width=250, height=140)
        print("\n\n")
        try:
            indices = []

            datos_conexion = [
                self.etiquetas_entries[0].get(),
                self.etiquetas_entries[1].get(),
                self.etiquetas_entries[2].get(),
                self.etiquetas_entries[3].get(),
                self.etiquetas_entries[4].get(),
            ]

            conexion = mysql.connector.connect(
                host=datos_conexion[0],
                port=datos_conexion[1],
                user=datos_conexion[2],
                password=datos_conexion[3],
                database=datos_conexion[4],
            )

            # Crear un cursor para ejecutar consultas
            cursor = conexion.cursor()

            try:
                consulta = "SELECT max(id_hecho) FROM datos_hecho"
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                for fila in resultados:
                    if fila[0]:
                        indices.append(fila[0])
                    else:
                        indices.append(0)
            except Exception:
                self.mostrar_mensaje_advertencia(
                    "No se ha encontrado tabla 'datos_hecho'"
                )

            try:
                consulta = "SELECT max(id) FROM armas"
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                for fila in resultados:
                    if fila[0]:
                        indices.append(fila[0])
                    else:
                        indices.append(0)
            except Exception:
                self.mostrar_mensaje_advertencia("No se ha encontrado tabla 'armas'")

            try:
                consulta = "SELECT max(id) FROM automotores"
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                for fila in resultados:
                    if fila[0]:
                        indices.append(fila[0])
                    else:
                        indices.append(0)
            except Exception:
                self.mostrar_mensaje_advertencia(
                    f"No se ha encontrado tabla 'automotores'"
                )

            try:
                consulta = "SELECT max(id) FROM objetos"
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                for fila in resultados:
                    if fila[0]:
                        indices.append(fila[0])
                    else:
                        indices.append(0)
            except Exception:
                self.mostrar_mensaje_advertencia("No se ha encontrado tabla 'objetos'")

            try:
                consulta = "SELECT max(id) FROM secuestros"
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                for fila in resultados:
                    if fila[0]:
                        indices.append(fila[0])
                    else:
                        indices.append(0)
            except Exception:
                self.mostrar_mensaje_advertencia(
                    "No se ha encontrado tabla 'secuestros'"
                )

            try:
                consulta = "SELECT max(id) FROM involucrados"
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                for fila in resultados:
                    if fila[0]:
                        indices.append(fila[0])
                    else:
                        indices.append(0)
            except Exception:
                self.mostrar_mensaje_advertencia(
                    "No se ha encontrado tabla 'involucrados'"
                )

            try:
                consulta = "SELECT fecha_carga FROM datos_hecho WHERE id_hecho = (SELECT max(id_hecho) FROM datos_hecho)"
                cursor.execute(consulta)
                ultima_fecha = cursor.fetchone()
                ultima_fecha = ultima_fecha[0].strftime("%d %B %Y")
            except Exception as error:
                self.mostrar_mensaje_advertencia(
                    "No se ha podido recuperar la ultima fecha cargada: \n{error}'",
                )

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            self.btn_base.config(bg=self.verde)

            self.mostrar_mensaje_info(
                "Se ha logrado establecer conexión con la base de datos",
            )
            self.imprimir_con_color("Establecida conexión con base.", "verde")
            self.imprimir_con_color(f"Host: {datos_conexion[0]}", "blanco")
            self.imprimir_con_color(f"User: {datos_conexion[1]}", "blanco")
            self.imprimir_con_color(f"Nombre de la base: {datos_conexion[3]}", "blanco")
            self.imprimir_con_color(f"Ultima fecha en base: {ultima_fecha}", "blanco")

            ventana.botones[0].config(bg=self.verde)

            ventana.conexion = datos_conexion.copy()

            texto = f"Conexión satisfactoria!\n\nÚltima fecha: {ultima_fecha}\n\n"
            tags = (
                "Hechos: ",
                "Armas: ",
                "Automotores: ",
                "Objetos: ",
                "Secuestros: ",
                "Involucrados: ",
            )
            for i in range(0, len(indices)):
                texto += tags[i] + str(indices[i]) + "\n"

            output.insert(tk.END, texto)
            ventana.indices = indices

        except Exception as error:
            self.mostrar_mensaje_error(error)
            texto = "No se ha podido establecer conexión..."
            output.insert(tk.END, texto)

    def crear_base(self, host, port, user, passw, base):
        self.imprimir_con_color("Creando base de datos...", "blanco")
        self.imprimir_con_color(f"Host: {host}", "blanco")
        self.imprimir_con_color(f"Puerto: {port}", "blanco")
        self.imprimir_con_color(f"User: {user}", "blanco")
        self.imprimir_con_color(f"Nombre de la base: {base}", "blanco")
        conn = mysql.connector.connect(host=host, port=port, user=user, password=passw)
        cursor = conn.cursor()
        cursor.execute(f"SHOW DATABASES")
        databases = cursor.fetchall()
        if (base,) in databases:
            self.mostrar_mensaje_advertencia("La base de datos ya existe.")
        else:
            try:
                conn = mysql.connector.connect(
                    host=host, port=port, user=user, password=passw
                )
                conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {base}")
                conn.database = base
                cursor = conn.cursor()

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS datos_hecho (
                        id_hecho INT PRIMARY KEY,
                        nro_registro VARCHAR(30) NOT NULL,
                        fecha_carga DATE NOT NULL NOT NULL,
                        hora_carga TIME NOT NULL,
                        dependencia VARCHAR(100) NOT NULL,
                        fecha_inicio_hecho DATE,
                        hora_inicio_hecho TIME,
                        partido_hecho VARCHAR(50) NOT NULL,
                        localidad_hecho VARCHAR(50),
                        latitud VARCHAR(50),
                        calle VARCHAR(50),
                        longitud VARCHAR(50),
                        altura VARCHAR(10),
                        entre VARCHAR(50),
                        calificaciones VARCHAR(5000) NOT NULL,
                        relato VARCHAR(32767) NOT NULL
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_datos_hecho_partido_hecho ON datos_hecho(partido_hecho)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_datos_hecho_fecha_carga ON datos_hecho(fecha_carga)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_datos_hecho_localidad_hecho ON datos_hecho(localidad_hecho)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS automotores (
                        id INT PRIMARY KEY,
                        id_hecho INT NOT NULL,
                        marca VARCHAR(50) NOT NULL,
                        modelo VARCHAR(50),
                        color VARCHAR(50),
                        dominio VARCHAR(50),
                        nro_motor VARCHAR(50),
                        nro_chasis VARCHAR(50),
                        vinculo VARCHAR(50) NOT NULL,
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_automotores_marca ON automotores(marca)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_automotores_modelo ON automotores(modelo)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_automotores_dominio ON automotores(dominio)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_automotores_vinculo ON automotores(vinculo)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS armas (
                        id INT PRIMARY KEY,
                        id_hecho INT NOT NULL,
                        tipo_arma VARCHAR(100) NOT NULL,
                        marca VARCHAR(50) NOT NULL,
                        modelo VARCHAR(50),
                        nro_serie VARCHAR(50),
                        calibre VARCHAR(50),
                        observaciones VARCHAR(1000),
                        implicacion VARCHAR(50) NOT NULL,
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_armas_marca ON armas(marca)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS secuestros (
                        id INT PRIMARY KEY,
                        id_hecho INT NOT NULL,
                        tipo VARCHAR(50) NOT NULL,
                        marca VARCHAR(50),
                        modelo VARCHAR(50),
                        cantidad VARCHAR(50),
                        valor VARCHAR(50),
                        descripcion VARCHAR(1000),
                        implicacion VARCHAR(50) NOT NULL,
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_secuestros_implicacion ON secuestros(implicacion)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS objetos (
                        id INT PRIMARY KEY,
                        id_hecho INT NOT NULL,
                        tipo VARCHAR(50) NOT NULL,
                        marca VARCHAR(50),
                        modelo VARCHAR(50),
                        cantidad VARCHAR(50),
                        valor VARCHAR(50),
                        descripcion VARCHAR(1000),
                        implicacion VARCHAR(50) NOT NULL,
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_objetos_implicacion ON objetos(implicacion)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS involucrados (
                        id INT PRIMARY KEY,
                        id_hecho INT,
                        involucrado VARCHAR(30),
                        pais_origen VARCHAR(50),
                        tipo_dni VARCHAR(10),
                        nro_dni VARCHAR(20),
                        genero VARCHAR(20),
                        apellido VARCHAR(50),
                        nombre VARCHAR(50),
                        provincia_nacimiento VARCHAR(50),
                        ciudad_nacimiento VARCHAR(50),
                        fecha_nacimiento DATE,
                        observaciones VARCHAR(1000),
                        provincia_domicilio VARCHAR(50),
                        partido_domicilio VARCHAR(50),
                        localidad_domicilio VARCHAR(50),
                        calle_domicilio VARCHAR(50),
                        nro_domicilio VARCHAR(20),
                        entre VARCHAR(50),
                        piso VARCHAR(20),
                        departamento VARCHAR(20),
                        caracteristicas_fisicas VARCHAR(500),
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_involucrado ON involucrados(involucrado)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_nombre ON involucrados(nombre)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_apellido ON involucrados(apellido)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_pais_origen ON involucrados(pais_origen)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_partido_domicilio ON involucrados(partido_domicilio)"
                )

                conn.commit()
                conn.close()
                self.mostrar_mensaje_info("Base de datos creada.")
                self.imprimir_con_color(f"Base de datos creada", "verde")
            except Exception as error:
                self.mostrar_mensaje_error(f"No se ha podido crear la base: {error}")
                self.imprimir_con_color(
                    f"No se ha podido crear la base: {error}", "rojo"
                )
