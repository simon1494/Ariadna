import sys

sys.path.append("../ariadna")
import re
from .motor_base import MotorBase


class MotorInicial(MotorBase):
    def _regex(self, iter):
        # retorna una expresión regular armada a partir de una lista o las claves de un diccionario
        resultado = ""
        nueva_lista = (
            iter
            if isinstance(iter, tuple) or isinstance(iter, list)
            else list(iter.keys())
        )
        for item in nueva_lista:
            if nueva_lista.index(item) != 0:
                resultado = f"{resultado}|{item}"
            else:
                resultado = f"{item}"
        return re.compile(f"({resultado})")

    def _todos(self, archivo, general, paso):
        resultado = []
        for registro in archivo:
            nuevo = self._un_solo(
                self._prueba(self._regex(general), registro[paso]), general
            )
            resultado.append(nuevo)
        return resultado

    def _efectos(self, archivo, general):
        resultado = []
        for registro in archivo:
            if registro[1].find("INSTA A LA ACCIÓN") > -1:
                nuevo = self._un_solo(
                    self._prueba(self._regex(general[1][1]), registro[2]), general[1][1]
                )
                nuevo.update(
                    self._un_solo(
                        self._prueba(self._regex(general[1][0]), registro[3]),
                        general[1][0],
                    )
                )
                resultado.append(nuevo)
            elif registro[1].find("INSTA A LA ACCIÓN") == -1:
                nuevo = self._un_solo(
                    self._prueba(self._regex(general[0]), registro[3]), general[0]
                )
                resultado.append(nuevo)
        for item in resultado:
            item["¿Aporta documentación en este acto?"] = item[
                "¿Aporta documentación en este acto?"
            ].replace("¿Aporta documentación en este acto? ", "")
            item["¿Aporta efectos en este acto?"] = item[
                "¿Aporta efectos en este acto?"
            ].replace("¿Aporta efectos en este acto? ", "")
        return resultado

    def _prueba(self, regex, texto):
        resultado = []
        coincidencias = re.finditer(regex, texto)
        posiciones = [coincidencia.start() for coincidencia in coincidencias]
        for i in range(0, len(posiciones)):
            if i == len(posiciones) - 1:
                texto1 = texto[posiciones[i] :]
            else:
                texto1 = texto[posiciones[i] : posiciones[i + 1]]
            resultado.append(texto1)
        return resultado

    def _un_solo(self, lista, general):
        # Retorna UN SOLO diccionario con claves iguales a los elementos de "general".
        # Luego, busca en cada item de "lista" las claves de ese diccionario;
        # si la encuentra, la agrega al valor de esa clave. Especialmente util
        # para separar correctamente los efectos o involucrados de un registros
        # que se encuentran desordenados.
        claves = general
        canonico = {elemento: "" for elemento in claves}
        for i in list(canonico.keys()):
            for j in lista:
                if j.find(i) != -1:
                    canonico[i] = (f"{canonico[i]} {j}").strip()
        return canonico
