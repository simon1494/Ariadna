import sys

sys.path.append("../ariadna")
import pandas as pd
import tkinter as tk
import checkpoints as ck
import os

# Obtener la ruta del directorio padre del archivo actual (tu_proyecto)
DIRECTORIO_PADRE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Administrador:
    @staticmethod
    def _cargar(path, no_tiene_encabezados=True, es_original=True):
        if no_tiene_encabezados:
            data = pd.read_excel(path, header=None)
        else:
            data = pd.read_excel(path)
        a = data.values.tolist()
        if es_original:
            a = [
                sublista
                for sublista in a
                if sublista[0].lower() not in ["anulado", "anulada"]
            ]
        return a

    @staticmethod
    def _convertir_inicial(archivo, encabezados, nombre=None, error=False):
        if not error:
            if nombre == None:
                nombre_archivo = tk.simpledialog.askstring(
                    "Nombre", "Nombre del archivo:"
                )
            else:
                nombre_archivo = nombre
            ult = pd.DataFrame(archivo, columns=encabezados)
            ult.to_excel(
                rf"{DIRECTORIO_PADRE}\Exportaciones\No segmentados\{nombre_archivo} (ns).xlsx",
                index=False,
            )
            return rf"{DIRECTORIO_PADRE}\Exportaciones\No segmentados\{nombre_archivo} (ns).xlsx"
        else:
            nombre_archivo = "(log_errores)"
            ult = pd.DataFrame(archivo, columns=encabezados)
            ult.to_excel(
                rf"{DIRECTORIO_PADRE}\Exportaciones\{nombre} {nombre_archivo}.xlsx",
                index=False,
            )
            return rf"{DIRECTORIO_PADRE}\Exportaciones\{nombre} {nombre_archivo}.xlsx"

    @staticmethod
    def _convertir_segmentado(archivo, nombre=False):
        if not nombre:
            nombre_archivo = tk.simpledialog.askstring("Nombre", "Nombre del archivo:")
        else:
            nombre_archivo = nombre

        writer = pd.ExcelWriter(
            rf"{DIRECTORIO_PADRE}\Exportaciones\Segmentados\{nombre_archivo.replace(' (ns).xlsx','')} (seg).xlsx",
            engine="xlsxwriter",
        )

        hechos_enc = ck.general_datos.copy()
        hechos_enc.insert(0, "id")
        hechos = pd.DataFrame(archivo[0], columns=hechos_enc)
        hechos["Latitud:"] = hechos["Latitud:"].astype(str)
        hechos["Longitud:"] = hechos["Longitud:"].astype(str)
        hechos.to_excel(
            writer,
            sheet_name="datos_hecho",
            index=False,
        )

        cal_enc = list(ck.general_calificaciones.keys())
        cal_enc.insert(0, "id")
        cal = pd.DataFrame(archivo[1], columns=cal_enc)
        cal.to_excel(
            writer,
            sheet_name="calificaciones",
            index=False,
        )

        armas_enc = list(ck.general_armas.keys())
        armas_enc.insert(0, "id")
        armas = pd.DataFrame(archivo[2], columns=armas_enc)
        armas.to_excel(
            writer,
            sheet_name="armas",
            index=False,
        )

        aut_enc = list(ck.general_automotores.keys())
        aut_enc.insert(0, "id")
        automotores = pd.DataFrame(archivo[3], columns=aut_enc)
        automotores.to_excel(
            writer,
            sheet_name="automotores",
            index=False,
        )

        obj_enc = list(ck.general_elementos.keys())
        obj_enc.insert(0, "id")
        objetos = pd.DataFrame(archivo[4], columns=obj_enc)
        objetos.to_excel(
            writer,
            sheet_name="objetos",
            index=False,
        )

        secu_enc = list(ck.general_elementos.keys())
        secu_enc.insert(0, "id")
        secuestros = pd.DataFrame(archivo[5], columns=secu_enc)
        secuestros.to_excel(
            writer,
            sheet_name="secuestros",
            index=False,
        )

        inv_enc = list(ck.general_involucrados.keys())
        inv_enc.insert(0, "id")
        involucrados = pd.DataFrame(archivo[6], columns=inv_enc)
        involucrados.to_excel(
            writer,
            sheet_name="involucrados",
            index=False,
        )

        writer.close()

    @staticmethod
    def _obtener_indices(archivo, antiguos):
        nuevos_indices = []

        for i in range(0, len(archivo)):
            if len(archivo[i]) > 0:
                nuevos_indices.append(int(archivo[i][-1][0]))
            else:
                nuevos_indices.append(antiguos[i] - 1)
        return nuevos_indices

    def _cargar_final(path):
        df = pd.read_excel(path, sheet_name=None)
        lista_anidada = []
        for hoja, datos in df.items():
            registros = []
            for indice, fila in datos.iterrows():
                registro = fila.to_list()
                registros.append(registro)
            lista_anidada.append(registros)

        return lista_anidada
