import tkinter as tk
import model
import mysql.connector
import locale
import datetime
import os
import copy
import checkpoints as ck
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
from pathlib import Path as Ph

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


class Ventana_Base:
    color_botones = "#8CA2EA"
    botones_iniciales = "#AFEB54"
    botones_segmentado = "#EBA605"
    botones_subir = "#C34DEB"
    amarillo = "#EBDD04"
    rojo = "#EA3830"
    verde = "#27EA00"
    color_back = "#1D2B61"

    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y-100}"


class Ventana_Principal(Ventana_Base):
    def __init__(self, master):
        self.ventana = master
        self.ventana.title("Ariadna b-2.1.0")
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
                "callback": lambda: self.procesar_varios(),
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

    def procesar_inicial(self):
        #::::::::::::::::::::::::procesado inicial:::::::::::::::::::::::::::
        try:
            path = filedialog.askopenfilename()

            nombre_archivo = os.path.splitext(os.path.basename(path))[0]

            formateador = model.Formateador()
            archivo = model.Administrador._cargar(path)
            tester = model.Tester(archivo)
            if len(tester.errores) > 0:
                log_errores = model.Administrador._convertir_inicial(
                    tester.errores,
                    ["indice", "n° registro", "para enmendar"],
                    nombre=nombre_archivo,
                    error=True,
                )
                tk.messagebox.showinfo(
                    "Advertencia",
                    "Hubo errores en los listados.\nSe ha generado un registro errores.",
                )
                os.startfile(log_errores)
            else:
                archivo, identificadores = formateador._formatear(archivo, ck.cp_iden)
                inicial = model.Inicial(archivo, identificadores)
                path = model.Administrador._convertir_inicial(
                    inicial.sin_duplicados, ck.general, nombre=nombre_archivo
                )
                if tk.messagebox.askyesno(
                    "Segmentar", "¿Desea proceder a segmentar el archivo?"
                ):
                    self.procesar_final(path)
                else:
                    tk.messagebox.showinfo(
                        "Proceso completado",
                        "El archivo fue procesado correctamente.",
                    )
        except FileNotFoundError:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ningún archivo."
            )

        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def procesar_final(self, path=False):
        if not self.todos_unos(self.indices):
            self._cargar_no_segmentado(path, self.indices)
        else:
            tk.messagebox.showinfo(
                "Advertencia", f"Antes de segmentar, primero setee los indices."
            )
            self.abrir_ventana_top_intermedia(
                self.ventana_top, Ventana_indices, self.indices
            )
            indices = list(map(lambda var: var.get(), self.indices))
            self._cargar_no_segmentado(path, indices)

    def procesar_crudos(self, path=False):
        try:
            carpeta = filedialog.askdirectory()
            archivos = os.listdir(carpeta)
            formateador = model.Formateador()

            for archivo in archivos:
                path = os.path.join(
                    carpeta, archivo
                )  # Obtener la ruta completa del archivo
                if os.path.isfile(path):  # Comprobar si es un archivo (no una carpeta)
                    try:
                        nombre_archivo = os.path.splitext(os.path.basename(path))[0]
                        archivo0 = model.Administrador._cargar(path)
                        try:
                            tester = model.Tester(archivo0)
                            try:
                                if len(tester.errores) > 0:
                                    log_errores = (
                                        model.Administrador._convertir_inicial(
                                            tester.errores,
                                            ["indice", "n° registro", "para enmendar"],
                                            nombre=nombre_archivo,
                                            error=True,
                                        )
                                    )
                                else:
                                    archivo0, identificadores = formateador._formatear(
                                        archivo0, ck.cp_iden
                                    )
                                    inicial = model.Inicial(archivo0, identificadores)
                                    path = model.Administrador._convertir_inicial(
                                        inicial.sin_duplicados,
                                        ck.general,
                                        nombre=nombre_archivo,
                                    )
                            except Exception as error:
                                print(
                                    f"({archivo}) Error en etapa de procesado del archivo: {error}"
                                )
                        except Exception as error:
                            print(
                                f"({archivo}) Error en etapa de testeo de información entrante: {error}"
                            )
                    except Exception as error:
                        print(
                            f"({archivo}) Error en etapa de carga del archivo crudo: {error}"
                        )
                print(f"Listo {archivo}")
            tk.messagebox.showinfo(
                "Aviso",
                "El procesado de crudos ha sido completado.",
            )
        except FileNotFoundError:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ninguna carpeta."
            )

    def procesar_varios(self):
        if not self.todos_unos(self.indices):
            try:
                carpeta = filedialog.askdirectory()
                archivos = os.listdir(carpeta)

                indices = list(map(lambda var: var.get(), self.indices))
                for archivo in archivos:
                    path = os.path.join(
                        carpeta, archivo
                    )  # Obtener la ruta completa del archivo
                    if os.path.isfile(
                        path
                    ):  # Comprobar si es un archivo (no una carpeta)
                        try:
                            archivo1 = model.Administrador._cargar(
                                path, no_tiene_encabezados=False
                            )
                            try:
                                segmentado = model.Segmentado(
                                    archivo1, indices, carpeta=True
                                )
                                try:
                                    mensaje = model.Formateador.comprobar_salida(
                                        segmentado.final
                                    )
                                    if mensaje != "":
                                        tk.messagebox.showinfo("Advertencia", mensaje)
                                    try:
                                        model.Administrador._convertir_segmentado(
                                            segmentado.final, nombre=archivo
                                        )
                                        print(f"\nPreparando {archivo}")
                                        try:
                                            indices_finales = (
                                                model.Administrador._obtener_indices(
                                                    segmentado.final, indices
                                                )
                                            )
                                            print(f"Iniciales: {str(indices)}")
                                            print(f"Finales: {str(indices_finales)}")
                                            indices = list(
                                                map(lambda x: x + 1, indices_finales)
                                            )
                                            print(f"Siguientes: {str(indices)}")
                                        except Exception as error:
                                            print(
                                                f"({archivo}) Error en la obtención de índices nuevos: {error}"
                                            )
                                    except Exception as error:
                                        print(
                                            f"({archivo}) Error en conversión final a formato Excel: {error}"
                                        )
                                except Exception as error:
                                    print(
                                        f"({archivo}) Error en la comprobación de datos salientes: {error}"
                                    )
                            except Exception as error:
                                print(
                                    f"({archivo}) Error en etapa de procesado: {error}"
                                )
                        except Exception as error:
                            print(f"({archivo}) Error en etapa de carga: {error}")
                    print(f"Listo {archivo}")
                tk.messagebox.showinfo(
                    "Aviso",
                    "El procesado de no segmentados ha sido completado.",
                )
            except FileNotFoundError:
                tk.messagebox.showinfo(
                    "Advertencia", f"No se ha seleccionado ninguna carpeta."
                )
        else:
            tk.messagebox.showinfo(
                "Advertencia", f"Antes de segmentar, primero setee los indices."
            )
            self.abrir_ventana_top_intermedia(
                self.ventana_top, Ventana_indices, self.indices
            )
            indices = list(map(lambda var: var.get(), self.indices))
            try:
                carpeta = filedialog.askdirectory()
                archivos = os.listdir(carpeta)

                indices = list(map(lambda var: var.get(), self.indices))
                for archivo in archivos:
                    path = os.path.join(
                        carpeta, archivo
                    )  # Obtener la ruta completa del archivo
                    if os.path.isfile(
                        path
                    ):  # Comprobar si es un archivo (no una carpeta)
                        try:
                            archivo1 = model.Administrador._cargar(
                                path, no_tiene_encabezados=False
                            )
                            try:
                                segmentado = model.Segmentado(
                                    archivo1, indices, carpeta=True
                                )
                                try:
                                    mensaje = model.Formateador.comprobar_salida(
                                        segmentado.final
                                    )
                                    if mensaje != "":
                                        tk.messagebox.showinfo("Advertencia", mensaje)
                                    try:
                                        model.Administrador._convertir_segmentado(
                                            segmentado.final, nombre=archivo
                                        )
                                        print(f"\nPreparando {archivo}")
                                        try:
                                            indices_finales = (
                                                model.Administrador._obtener_indices(
                                                    segmentado.final, indices
                                                )
                                            )
                                            print(f"Iniciales: {str(indices)}")
                                            print(f"Finales: {str(indices_finales)}")
                                            indices = list(
                                                map(lambda x: x + 1, indices_finales)
                                            )
                                            print(f"Siguientes: {str(indices)}")
                                        except Exception as error:
                                            print(
                                                f"({archivo}) Error en la obtención de índices nuevos: {error}"
                                            )
                                    except Exception as error:
                                        print(
                                            f"({archivo}) Error en conversión final a formato Excel: {error}"
                                        )
                                except Exception as error:
                                    print(
                                        f"({archivo}) Error en la comprobación de datos salientes: {error}"
                                    )
                            except Exception as error:
                                print(
                                    f"({archivo}) Error en etapa de procesado: {error}"
                                )
                        except Exception as error:
                            print(f"({archivo}) Error en etapa de carga: {error}")
                    print(f"Listo {archivo}")
                tk.messagebox.showinfo(
                    "Aviso",
                    "El procesado de no segmentados ha sido completado.",
                )
            except FileNotFoundError:
                tk.messagebox.showinfo(
                    "Advertencia", f"No se ha seleccionado ninguna carpeta."
                )

    def compilar_archivos(self):
        carpeta = filedialog.askdirectory()
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
            print("Listo", archivo)

        # Escribir los datos consolidados en un archivo de Excel
        with pd.ExcelWriter(archivo_final) as writer:
            print("\nComenzando proceso de compilación...")
            for hoja, df in datos.items():
                df.to_excel(writer, sheet_name=hoja, index=False)

        print("Analizando coherencia de indexados...")
        try:
            if self.comprobar_indices(f"{carpeta}/consolidado.xlsx"):
                print("Chequeada coherencia de indexados sin errores")
            else:
                print("Se detectaron errores de coherencia en los indexados")
        except Exception as error:
            print(error)
        print("Se ha creado el archivo consolidado en:", archivo_final)

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
                mes.append(fecha_.strftime("%B"))
            mes_final = list(set(mes))
            if 29 < len(fechas) < 32 or len(fechas) == 21:
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
                if mes_final[0] == "febrero":
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
                return False, f"(MES) Error en coherencia: {fechas}"

    def comprobar_nulos(self, archivo, advertencias=True):
        res2 = model.Formateador.comprobar_salida(archivo, advertencias=advertencias)
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

    def iniciar(self):
        self.ventana.mainloop()

    def _cargar_no_segmentado(self, path, indices):
        try:
            if path is False:
                archivo1 = model.Administrador._cargar(
                    filedialog.askopenfilename(), no_tiene_encabezados=False
                )
                segmentado = model.Segmentado(archivo1, indices)
            else:
                archivo1 = model.Administrador._cargar(path, no_tiene_encabezados=False)
                segmentado = model.Segmentado(archivo1, indices)
            try:
                try:
                    mensaje = model.Formateador.comprobar_salida(segmentado.final)
                    if mensaje != "":
                        tk.messagebox.showinfo("Advertencia", mensaje)
                except Exception as error:
                    print(error)
                model.Administrador._convertir_segmentado(segmentado.final)
                tk.messagebox.showinfo(
                    "Advertencia", f"El proceso se completo correctamente :)"
                )
            except AttributeError:
                tk.messagebox.showinfo(
                    "Advertencia", f"El proceso de segmentado se ha abortado."
                )
                ventana_errores = Ventana_addendum(
                    self.ventana, archivo=segmentado.errores
                )
        except FileNotFoundError:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ningún archivo."
            )

    def chequear_integridad(self, ventana):
        path = filedialog.askopenfilename()
        respuesta = messagebox.askyesno(
            "Selecciona tipo de archivo",
            "¿El archivo seleccionado corresponde a una fecha individual? En caso de que sea un mes, ELEGIR NO",
        )
        # COMPROBAR FECHAS
        if respuesta:
            # COMPROBAR INDICES DE FECHA
            try:
                if self.comprobar_indices(path):
                    # tk.messagebox.showinfo("Comprobados", f"Indices correctos.")
                    # COMPROBAR COHERENCIA DE FECHA
                    try:
                        res = self.comprobar_fechas(path)
                        if res[0]:
                            # tk.messagebox.showinfo("Comprobados", f"{res[1]}")
                            # COMPROBAR INTEGRIDAD DE TABLAS Y CAMPOS NO NULOS
                            try:
                                archivo_final = model.Administrador._cargar_final(path)
                                res2 = self.comprobar_nulos(
                                    archivo_final, advertencias=False
                                )
                                if res2 == "":
                                    tk.messagebox.showinfo(
                                        "Archivo comprobado",
                                        f"Comprobados índices, tablas, y campos no nulos. Integridad de archivo CORRECTA",
                                    )
                                    ventana.botones[1].config(bg=self.verde)
                                    ventana.a_subir = archivo_final
                                else:
                                    tk.messagebox.showwarning("Advertencia", f"{res2}")
                                    ventana.botones[1].config(bg=self.amarillo)
                            except Exception as error:
                                tk.messagebox.showerror(
                                    "Error", f"Error al comprobar nulos: {error}"
                                )
                                ventana.botones[1].config(bg=self.rojo)
                        else:
                            tk.messagebox.showwarning("Advertencia", f"{res[1]}")
                            ventana.botones[1].config(bg=self.amarillo)
                    except Exception as error:
                        tk.messagebox.showerror(
                            "Error", f"Error al comprobar fechas: {error}"
                        )
                        ventana.botones[1].config(bg=self.rojo)
                else:
                    tk.messagebox.showwarning("Advertencia", f"Indices no correctos.")
                    ventana.botones[1].config(bg=self.amarillo)
            except Exception as error:
                tk.messagebox.showerror("Error", f"Error al comprobar índices: {error}")
                ventana.botones[1].config(bg=self.rojo)

        # COMPROBAR MES
        else:
            # COMPROBAR INDICES DE MES
            try:
                if self.comprobar_indices(path):
                    # tk.messagebox.showinfo("Comprobados", f"Indices correctos.")
                    # COMPROBAR COHERENCIA DE MES
                    try:
                        res = self.comprobar_fechas(path, fecha=False)
                        if res[0]:
                            # tk.messagebox.showinfo("Comprobados", f"{res[1]}")
                            # COMPROBAR INTEGRIDAD DE TABLAS Y CAMPOS NO NULOS
                            try:
                                archivo_final = model.Administrador._cargar_final(path)
                                res2 = self.comprobar_nulos(
                                    archivo_final, advertencias=False
                                )
                                if res2 == "":
                                    tk.messagebox.showinfo(
                                        "Archivo comprobado",
                                        f"Comprobados índices, tablas, y campos no nulos. Integridad de archivo CORRECTA",
                                    )
                                    ventana.botones[1].config(bg=self.verde)
                                    ventana.a_subir = archivo_final
                                else:
                                    tk.messagebox.showwarning("Advertencia", f"{res2}")
                                    ventana.botones[1].config(bg=self.amarillo)
                            except Exception as error:
                                tk.messagebox.showerror(
                                    "Error", f"Error al comprobar nulos: {error}"
                                )
                                ventana.botones[1].config(bg=self.rojo)
                        else:
                            tk.messagebox.showwarning("Advertencia", f"{res[1]}")
                            ventana.botones[1].config(bg=self.amarillo)
                    except Exception as error:
                        tk.messagebox.showerror(
                            "Error", f"Error al comprobar fechas: {error}"
                        )
                        ventana.botones[1].config(bg=self.rojo)
                else:
                    tk.messagebox.showwarning("Advertencia", f"Indices no correctos.")
                    ventana.botones[1].config(bg=self.amarillo)
            except Exception as error:
                tk.messagebox.showerror("Error", f"Error al comprobar índices: {error}")
                ventana.botones[1].config(bg=self.rojo)

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
                cursor.executemany(consulta, data2)
                """tk.messagebox.showinfo(
                    "Todo OK", f"Archivo '{nombre_tabla}' a la espera de inserción..."
                )"""
            except Exception as error:
                tk.messagebox.showerror(
                    f"Error durante la inserción en {nombre_tabla}", f"{error}"
                )
                raise error

        conexion = mysql.connector.connect(
            host=ventana.conexion[0],
            user=ventana.conexion[1],
            password=ventana.conexion[2],
            database=ventana.conexion[3],
        )

        cursor = conexion.cursor()

        indices_archivo = obtener_indices_archivo(ventana.a_subir)
        if chequear_continuidad(ventana.indices, indices_archivo):
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
                    tk.messagebox.showwarning(
                        f"No se ha insertado la tabla 'datos_hecho' ya que no contenía registros."
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
                    tk.messagebox.showwarning(
                        f"No se ha insertado la tabla 'armas' ya que no contenía registros."
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
                    tk.messagebox.showwarning(
                        f"No se ha insertado la tabla 'automotores' ya que no contenía registros."
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
                    tk.messagebox.showwarning(
                        f"No se ha insertado la tabla 'objetos' ya que no contenía registros."
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
                    tk.messagebox.showwarning(
                        f"No se ha insertado la tabla 'secuestros' ya que no contenía registros."
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
                    tk.messagebox.showwarning(
                        f"Advertencia",
                        f"No se ha insertado la tabla 'involucrados' ya que no contenía registros.",
                    )
                conexion.commit()
                tk.messagebox.showinfo(
                    f"Éxito",
                    f"Archivo insertado correctamente.",
                )
                ventana.destroy()
            except Exception as error:
                tk.messagebox.showwarning(
                    f"Advertencia",
                    f"Una de las tablas tuvo problemas de inserción. Se aborta subida a base. \n\n Error: {error}",
                )
        else:
            tk.messagebox.showwarning(
                f"Advertencia",
                f"Los índices del archivo que se intenta subir no son continuos al indexado de la base. Se aborta proceso de inserción ya que generaría problemas de coherencia de índices primarios.",
            )
        conexion.close()

    @staticmethod
    def todos_unos(lista):
        for elemento in lista:
            if elemento.get() != 1:
                return False
        return True


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
                rf"{Ph(__file__).resolve().parent}\Base calificaciones\calificaciones_db.xlsx",
                header=None,
            ).values.tolist()
        )
        addendum = model.Addendum()
        simplificado = addendum.simplificada(original)

        # Agregar un nuevo registro
        df[simplificado] = entry.get()

        # convierto el dic en df
        df = list(df.items())
        df = pd.DataFrame(df)

        # Guardar los cambios en el archivo Excel
        df.to_excel(
            rf"{Ph(__file__).resolve().parent}\Base calificaciones\calificaciones_db.xlsx",
            index=False,
            header=False,
        )
        tk.messagebox.showinfo(
            "Alta",
            f"Se ha agregado la nueva carátula a la base de datos de calificaciones.",
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
            original = model.Administrador._cargar(
                self.path_original,
            )
            enmendado = model.Administrador._cargar(
                self.path_enmendado, no_tiene_encabezados=False, es_original=False
            )

            for error in enmendado:
                original[int(error[0])][0] = error[2]

            nombre_archivo = os.path.splitext(os.path.basename(self.path_original))[0]
            ult = pd.DataFrame(original)
            ult.to_excel(
                rf"{Ph(__file__).resolve().parent}\Exportaciones\Corregidos\{nombre_archivo}.xlsx",
                index=False,
                header=False,
            )
            self.boton_corregir.config(bg="#27EA00")
            tk.messagebox.showinfo(
                "Corregido", f"¡El archivo fue corredido correctamente!"
            )
            return rf"{Ph(__file__).resolve().parent}\Exportaciones\Corregidos\{nombre_archivo}.xlsx"
        except Exception as error:
            tk.messagebox.showinfo(
                "Advertencia", f"Ha ocurrido el siguiente error:\n {error}"
            )

    def cargar_original(self):
        path = filedialog.askopenfilename()
        if path:
            self.path_original = path
            self.boton_original.config(bg=self.verde)
        else:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ningún archivo."
            )

    def cargar_enmendado(self):
        path = filedialog.askopenfilename()
        if path:
            self.path_enmendado = path
            self.boton_enmendado.config(bg="#27EA00")
        else:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ningún archivo."
            )


class Ventana_indices(tk.Toplevel, Ventana_Base):
    def __init__(self, ventana, indices):
        super().__init__(ventana)
        self.title("Etiquetas y Cuadros de Texto")
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
        tk.messagebox.showinfo(
            "Indices configurados", f"Los índices fueron configurados correctamente"
        )
        self.destroy()

    def conectar_con_base(self):
        try:
            indices = []

            conexion = mysql.connector.connect(
                host="localhost", user="root", password="", database="delitos"
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
            tk.messagebox.showinfo("!!", error)

    def conectar_con_archivo(self):
        ruta_archivo = filedialog.askopenfilename()
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
            tk.messagebox.showinfo("!!", f"No se ha seleccionado ningún archivo")


class Ventana_conectar(tk.Toplevel, Ventana_Base):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.title("Conectar con base")
        self.ancho = 360
        self.alto = 360
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.configure(bg=self.color_back)

        self.host = tk.StringVar()
        self.user = tk.StringVar()
        self.passw = tk.StringVar()
        self.base = tk.StringVar()

        self.host.set("localhost")
        self.user.set("root")
        self.passw.set("")
        self.base.set("delitos")

        self.set_vars = [self.host, self.user, self.passw, self.base]

        self.indices = []

        self.crear_widgets(ventana)

    def crear_widgets(self, ventana):
        etiquetas = [
            "HOST: ",
            "USER: ",
            "PASS: ",
            "DATABASE: ",
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
            ),
        )
        self.crear_base_.place(x=200, y=310)

    def conectar_con_base(self, ventana):

        output = tk.Text(self, background=self.color_botones)
        output.config(borderwidth=2, relief="sunken")
        output.place(x=58, y=135, width=250, height=165)

        try:

            indices = []

            datos_conexion = [
                self.etiquetas_entries[0].get(),
                self.etiquetas_entries[1].get(),
                self.etiquetas_entries[2].get(),
                self.etiquetas_entries[3].get(),
            ]

            conexion = mysql.connector.connect(
                host=datos_conexion[0],
                user=datos_conexion[1],
                password=datos_conexion[2],
                database=datos_conexion[3],
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
                tk.messagebox.showwarning(
                    "Advertencia", f"No se ha encontrado tabla 'datos_hecho'"
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
                tk.messagebox.showwarning(
                    "Advertencia", f"No se ha encontrado tabla 'armas'"
                )

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
                tk.messagebox.showwarning(
                    "Advertencia", f"No se ha encontrado tabla 'automotores'"
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
                tk.messagebox.showwarning(
                    "Advertencia", f"No se ha encontrado tabla 'objetos'"
                )

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
                tk.messagebox.showwarning(
                    "Advertencia", f"No se ha encontrado tabla 'secuestros'"
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
                tk.messagebox.showwarning(
                    "Advertencia", f"No se ha encontrado tabla 'involucrados'"
                )

            try:
                consulta = "SELECT fecha_carga FROM datos_hecho WHERE id_hecho = (SELECT max(id_hecho) FROM datos_hecho)"
                cursor.execute(consulta)
                ultima_fecha = cursor.fetchone()
                ultima_fecha = ultima_fecha[0].strftime("%d %B %Y")
            except Exception as error:
                tk.messagebox.showwarning(
                    "Advertencia",
                    f"No se ha podido recuperar la ultima fecha cargada: \n{error}'",
                )

            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

            self.btn_base.config(bg=self.verde)

            tk.messagebox.showinfo(
                "Conexión satisfactoria",
                "Se ha logrado establecer conexión con la base de datos",
            )

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
            tk.messagebox.showinfo("-.-", error)
            texto = "No se ha podido establecer conexión..."
            output.insert(tk.END, texto)

    def crear_base(self, host, user, passw):
        conn = mysql.connector.connect(host=host, user=user, password=passw)
        conn.cursor().execute("CREATE DATABASE IF NOT EXISTS Delitos")
        conn.database = "Delitos"
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
                observaciones VARCHAR(200),
                implicacion VARCHAR(50) NOT NULL,
                FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
            )
        """
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_armas_marca ON armas(marca)")

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
                descripcion VARCHAR(200),
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
                descripcion VARCHAR(200),
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
                observaciones VARCHAR(500),
                provincia_domicilio VARCHAR(50),
                partido_domicilio VARCHAR(50),
                localidad_domicilio VARCHAR(50),
                calle_domicilio VARCHAR(50),
                nro_domicilio VARCHAR(20),
                entre VARCHAR(50),
                piso VARCHAR(20),
                departamento VARCHAR(20),
                caracteristicas_fisicas VARCHAR(100),
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
