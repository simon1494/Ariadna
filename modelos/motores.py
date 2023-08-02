import sys

sys.path.append("../ariadna")
import re
import pandas as pd
import checkpoints as ck
from datetime import datetime
from .logueador import Logueador
from .cuadros_de_mensajes import Mensajes


class CoreMotor(Mensajes, Logueador):
    def _posiciones_datos(self, texto, cortes, quitar=True):
        contador = 0
        item = []
        for j in cortes:
            lista = []
            lista.append(j)
            lista.append(texto.find(j))
            if quitar is False:
                item.append(lista)
            elif quitar is True:
                if lista[1] == -1:
                    pass
                else:
                    item.append(lista)
        item = dict(item)
        item = sorted(item.items(), key=lambda x: x[1])
        contador += 1
        return item

    def _segmentador(self, texto, puntos_de_corte, canon, encabezados=True):
        para_buscar = texto
        posiciones = puntos_de_corte
        canonico = {}
        for i in canon:
            canonico[i] = ""
        prueba = {}
        if encabezados is True:
            for i in range(0, len(posiciones)):
                if i < len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[
                        posiciones[i][1] + len(clave) : posiciones[i + 1][1]
                    ].strip()
                elif i == len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] + len(clave) :].strip()
                prueba[clave] = valor
            for k in canonico.keys():
                if k in prueba:
                    canonico[k] = prueba[k]
        elif encabezados is False:
            for i in range(0, len(posiciones)):
                if i < len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] : posiciones[i + 1][1]].strip()
                elif i == len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] :].strip()
                prueba[clave] = valor
            for k in canonico.keys():
                if k in prueba:
                    canonico[k] = prueba[k]
        return canonico

    def _descomponer(self, particiones, canon, paso, encabezados=True):
        if paso != 1:
            b = []
            for i in particiones:
                x = self._segmentador(
                    i[paso],
                    self._posiciones_datos(i[paso], canon),
                    canon,
                    encabezados=encabezados,
                )
                b.append(x)
            return b
        elif paso == 1:
            b = []
            for i in particiones:
                if i[paso].find(" Descripcion:") > -1:
                    x = self._segmentador(
                        i[paso],
                        self._posiciones_datos(i[paso], canon[0]),
                        canon[0],
                        encabezados=encabezados,
                    )
                    b.append(x)
                elif i[paso].find(" Descripcion:") == -1:
                    x = self._segmentador(
                        i[paso],
                        self._posiciones_datos(i[paso], canon[1]),
                        canon[1],
                        encabezados=encabezados,
                    )
                    b.append(x)
            return b

    def _recuperar_values(self, dics):
        a_lista = []
        for i in dics:
            registro = []
            for value in i.values():
                registro.append(value)
            a_lista.append(registro)
        return a_lista

    def _limpiar_registro(self, registro):
        nuevo = registro.copy()
        for i in range(len(nuevo)):
            if nuevo[i] == "Sin especificar" or nuevo[i] == "Sin especifica":
                nuevo[i] = ""
        return nuevo

    def _formatear_fecha(self, registro, inicial=True):
        _registro = registro.copy()
        if inicial:
            try:
                if len(_registro[2]) > 4:
                    fecha_objeto = datetime.strptime(_registro[2], "%d %B %Y")
                    fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
                    _registro[2] = fecha_formateada

                if len(_registro[9]) > 4:
                    fecha_objeto = datetime.strptime(_registro[9], "%d %B %Y")
                    fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
                    _registro[9] = fecha_formateada

                if len(_registro[11]) > 4:
                    fecha_objeto = datetime.strptime(_registro[11], "%d %B %Y")
                    fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
                    _registro[11] = fecha_formateada
            except Exception as error:
                self.imprimir_con_color(error, "rojo")
            return _registro
        else:
            try:
                if len(_registro[15]) > 4 and _registro[15] != "Sin especifica":
                    fecha_objeto = datetime.strptime(_registro[15], "%d %B %Y")
                    fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
                    _registro[15] = fecha_formateada
            except Exception as error:
                self.imprimir_con_color(error, "rojo")
            return _registro


class Core_Inicial(CoreMotor):
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


class Core_Final(CoreMotor):
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
