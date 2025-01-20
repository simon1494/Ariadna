import sys

sys.path.append("../ariadna")
import locale
import mysql.connector
import locale
import datetime
import os
import pandas as pd
import tkinter as tk
import settings as ck
from tkinter import messagebox
from tkinter import simpledialog
from .ventana_base import VentanaBase
from .ventana_calificaciones import VentanaCalificaciones
from .ventana_conexion import VentanaConexion
from .ventana_errores import VentanaErrores
from .ventana_indices import VentanaIndices
from .ventana_intermedia import VentanaIntermedia
from modelos.gestores_de_archivos.separador import Separador
from modelos.gestores_de_archivos.formateador import Formateador
from modelos.gestores_de_archivos.testeador import Tester
from modelos.procesadores.procesador_inicial import Inicial
from modelos.procesadores.procesador_segmentado import Segmentado
import calendar

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


def mes_actual_formato():
    # Obtener el mes y el número en curso
    fecha_actual = datetime.datetime.now()
    mes_numero = fecha_actual.month
    nombre_mes = calendar.month_name[mes_numero].capitalize()

    # Devolver en formato "mm Mes"
    return f"{mes_numero:02d} {nombre_mes}"


def ocultar_y_mostrar(func):
    def wrapper(self, *args, **kwargs):
        self.ventana_top.withdraw()  # Oculta la ventana
        try:
            result = func(self, *args, **kwargs)  # Ejecuta el método
            self.ventana_top.deiconify()  # Muestra la ventana nuevamente
        except Exception as error:
            self.imprimir_con_color(
                f"Error: {error}",
                "rojo",
            )
        finally:
            try:
                self.ventana_top.deiconify()
            except Exception:
                pass
        return result

    return wrapper


