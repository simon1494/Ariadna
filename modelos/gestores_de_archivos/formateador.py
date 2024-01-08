import sys

sys.path.append("../ariadna")
import re
import pandas as pd
from modelos.motores.motor_base import MotorBase


class Formateador(MotorBase):
    def _formatear(self, lista, identi):
        quitados = 0
        final = []
        identificadores = []
        for i in lista:
            texto = i[0]
            que_uso = identi[0] if texto.find("Nº de Denuncia: ") != -1 else identi[1]
            iden = self._segmentador(
                texto,
                self._posiciones_datos(texto, que_uso),
                que_uso,
            )
            texto2 = texto.replace("_x000D_", "")
            texto2 = texto2.replace("\n", " ")
            texto2 = texto2.replace("  ", " ")
            texto2 = self._clean_regexs(texto2)
            texto2 = texto2.replace("  ", " ")
            if texto2.find("NO VÁLIDO COMO DOCUMENTO LEGAL") == -1:
                # AGREGADO 2023-07-28 para filtrar registros no asignados a fiscalía
                final.append(texto2)
                valor = iden.pop(que_uso[0])
                iden[" Nro registro: "] = valor
                del iden[que_uso[2]]
                identificadores.append(iden.copy())
            else:
                quitados += 1
        if quitados > 0:
            mensaje = f"Se filtraron {quitados} registros no asignados a fiscalía."
            self.imprimir_con_color(mensaje, "amarillo")
        return final, identificadores

    def _clean_regexs(self, text):
        regex0 = r"(Nº de Denuncia: | N° de Acta de Procedimiento: )..................................................(FORMULARIO DE DECLARACIÓN |ACTA DE PROCEDIMIENTO ).......................................................................\d+(/)\d+"
        regex1 = r"PP:......................(N° de Acta de Procedimiento: |Nº de Denuncia: ).........................................................................................................................\d/\d"
        regex2 = r"( PP:).................................................................................................Emitido por el Sistema...................................................\d*"
        regex3 = r"(Nº de Denuncia)....................................................FORMULARIO.......................................................................................\d*/\d*"
        regex4 = r"(N° de Acta de Procedimiento: )..................................................ACTA......................................................................\d*/\d*/\d*.......-.\d*/\d"
        texto = re.sub(regex0, "", text)
        texto1 = re.sub(regex1, "", texto)
        texto2 = re.sub(regex2, "", texto1)
        texto3 = re.sub(regex3, "", texto2)
        texto4 = re.sub(regex4, "", texto3)
        texto5 = texto4.replace(
            " INVOLUCRADO - TESTIGO DEL HECHO DATOS ", " INVOLUCRADO - TESTIGO DATOS "
        )  # se agrega a causa de una actualización del Sisep con fecha 2023-06-09
        texto6 = texto5.replace(
            "CALIFICACIÓN LEGAL DEL HECHO Delito: ",
            "CALIFICACIÓN LEGAL DEL HECHO Tipificación: ",
        )
        return texto6

    @staticmethod
    def comprobar_salida(archivo, advertencias=True):
        tablas = {
            "hechos": pd.DataFrame(archivo[0]),
            "armas": pd.DataFrame(archivo[2]),
            "automotores": pd.DataFrame(archivo[3]),
            "objetos": pd.DataFrame(archivo[4]),
            "secuestros": pd.DataFrame(archivo[5]),
            "involucrados": pd.DataFrame(archivo[6]),
        }
        df_vacios = []
        columnas_vacias = []
        no_nulos_con_nulos = []

        for campo, df in tablas.items():
            if len(df) > 0:
                if campo == "hechos":
                    for columna in df.columns:
                        if columna in [0, 1, 3, 4, 7, 14, 26, 29]:
                            contiene_nulos = df[columna].isna().any()
                            if contiene_nulos:
                                no_nulos_con_nulos.append((columna, campo))
                if campo in ["armas", "automotores", "objetos", "secuestros"]:
                    for columna in df.columns:
                        if columna in [0, 1, 2, 8]:
                            contiene_nulos = df[columna].isna().any()
                            if contiene_nulos:
                                no_nulos_con_nulos.append((columna, campo))
                if campo == "involucrados":
                    for columna in df.columns:
                        if columna in [0, 1, 2]:
                            contiene_nulos = df[columna].isna().any()
                            if contiene_nulos:
                                no_nulos_con_nulos.append((columna, campo))
                for columna in df.columns:
                    if columna not in [6, 7, 21, 22, 27, 30]:
                        contiene_nan = df[columna].isna().all()
                        if contiene_nan:
                            columnas_vacias.append((columna, campo))
            else:
                df_vacios.append(campo)

        mensaje = ""

        if len(columnas_vacias) > 0:
            mensaje = mensaje + "\n\nLas siguientes columnas estan vacías:"
            for columna, tabla in columnas_vacias:
                mensaje = mensaje + f"\n -Columna {columna} de la tabla '{tabla}'"

        if len(no_nulos_con_nulos) > 0:
            mensaje = mensaje + "\n\nLas siguientes columnas no nulas contienen nulos:"
            for columna, tabla in no_nulos_con_nulos:
                mensaje = mensaje + f"\n -Columna {columna} de la tabla '{tabla}'"

        if advertencias:
            if len(df_vacios) > 0:
                mensaje = mensaje + "Las siguientes tablas estan vacías:\n"
                for item in df_vacios:
                    mensaje = mensaje + f"\n -'{item}'"

            if 1200 > len(tablas["hechos"]) > 2400:
                if 1200 > len(tablas["hechos"]):
                    mensaje = (
                        mensaje + "\n\nEl archivo contiene menos de 1200 registros."
                    )
                elif len(tablas["hechos"]) > 2400:
                    mensaje = mensaje + "\n\nEl archivo contiene más de 2400 registros."

        return mensaje
