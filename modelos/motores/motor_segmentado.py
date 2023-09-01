import sys

sys.path.append("../ariadna")
import pandas as pd
import settings as ck
from .motor_base import MotorBase


class MotorSegmentado(MotorBase):
    def _armar_paquete(self, archivo, columna):
        nuevo = []
        for item in archivo:
            if pd.isna(item[columna]) is False:
                elemento = []
                indice_hecho = item[0]
                texto = item[columna]
                elemento.append(indice_hecho)
                elemento.append(texto)
                nuevo.append(elemento)
        return self._separar(nuevo, self._seleccionar_splitter(columna))

    def _separar(self, archivo, splitter):
        nuevo = []
        for i in range(0, len(archivo)):
            texto = archivo[i][1]
            a = splitter
            matches = texto.split(a)
            id = f"id_hecho {str(archivo[i][0])} "
            del matches[0]
            matches = list(map(lambda x: a + x, matches))
            matches = list(map(lambda x: id + x, matches))
            nuevo.extend(matches)
        return nuevo

    def _descomponer(self, particiones, canon, indice, encabezados=True):
        b = []
        for i in particiones:
            x = self._segmentador(
                i,
                self._posiciones_datos(i, canon),
                canon,
                encabezados=encabezados,
            )
            b.append(x)
        return self._indexador(self._recuperar_values(b), indice)

    def _descomponer_involucrado(self, texto, canon):
        general = ck.general_involucrados.copy()
        cortes = list(canon.keys())
        texto1 = texto.replace(cortes[1], self._tipo_involucrado(cortes[1]))
        texto1 = texto1.replace(
            " Descripción: ", " Descripcion: "
        )  # a causa de una actualización del sistema Sisep en el campo
        nuevo = self._segmentador(texto1, self._posiciones_datos(texto1, cortes), canon)
        for key in nuevo:
            if key in general:
                general[key] = nuevo[key]
                general[" tipo: "] = nuevo[list(nuevo.keys())[1]].strip()
        return general

    def _todo_un_campo_involucrado(self, lista, canon):
        nuevo = []
        nuevo.extend(
            list(map(lambda x: self._descomponer_involucrado(x, canon), lista))
        )
        return self._recuperar_values(nuevo)

    def _tipo_involucrado(self, tipo):
        match tipo:
            case " INVOLUCRADO - APREHENDIDO DATOS":
                return " INVOLUCRADO - APREHENDIDO DATOS Aprehendido"
            case " INVOLUCRADO - TESTIGO DATOS":
                return " INVOLUCRADO - TESTIGO DATOS Testigo presencial"
            case " INVOLUCRADO - PERSONA DE CONFIANZA DATOS":
                return " INVOLUCRADO - PERSONA DE CONFIANZA DATOS Persona de confianza"
            case " INVOLUCRADO - TESTIGO DEL PROCEDIMIENTO DATOS":
                return " INVOLUCRADO - TESTIGO DEL PROCEDIMIENTO DATOS Testigo de procedimiento"
            case " INVOLUCRADO - REPRESENTANTE DATOS":
                return " INVOLUCRADO - REPRESENTANTE DATOS Representante"
            case " INVOLUCRADO - SOSPECHOSO DATOS":
                return " INVOLUCRADO - SOSPECHOSO DATOS Sospechoso"
            case " INVOLUCRADO - DENUNCIADO DATOS":
                return " INVOLUCRADO - DENUNCIADO DATOS Denunciado"
            case " INVOLUCRADO - VICTIMA DATOS":
                return " INVOLUCRADO - VICTIMA DATOS Victima"
            case " DENUNCIANTE DATOS":
                return " DENUNCIANTE DATOS Denunciante"
            case " INVOLUCRADO - PROFUGO DATOS":
                return " INVOLUCRADO - PROFUGO DATOS Profugo"

    def _seleccionar_splitter(self, columna):
        match columna:
            case 26:
                return ck.splitters["calificaciones"]
            case 29:
                return ck.splitters["testigos_pre"]  #
            case 30:
                return ck.splitters["sospechosos"]  #
            case 31:
                return ck.splitters["victimas"]  #
            case 32:
                return ck.splitters["aprehendidos"]  #
            case 33:
                return ck.splitters["profugos"]
            case 34:
                return ck.splitters["testigos_pro"]
            case 35:
                return ck.splitters["representantes"]
            case 36:
                return ck.splitters["confianzas"]
            case 37:
                return ck.splitters["denunciantes"]
            case 38:
                return ck.splitters["denunciados"]
            case 42:
                return ck.splitters["automotores"]
            case 43:
                return ck.splitters["armas"]
            case 44:
                return ck.splitters["secuestros"]
            case 45:
                return ck.splitters["objetos"]

    def _todos_los_involucrados(self, involucrados, indice, limpiar=False):
        nuevo = []
        nuevo.extend(
            self._todo_un_campo_involucrado(involucrados[0], ck.testigos_procedimiento)
        )

        nuevo.extend(
            self._todo_un_campo_involucrado(involucrados[1], ck.testigos_presenciales)
        )

        nuevo.extend(self._todo_un_campo_involucrado(involucrados[2], ck.victimas))

        nuevo.extend(self._todo_un_campo_involucrado(involucrados[3], ck.confianzas))

        nuevo.extend(self._todo_un_campo_involucrado(involucrados[4], ck.aprehendidos))

        nuevo.extend(self._todo_un_campo_involucrado(involucrados[5], ck.sospechosos))

        nuevo.extend(self._todo_un_campo_involucrado(involucrados[6], ck.denunciados))

        nuevo.extend(self._todo_un_campo_involucrado(involucrados[7], ck.denunciantes))

        nuevo.extend(
            self._todo_un_campo_involucrado(involucrados[8], ck.representantes)
        )

        nuevo.extend(self._todo_un_campo_involucrado(involucrados[9], ck.profugos))

        for index, item in enumerate(nuevo, indice):
            item.insert(0, str(index))

        return nuevo