class VentanaPrincipal(VentanaBase):
    def __init__(self, master, version, usuario):
        self.crear_directorio_de_exportaciones()
        self.crear_base_caratulas()
        self.insertar_caratulas_preexistentes()
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
                    self.ventana_top, VentanaErrores
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
                    self.ventana_top, VentanaIndices, indices=self.indices
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
                    self.ventana_top, VentanaConexion
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
            {
                "nombre": "reconstruir",
                "texto": "Reconstruir base",
                "callback": lambda: self.reconstruir(self.ventana_top),
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
            path = self.seleccionar_archivo(
                f"/Exportaciones/Crudos/2025/{mes_actual_formato()}"
            )

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
                self.ventana_top, VentanaIndices, self.indices
            )
            indices = list(map(lambda var: var.get(), self.indices))
            self.ventana_top.withdraw()
            self._cargar_no_segmentado(path, indices)

    def _cargar_no_segmentado(self, path, indices):
        try:
            if path is False:
                path_archivo = self.seleccionar_archivo(
                    f"/Exportaciones/No segmentados/2025/{mes_actual_formato()}"
                )
                archivo1 = self._cargar(
                    path_archivo, no_tiene_encabezados=False, es_original=False
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
                        for i, ind in enumerate(self.indices):
                            ind.set(indices_finales[i] + 1)

                        self.imprimir_con_color(
                            f"Siguientes:--{str([valor.get() for valor in self.indices])}",
                            "blanco",
                        )
                    except Exception as error:
                        self.imprimir_con_color(
                            f"Error en la obtención de índices nuevos: {error}",
                            "rojo",
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
                    ventanaErrores = VentanaCalificaciones(
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
                        for i, ind in enumerate(self.indices):
                            ind.set(indices_finales[i] + 1)

                        self.imprimir_con_color(
                            f"Siguientes:--{str([valor.get() for valor in self.indices])}",
                            "blanco",
                        )
                    except Exception as error:
                        self.imprimir_con_color(
                            f"Error en la obtención de índices nuevos: {error}",
                            "rojo",
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
                    ventanaErrores = VentanaCalificaciones(
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
                    self.ventana_top, VentanaIndices, self.indices
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
                        segmentado = Segmentado(archivo1, indices)
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
                            ventanaErrores = VentanaCalificaciones(
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
            archivo_final = f"{carpeta}/{os.path.basename(carpeta)}.xlsx"

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
                if self.comprobar_indices(archivo_final):
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
        respuesta = self.mostrar_mensaje_pregunta(
            "Desea procesar un archivo o una carpeta? Para archivo, presione SI. De lo controario, NO."
        )
        try:
            separador = Separador()
            if respuesta:
                separador.procesar_uno()
            else:
                separador.procesar_archivos()
                self.mostrar_mensaje_info(
                    "La carpeta ha sido mapeada y sus archivos separados con éxito."
                )
        except WindowsError:
            self.imprimir_con_color("Nada seleccionado.", "blanco")
            self.mostrar_mensaje_advertencia("Nada seleccionado.")
        """except Exception as error:
            self.imprimir_con_color(f"Error inesperado: {error}", "rojo")
            self.mostrar_mensaje_error(f"Error inesperado: {error}")
            raise error"""

    def _archivos(self):
        carpeta = self.seleccionar_archivo("/Exportaciones/Segmentados/2025/")
        print("\n")
        archivos = os.listdir(carpeta)

        # Nombre del archivo final
        archivo_final = f"{carpeta}/{os.path.basename(carpeta)}.xlsx"

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
            if self.comprobar_indices(archivo_final):
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
                if (
                    tuplas_hojas.index(tupla) != 1
                ):  # No analiza los índices de calificaciones ya que es una tabla obsoleta en el nuevo DB Scheme y puede contener errores de indexado.
                    if not tupla:  # Si la lista está vacía, no se considera consecutiva
                        break

                    n = tupla[0]  # Primer elemento de la lista
                    for num in tupla:
                        if num != n:  # Si el número no es igual a n, no es consecutivo
                            self.imprimir_con_color(
                                f"--- Discontinuidad de índices detectada en Hoja {tuplas_hojas.index(tupla)} ---",
                                "amarillo",
                            )
                            self.imprimir_con_color(
                                f"Índice de rotura: {num}", "amarillo"
                            )
                            self.imprimir_con_color(
                                f"Inicio de índices: {tupla[0]}", "amarillo"
                            )
                            self.imprimir_con_color(f"Índice esperado: {n}", "amarillo")
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
        self.ventana_top = VentanaIntermedia(
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
    def chequear_integridad(self, ventana, reconstruir=False, archivo=None):
        print("\n\n")
        if not reconstruir:
            path = self.seleccionar_archivo("/Exportaciones/Segmentados/2025/")
        else:
            path = archivo
        if path:
            if not archivo:
                respuesta = self.mostrar_mensaje_pregunta(
                    "¿El archivo seleccionado corresponde a una fecha individual? En caso de que sea un mes, ELEGIR NO",
                )
            else:
                respuesta = False
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
                                        if not reconstruir:
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
    def subir_a_base(self, ventana, reconstruir=False):
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
                    print("-------------------------------------------")
                    print(f"Índices en base: {indices_base[i]}")
                    print(f"Índices en archivo: {indices_archivo[i]}")
                    print("-------------------------------------------")
                    return False
                return True

        def chequear_continuidad_fechas(cursor, data, reconstruir=False):
            def es_dia_anterior(fecha1_str, fecha2_str):
                # Convertir las cadenas de fecha a objetos datetime.date
                fecha1 = datetime.datetime.strptime(fecha1_str, "%Y-%m-%d").date()
                fecha2 = datetime.datetime.strptime(fecha2_str, "%Y-%m-%d").date()
                print(fecha1, fecha2)
                # Obtener la diferencia entre las fechas
                diferencia = fecha2 - fecha1

                # Verificar si la diferencia es de un día
                return diferencia == datetime.timedelta(days=1)

            if reconstruir:
                return True
            try:
                # Ejecutar la consulta SQL
                cursor.execute(
                    "SELECT fecha_carga FROM datos_hecho WHERE id_hecho = (SELECT MAX(id_hecho) FROM datos_hecho)"
                )
                # Obtener el resultado de la consulta
                resultado = cursor.fetchone()
                # Si hay resultado, formatear la fecha
                if resultado:
                    fecha = resultado[0]
                    fecha_formateada = fecha.strftime("%Y-%m-%d")
                    if es_dia_anterior(fecha_formateada, data[-1][3]):
                        self.imprimir_con_color(
                            f"La fecha {data[-1][3]} del archivo a insertar es contigua a la última fecha en base.",
                            "verde",
                        )
                        return es_dia_anterior(fecha_formateada, data[-1][3])
                    else:
                        bypass = simpledialog.askstring(
                            "ADVERTENCIA",
                            "Las fechas no son contiguas, pero puede evitar esta validacion si asi lo desea.\nIngrese el codigo para saltar la validacion e insertar el archivo directo en base: ",
                        )
                        if bypass == "1494":
                            return True
                    return False
                else:
                    # No hay resultado, mostrar cuadro de diálogo
                    root = tk.Tk()
                    root.withdraw()  # Ocultar la ventana principal de Tkinter
                    respuesta = tk.messagebox.askyesno(
                        "Sin fechas en la base",
                        "La base parece no tener fechas aun. Seleccione SI en caso de que el archivo a insertar sea el primero; seleccione NO para abortar el proceso.",
                    )
                    return respuesta
            except Exception as error:
                self.mostrar_mensaje_error(
                    f"Error en el chequeo de contiguidad de fechas. Error: {error}"
                )
                return False

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
                    f"Error durante la inserción en {nombre_tabla}.Error: {error}"
                )
                raise error

        if ventana.conexion[4] != "op_sol":
            try:
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
                self.imprimir_con_color(
                    "Chequeando continuidad de indexados...", "lila"
                )
                if chequear_continuidad_fechas(cursor, ventana.a_subir[0], reconstruir):
                    if chequear_continuidad(ventana.indices, indices_archivo):
                        self.imprimir_con_color(
                            "CHEQUEO: continuidad de índices correcta.", "verde"
                        )
                        print("\n")
                        self.imprimir_con_color(
                            "Iniciando inserción de datos en base...", "lila"
                        )
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
                            if not reconstruir:
                                self.mostrar_mensaje_info(
                                    "Archivo insertado correctamente.",
                                )
                            self.imprimir_con_color(
                                "Archivo insertado correctamente.", "verde"
                            )
                            conexion.commit()
                            self.consultar_indices_a_base(
                                ventana.conexion[0],
                                ventana.conexion[1],
                                ventana.conexion[2],
                                ventana.conexion[3],
                                ventana.conexion[4],
                                ventana,
                            )
                            print()
                            self.imprimir_con_color("Nuevos indices: ", "verde")
                            self.imprimir_con_color(f"{ventana.indices[0]}", "verde")
                            self.imprimir_con_color(f"{ventana.indices[1]}", "verde")
                            self.imprimir_con_color(f"{ventana.indices[2]}", "verde")
                            self.imprimir_con_color(f"{ventana.indices[3]}", "verde")
                            self.imprimir_con_color(f"{ventana.indices[4]}", "verde")

                            ventana.botones[1].config(bg=self.botones_subir)
                            ventana.botones[2].config(bg=self.botones_subir)
                            ventana.a_subir = None
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
                else:
                    self.mostrar_mensaje_advertencia(
                        "Las fechas del archivo que se intenta subir no son continuas las de la base. Se aborta proceso de inserción ya que generaría vacíos en la información.",
                    )
                    self.imprimir_con_color(
                        "Las fechas del archivo que se intenta subir no son continuas las de la base. Se aborta proceso de inserción ya que generaría vacíos en la información.",
                        "amarillo",
                    )
                conexion.close()
            except AttributeError:
                self.mostrar_mensaje_advertencia(
                    "Ningun archivo seleccionado para insertar en base."
                )
        else:
            try:
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
                self.imprimir_con_color(
                    "Chequeando continuidad de indexados...", "lila"
                )
                indices_archivo = obtener_indices_archivo(ventana.a_subir)
                if chequear_continuidad(
                    ventana.indices, indices_archivo
                ) and chequear_continuidad_fechas(
                    cursor, ventana.a_subir[0], reconstruir
                ):
                    self.imprimir_con_color(
                        "CHEQUEO: continuidad de índices correcta.", "verde"
                    )
                    print("\n")
                    self.imprimir_con_color(
                        "Iniciando inserción de datos en base...", "lila"
                    )
                    try:
                        if indices_archivo[0]:
                            insertar(
                                cursor,
                                "datos_hecho",
                                ventana.a_subir[0],
                                ck.oper_sol_recortes["datos_hecho"],
                                ck.oper_sol["datos_hecho"],
                            )
                        else:
                            self.mostrar_mensaje_advertencia(
                                "No se ha insertado la tabla 'datos_hecho' ya que no contenía registros."
                            )
                        conexion.commit()
                        ventana.botones[1].config(bg=self.botones_subir)
                        ventana.botones[2].config(bg=self.botones_subir)
                        ventana.a_subir = None
                        self.imprimir_con_color(
                            "Archivo insertado correctamente.", "verde"
                        )
                    except Exception as error:
                        self.mostrar_mensaje_advertencia(
                            f"Una de las tablas tuvo problemas de inserción. Se aborta subida a base. \n\n Error: {error}",
                        )
            except AttributeError:
                self.mostrar_mensaje_advertencia(
                    "Ningun archivo seleccionado para insertar en base."
                )

    def consultar_indices_a_base(self, host, port, user, password, database, ventana):
        try:
            indices = []
            conexion = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
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
            ventana.indices = indices
        except Exception as error:
            self.mostrar_mensaje_error(error)

    @staticmethod
    def todos_unos(lista):
        for elemento in lista:
            if elemento.get() != 1:
                return False
        return True

    def reconstruir(self, ventana):
        carpeta = self.seleccionar_carpeta("Exportaciones/Segmentados")
        archivos = os.listdir(carpeta)
        for archivo in archivos:
            try:
                path = os.path.join(
                    carpeta, archivo
                )  # Obtener la ruta completa del archivo
                if os.path.isfile(path):  # Comprobar si es un archivo (no una carpeta)
                    print(path)
                    self.chequear_integridad(ventana, reconstruir=True, archivo=path)
                    self.subir_a_base(ventana, reconstruir=True)
            except Exception as error:
                self.imprimir_con_color(
                    f"Error en archivo de reconstrucción:\2 {error}"
                )
        self.imprimir_con_color(
            "-----------------------------\nReconstrucción finalizada sin fallos.\n-----------------------------",
            "verde",
        )

    def iniciar(self):
        self.ventana.mainloop()
