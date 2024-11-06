import sys

sys.path.append("../ariadna")
import os
import pandas as pd
import re
from tkinter.filedialog import askopenfilename
from datetime import datetime
from modelos.gestores_de_informacion.logueador import Logueador
from modelos.gestores_de_informacion.mensajeador import Mensajeador
import locale

locale.setlocale(locale.LC_TIME, "es_ES.utf8")


class Separador(Logueador, Mensajeador):
    def __init__(self) -> None:
        self.imprimir_con_color("--- MÓDULO MAPEADOR INICIALIZADO ---", "azul")
        print("")

    def find_paso_columns(self, df):
        paso_columns = []
        first_row = df.iloc[0]
        column_names = [i for i in range(len(first_row))]

        for i, column_value in enumerate(first_row):
            if str(column_value).lower().startswith("paso"):
                paso_columns.append(column_names[i])

        return paso_columns

    def extract_dates_between_strings(self, text, start_string, end_string):
        dates = []
        pattern = re.compile(f"{start_string}(.*?){end_string}")
        matches = pattern.findall(text)
        for match in matches:
            dates.append(match.strip())
        return dates

    def get_paso_dates(self, df, paso_columns):
        paso_dates = []

        for column in paso_columns:
            for cell in df[column]:
                if isinstance(cell, str):
                    extracted_dates = self.extract_dates_between_strings(
                        cell, "Fecha: ", " Hora:"
                    )
                    paso_dates.extend(extracted_dates)

        return paso_dates

    def obtener_lineas_de_errores(self, df, paso_columns):
        errores = []

        for column in paso_columns:
            for idx, cell in df[column].items():  # Usa idx para obtener el índice
                if isinstance(cell, str):
                    extracted_dates = self.extract_dates_between_strings(
                        cell, "Fecha: ", " Hora:"
                    )
                    try:
                        # Intentamos convertir cada fecha y verificamos errores
                        index_errores = [
                            self.convertir_fecha(fecha) for fecha in extracted_dates
                        ]
                    except Exception:
                        errores.append(
                            idx + 1
                        )  # Agregamos el índice de la fila con error
        return errores

    def generar_str_error_con_lineas(self, lista_errores):
        retorno = "\nLineas con errores"
        for error in lista_errores:
            retorno += f"\n--> {error}"
        return retorno

    def get_paso_data(self, df, paso_columns):
        paso_data = df[paso_columns]
        return paso_data

    def convertir_fecha(self, fecha):
        fecha_str = fecha
        fecha_obj = datetime.strptime(fecha_str, "%d %B %Y")
        numero_mes = fecha_obj.strftime("%m")
        dia_mes = fecha_obj.strftime("%d")
        formato_deseado = f"{numero_mes}-{dia_mes}"
        return formato_deseado

    def medir_largo_estructura(self, estructura) -> int:
        return len(estructura)

    def filtrar_y_guardar_campo(self, df, fecha, destino):
        search_string = f"Fecha: {fecha} Hora: "
        filtered_df = df[
            df[df.columns[0]].str.contains(
                f"{search_string}|CHEQUEAR DESDE EL SISEP", regex=True, case=True
            )
        ]
        nombre = self.convertir_fecha(fecha)
        if not os.path.isfile(rf"{destino}\{nombre}.xlsx"):
            filtered_df.to_excel(rf"{destino}\{nombre}.xlsx", header=False, index=False)
            self.imprimir_con_color(
                f"Listo {fecha}. {len(filtered_df)} registros.", color="verde"
            )
        return self.medir_largo_estructura(filtered_df)

    def procesar_uno(self):
        directorio = self.obtener_directorio_github("Delfos\exportaciones")
        ruta_archivo = askopenfilename(initialdir=directorio)
        destino = self.distribuir_archivos("cr", os.path.basename(ruta_archivo))
        # destino = self.seleccionar_carpeta("/Exportaciones/Crudos/")
        nombre_archivo = ruta_archivo
        if os.path.isfile(nombre_archivo):
            try:
                df = pd.read_excel(nombre_archivo, header=None)
                largo_df = self.medir_largo_estructura(df)
                paso_columns = self.find_paso_columns(df)
                paso_data = self.get_paso_data(df, paso_columns)
                paso_dates = self.get_paso_dates(df, paso_columns)
                paso_dates = set(paso_dates)
                print("")
                self.imprimir_con_color(
                    f"Fechas en el archivo {nombre_archivo.replace('.xlsx','')}:",
                    color="blanco",
                )
                for fecha in paso_dates:
                    self.imprimir_con_color(f"{fecha}", color="blanco")
                self.imprimir_con_color(f"Total registros: {largo_df}", color="blanco")
                suma_subs = 0
                try:
                    for fecha in paso_dates:
                        largo_sub = self.filtrar_y_guardar_campo(
                            paso_data, fecha, destino
                        )
                        suma_subs += largo_sub
                except Exception:
                    listado_errores = self.obtener_lineas_de_errores(df, paso_columns)
                    raise ValueError(
                        f"{self.generar_str_error_con_lineas(listado_errores)}"
                    )
                if suma_subs == largo_df:
                    self.imprimir_con_color(
                        f"La suma de sub-listados [{suma_subs}] coincide con el total [{largo_df}]",
                        "verde",
                    )
                else:
                    if (largo_df - suma_subs) <= 4:
                        self.imprimir_con_color(
                            f"La suma de sub-listados [{suma_subs}] NO coincide con el total [{largo_df}] en {(largo_df - suma_subs)} registros.",
                            "amarillo",
                        )
                    elif (largo_df - suma_subs) > 4:
                        self.imprimir_con_color(
                            f"La suma de sub-listados [{suma_subs}] NO coincide con el total [{largo_df}] en {(largo_df - suma_subs)} registros.",
                            "rojo",
                        )
            except Exception as error:
                self.imprimir_con_color(
                    f"Error con el archivo {nombre_archivo}: {error}",
                    color="amarillo",
                )
        else:
            self.imprimir_con_color("Nada seleccionado.", "blanco")
            self.mostrar_mensaje_advertencia("Nada seleccionado.")

    def procesar_archivos(self):
        directorio = self.seleccionar_carpeta("/Exportaciones/Crudos/")
        destino = self.seleccionar_carpeta("/Exportaciones/Crudos/")

        # Obtén la lista de nombres de archivos en el directorio
        nombres_archivos = os.listdir(directorio)

        # Itera sobre los nombres de archivos
        for nombre_archivo in nombres_archivos:
            ruta_archivo = os.path.join(directorio, nombre_archivo)

            if os.path.isfile(ruta_archivo):
                try:
                    df = pd.read_excel(ruta_archivo, header=None)
                    df.iloc[:, 0] = df.iloc[:, 0].astype(str)
                    largo_df = self.medir_largo_estructura(df)
                    paso_columns = self.find_paso_columns(df)
                    paso_data = self.get_paso_data(df, paso_columns)
                    paso_dates = self.get_paso_dates(df, paso_columns)
                    paso_dates = set(paso_dates)
                    print("")
                    self.imprimir_con_color(
                        f"Fechas en el archivo {nombre_archivo.replace('.xlsx','')}:",
                        color="blanco",
                    )
                    for fecha in paso_dates:
                        self.imprimir_con_color(f"{fecha}", color="blanco")
                    self.imprimir_con_color(
                        f"Total registros: {largo_df}", color="blanco"
                    )
                    suma_subs = 0
                    try:
                        for fecha in paso_dates:
                            largo_sub = self.filtrar_y_guardar_campo(
                                paso_data, fecha, destino
                            )
                            suma_subs += largo_sub
                    except Exception:
                        listado_errores = self.obtener_lineas_de_errores(
                            df, paso_columns
                        )
                        raise ValueError(
                            f"{self.generar_str_error_con_lineas(listado_errores)}"
                        )
                    if suma_subs == largo_df:
                        self.imprimir_con_color(
                            f"La suma de sub-listados [{suma_subs}] coincide con el total [{largo_df}]",
                            "verde",
                        )
                    else:
                        if (largo_df - suma_subs) <= 4:
                            self.imprimir_con_color(
                                f"La suma de sub-listados [{suma_subs}] NO coincide con el total [{largo_df}] en {(largo_df - suma_subs)} registros.",
                                "amarillo",
                            )
                        elif (largo_df - suma_subs) > 4:
                            self.imprimir_con_color(
                                f"La suma de sub-listados [{suma_subs}] NO coincide con el total [{largo_df}] en {(largo_df - suma_subs)} registros.",
                                "rojo",
                            )
                except Exception as error:
                    self.imprimir_con_color(
                        f"Error con el archivo {nombre_archivo}: {error}",
                        color="amarillo",
                    )
