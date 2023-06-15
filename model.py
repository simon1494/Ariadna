import re
import copy
import tkinter as tk
import checkpoints as ck
import pandas as pd
from pathlib import Path as Ph


class Administrador:
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
            print(a[112])
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
                rf"{Ph(__file__).resolve().parent}\Exportaciones\No segmentados\{nombre_archivo} (ns).xlsx",
                index=False,
            )
            return rf"{Ph(__file__).resolve().parent}\Exportaciones\No segmentados\{nombre_archivo} (ns).xlsx"
        else:
            nombre_archivo = "(log_errores)"
            ult = pd.DataFrame(archivo, columns=encabezados)
            ult.to_excel(
                rf"{Ph(__file__).resolve().parent}\Exportaciones\{nombre} {nombre_archivo}.xlsx",
                index=False,
            )
            return rf"{Ph(__file__).resolve().parent}\Exportaciones\{nombre} {nombre_archivo}.xlsx"

    @staticmethod
    def _convertir_segmentado(archivo, nombre=False):
        if not nombre:
            nombre_archivo = tk.simpledialog.askstring("Nombre", "Nombre del archivo:")
        else:
            nombre_archivo = nombre

        writer = pd.ExcelWriter(
            rf"{Ph(__file__).resolve().parent}\Exportaciones\Segmentados\{nombre_archivo} (seg).xlsx",
            engine="xlsxwriter",
        )

        hechos_enc = ck.general_datos.copy()
        hechos_enc.insert(0, "id")
        hechos = pd.DataFrame(archivo[0], columns=hechos_enc)
        hechos["Latitud:"] = hechos["Latitud:"].astype(str)
        hechos["Longitud:"] = hechos["Latitud:"].astype(str)
        hechos.to_excel(
            writer,
            sheet_name="datos_hecho",
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

        armas_enc = list(ck.general_armas.keys())
        armas_enc.insert(0, "id")
        armas = pd.DataFrame(archivo[3], columns=armas_enc)
        armas.to_excel(
            writer,
            sheet_name="armas",
            index=False,
        )

        aut_enc = list(ck.general_automotores.keys())
        aut_enc.insert(0, "id")
        automotores = pd.DataFrame(archivo[2], columns=aut_enc)
        automotores.to_excel(
            writer,
            sheet_name="automotores",
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

        obj_enc = list(ck.general_elementos.keys())
        obj_enc.insert(0, "id")
        objetos = pd.DataFrame(archivo[4], columns=obj_enc)
        objetos.to_excel(
            writer,
            sheet_name="objetos",
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

        writer.close()

    @staticmethod
    def _obtener_indices(archivo):
        nuevos_indices = []

        for i in range(0, len(archivo)):
            if len(archivo[i]) > 0:
                nuevos_indices.append(int(archivo[i][-1][0]))
            else:
                nuevos_indices.append(None)
        return nuevos_indices

    """@staticmethod
    def quitar_anulados(archivo):
        final = [
            sublista
            for sublista in archivo
            if sublista[0].lower() not in ["anulado", "anulada"]
        ]
        return final"""


class CoreMotor:
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
            if nuevo[i] == "Sin especificar":
                nuevo[i] = ""
        return nuevo


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
                return ck.splitters["elementos"]
            case 45:
                return ck.splitters["elementos"]

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


class Formateador(CoreMotor):
    def _formatear(self, lista, identi):
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
            texto2 = texto.replace("\n", " ")
            texto2 = texto2.replace("  ", " ")
            texto2 = self._clean_regexs(texto2)
            final.append(texto2)
            valor = iden.pop(que_uso[0])
            iden[" Nro registro: "] = valor
            del iden[que_uso[2]]
            identificadores.append(iden.copy())
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
        return texto5

    @staticmethod
    def comprobar_salida(archivo):
        tablas = {
            "hechos": pd.DataFrame(archivo[0]),
            "automotores": pd.DataFrame(archivo[1]),
            "armas": pd.DataFrame(archivo[2]),
            "objetos": pd.DataFrame(archivo[3]),
            "secuestros": pd.DataFrame(archivo[4]),
            "involucrados": pd.DataFrame(archivo[5]),
        }

        df_vacios = []
        columnas_vacias = []

        for campo, df in tablas.items():
            if len(df) > 0:
                for columna in df.columns:
                    if columna != 27:
                        contiene_nan = df[columna].isna().all()
                        if contiene_nan:
                            columnas_vacias.append((columna, campo))
            else:
                df_vacios.append(campo)

        mensaje = ""

        if len(df_vacios) > 0:
            mensaje = mensaje + "Las siguientes tablas estan vacías:\n"
            for item in df_vacios:
                mensaje = mensaje + f"\n -'{item}'"

        if len(columnas_vacias) > 0:
            mensaje = mensaje + "\n\nLas siguientes columnas estan vacías:"
            for columna, tabla in columnas_vacias:
                mensaje = mensaje + f"\n -Columna {columna} de la tabla '{tabla}'"
        return mensaje


class Tester(Formateador):
    def __init__(self, archivo):
        self.errores = self.comprobar_entrada(archivo)
        self.errores_salida = None

    def comprobar_entrada(self, archivo):
        archiv = copy.deepcopy(archivo)
        registros, identificadores = self.formatear(archiv, ck.cp_iden)
        resultado = []
        for item in registros:
            if item.find("Paso 1 - Declaración Testimonial ") > -1:
                con1 = item.find("Paso 1 - Declaración Testimonial ") > -1
                con2 = item.find("Paso 2 - Declaración Testimonial ") > -1
                con3 = item.find("Paso 3 - Declaración Testimonial ") > -1
                con4 = item.find("Paso 4 - Declaración Testimonial ") > -1
                con5 = item.find("Paso 5 - Declaración Testimonial ") > -1
                final = con1 and con2 and con3 and con4 and con5
            else:
                con1 = item.find("Paso 1 - Funcionarios intervinientes") > -1

                con3 = item.find("Paso 3 - Relato del procedimiento") > -1
                con4 = (
                    item.find(
                        "Paso 4 - Elementos secuestrados y pruebas Elementos secuestrados y pruebas"
                    )
                    > -1
                )
                con5 = item.find("Paso 5 - Firmas") > -1
                final = con1 and con3 and con4 and con5
            if final is False:
                nuevo = []
                nuevo.append(registros.index(item))
                identificador = self.identificar(
                    identificadores[registros.index(item)]
                ).replace("-", "")
                identificador = identificador.replace("/", "")
                nuevo.append(identificador)
                nuevo.append(item)
                resultado.append(nuevo)
        resultado2 = list(map(list, set(map(tuple, resultado))))
        return resultado2

    @staticmethod
    def identificar(diccionario):
        if diccionario[" Nro registro: "] != "":
            return diccionario[" Nro registro: "]
        else:
            return "no identificado"

    def formatear(self, lista, identi):
        final = []
        identificadores = []
        lista_ = copy.deepcopy(lista)
        for i in lista_:
            texto = i[0]
            que_uso = identi[0] if texto.find("Nº de Denuncia: ") != -1 else identi[1]
            iden = self._segmentador(
                texto,
                self._posiciones_datos(texto, que_uso),
                que_uso,
            )
            texto2 = texto.replace("\n", " ")
            texto2 = texto2.replace("  ", " ")
            texto2 = self._clean_regexs(texto2)
            final.append(texto2)
            valor = iden.pop(que_uso[0])
            iden[" Nro registro: "] = valor
            del iden[que_uso[2]]
            identificadores.append(iden.copy())
        return final, identificadores


class Inicial(Core_Inicial):
    def __init__(self, archivo, identificadores):
        # checkpoints
        self._checkpoints = ck.cp_iniciales
        self._ident = ck.cp_iden
        self._cortes_datos = ck.cp_datos
        self._cortes_inv = ck.cp_inv
        self._cortes_efectos = ck.efectos_combinado
        self._encabezados = ck.encabezados
        self._general = ck.general

        # preparación y formateado de pasos iniciales
        self.formateado, self.identificadores = archivo, identificadores
        self.particiones = self._barrer_inicial(self.formateado, self._checkpoints)

        # procesamiento de campos iniciales
        self.datos_inv = self._todos(self.particiones, self._cortes_inv, 0)
        self.datos_efectos = self._efectos(self.particiones, self._cortes_efectos)
        self.datos_hecho = self._descomponer(self.particiones, self._cortes_datos, 1)
        self.datos_hecho = list(
            map(
                lambda item: {
                    **item,
                    "CALIFICACIÓN LEGAL DEL HECHO ": "CALIFICACIÓN LEGAL DEL HECHO "
                    + item["CALIFICACIÓN LEGAL DEL HECHO "],
                },
                self.datos_hecho,
            )
        )
        self.datos_hecho = list(
            map(
                lambda item: {
                    **item,
                    " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada": item[
                        " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada"
                    ].replace(
                        ": ", ""
                    ),
                },
                self.datos_hecho,
            )
        )

        # unificado de campos iniciales
        self.procesados = self._unificar(
            self.identificadores,
            self.datos_hecho,
            self.datos_inv,
            self.datos_efectos,
            self.particiones,
            self._general,
        )
        self.sin_duplicados = self._borrar_duplicados(self.procesados)
        self.sin_duplicados = list(
            map(lambda registro: self.limpiar_relato(registro), self.sin_duplicados)
        )

    def _barrer_inicial(self, listado, cortes):
        b = []
        for i in listado:
            if i.find(cortes[0][0]) == 0:
                x = self._segmentador(
                    i,
                    self._posiciones_datos(i, cortes[0]),
                    cortes[0],
                )
                b.append(x)
            else:
                x = self._segmentador(
                    i,
                    self._posiciones_datos(i, cortes[1]),
                    cortes[1],
                )
                b.append(x)
        return self._recuperar_values(b)

    def _unificar(self, identificadores, hechos, involucrados, efectos, relatos, canon):
        unificada = []
        for i in range(0, len(hechos)):
            item = canon.copy()
            for key in hechos[i].keys():
                if key in item:
                    item[key] = hechos[i][key].strip()
            if item[" Descripción:"] == "":
                try:
                    item[" Descripción:"] = hechos[i][" Descripcion:"]
                except Exception as error:
                    print(f"Error en la 'Descripcion' del index {i}: {error}")
            for key in involucrados[i].keys():
                if key in item:
                    item[key] = involucrados[i][key].strip()
            for key in efectos[i].keys():
                if key in item:
                    item[key] = efectos[i][key].strip()
            for key in identificadores[i].keys():
                if key in item:
                    item[key] = identificadores[i][key].strip()
            item[" Relato: "] = relatos[i][2].strip()
            unificada.append(item.copy())
        return self._recuperar_values(unificada)

    @staticmethod
    def limpiar_relato(registro):
        registro_nuevo = copy.deepcopy(registro)
        texto = registro[38]
        regex1 = r"(Relato del procedimiento ).*RELATO DEL PROCEDIMIENTO: "
        regex2 = r"Relato del hecho RELATO DEL HECHO: "
        texto = re.sub(regex1, "", texto)
        texto = re.sub(regex2, "", texto)
        registro_nuevo[38] = texto
        return registro_nuevo

    def _borrar_duplicados(self, archivo):
        lista = archivo.copy()
        lista_nros = []
        duplicados = []
        contador2 = 0

        for i in range(0, len(lista)):
            lista_nros.append(lista[i][0])

        for i in range(0, len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i][0] == lista[j][0]:
                    duplicados.append(lista[j][0])

        duplicados = list(set(duplicados))

        if len(duplicados) > 0:
            for item in duplicados:
                print("\n")
                contador = 0
                for i in lista:
                    if i[0] == item:
                        contador += 1
                while contador > 1:
                    for z in range(0, len(lista)):
                        if lista[z][0] == item:
                            del lista[z]
                            contador -= 1
                            contador2 += 1
                            break
            if len(duplicados) > 0:
                for duplicado in duplicados:
                    print(duplicado)
                print(f"Se han eliminado {contador2} duplicados.\n")
        return lista


class Addendum:
    def rearmar_calificacion(self, registro, base, son_registros=True):
        if son_registros:
            calificacion = registro[26]
            base_nueva = base.copy()
            if calificacion.find("tipificación"):
                resultado = calificacion.split(
                    "CALIFICACIÓN LEGAL DEL HECHO Tipificación: "
                )
            else:
                resultado = calificacion.split("CALIFICACIÓN LEGAL DEL HECHO Delito: ")
            del resultado[0]
            resultado = list(map(lambda item: item.strip(), resultado))
            resultado = self.cotejar_todas(resultado, base_nueva)
            final = "; ".join(resultado)
            registro[26] = final
            return registro
        else:
            errores = []
            calificacion = registro[2]
            base_nueva = base.copy()
            calificacion = [calificacion.strip()]
            calificacion = self.cotejar_todas(calificacion, base_nueva)
            final = "; ".join(calificacion)
            registro[2] = final
            return registro

    @staticmethod
    def simplificada(calificacion):
        calificacion3 = calificacion.replace("Consumado: Si", "")
        calificacion4 = calificacion3.replace("Consumado: No", "")
        calificacion0 = calificacion4.replace(" ", "")
        calificacion1 = calificacion0.replace("-", "")
        calificacion2 = calificacion1.replace(".", "")
        return calificacion2

    def cotejar_una(self, calificacion, data):
        a_cotejar = self.simplificada(calificacion)
        if a_cotejar in data:
            resultado = data[a_cotejar]
            return resultado
        else:
            return "error"

    def cotejar_todas(self, elementos, data):
        final = list(map(lambda item: self.cotejar_una(item, data), elementos))
        return final

    @staticmethod
    def identificar_errores(archivo_original, modificado):
        errores = []
        for i in range(0, len(modificado)):
            if modificado[i][2].find("error") > -1:
                errores.append(
                    [
                        modificado[i][0],
                        modificado[i][1],
                        archivo_original[i][2],
                    ]
                )
        return errores


class Segmentado(Core_Final, Addendum):
    def __init__(self, archivo, indices, carpeta=False):
        # enlaza con la base de calificaciones actual y lo almanece en forma de diccionario
        self.base_calificaciones = dict(
            pd.read_excel(
                rf"{Ph(__file__).resolve().parent}\Base calificaciones\calificaciones_db.xlsx",
                header=None,
            ).values.tolist()
        )
        # preparación e indexado del archivo inicial
        self.segmentados = archivo
        self.indexados = self._indexador(self.segmentados, indices[0])

        # indexado de entidades simples)
        self.calificaciones = list(
            map(
                lambda x: x.replace("CALIFICACIÓN LEGAL DEL HECHO ", ""),
                self._armar_paquete(self.indexados, 26),
            )
        )
        self.armas = self._armar_paquete(self.indexados, 43)
        self.objetos = self._armar_paquete(self.indexados, 45)
        self.secuestros = self._armar_paquete(self.indexados, 44)
        self.automotores = self._armar_paquete(self.indexados, 42)

        # indexado de involucrados
        self.testigos_procedimiento = self._armar_paquete(self.indexados, 34)
        self.testigos_presenciales = self._armar_paquete(self.indexados, 29)  #
        self.victimas = self._armar_paquete(self.indexados, 31)  #
        self.personas_confianza = self._armar_paquete(self.indexados, 36)
        self.aprehendidos = self._armar_paquete(self.indexados, 32)  #
        self.sospechosos = self._armar_paquete(self.indexados, 30)  #
        self.denunciados = self._armar_paquete(self.indexados, 38)
        self.denunciante = self._armar_paquete(self.indexados, 37)
        self.representante = self._armar_paquete(self.indexados, 35)
        self.profugos = self._armar_paquete(self.indexados, 33)
        self.involucrados = [
            self.testigos_procedimiento,
            self.testigos_presenciales,
            self.victimas,
            self.personas_confianza,
            self.aprehendidos,
            self.sospechosos,
            self.denunciados,
            self.denunciante,
            self.representante,
            self.profugos,
        ]

        # segmentado de entidades simples
        self._automotores = self._descomponer(
            self.automotores, ck.general_automotores, indices[2]
        )
        self._armas = self._descomponer(self.armas, ck.general_armas, indices[3])
        self._objetos = self._descomponer(
            self.objetos, ck.general_elementos, indices[4]
        )
        self._secuestros = self._descomponer(
            self.secuestros, ck.general_elementos, indices[5]
        )
        self._calificaciones = self._descomponer(
            self.calificaciones, ck.general_calificaciones, indices[1]
        )
        self._calificaciones_chequeadas = list(
            map(
                lambda registro: self.rearmar_calificacion(
                    registro, self.base_calificaciones, son_registros=False
                ),
                copy.deepcopy(self._calificaciones),
            )
        )
        self.errores = self.identificar_errores(
            self._calificaciones, self._calificaciones_chequeadas
        )
        if not len(self.errores):
            self.indexados = list(
                map(
                    lambda registro: self.rearmar_calificacion(
                        registro, self.base_calificaciones
                    ),
                    self.indexados,
                )
            )
            self.datos = self._recortar(self.indexados)

            # segmentado y consolidación de todos los involucrados
            self._involucrados = self._todos_los_involucrados(
                self.involucrados, indices[6], limpiar=True
            )

            # limpieza de campos "Sin especificar".
            if not carpeta:
                if tk.messagebox.askyesno(
                    "Consulta", "¿Desea limpiar los 'Sin especificar?"
                ):
                    self.datos = list(
                        map(lambda x: self._limpiar_registro(x), self.datos)
                    )
                    self._automotores = list(
                        map(lambda x: self._limpiar_registro(x), self._automotores)
                    )
                    self._armas = list(
                        map(lambda x: self._limpiar_registro(x), self._armas)
                    )
                    self._objetos = list(
                        map(lambda x: self._limpiar_registro(x), self._objetos)
                    )
                    self._secuestros = list(
                        map(lambda x: self._limpiar_registro(x), self._secuestros)
                    )
                    self._involucrados = list(
                        map(lambda x: self._limpiar_registro(x), self._involucrados)
                    )
            else:
                self.datos = list(map(lambda x: self._limpiar_registro(x), self.datos))
                self._automotores = list(
                    map(lambda x: self._limpiar_registro(x), self._automotores)
                )
                self._armas = list(
                    map(lambda x: self._limpiar_registro(x), self._armas)
                )
                self._objetos = list(
                    map(lambda x: self._limpiar_registro(x), self._objetos)
                )
                self._secuestros = list(
                    map(lambda x: self._limpiar_registro(x), self._secuestros)
                )
                self._involucrados = list(
                    map(lambda x: self._limpiar_registro(x), self._involucrados)
                )
            # archivo final segmentado
            self.final = [
                self.datos,
                self._calificaciones,
                self._automotores,
                self._armas,
                self._objetos,
                self._secuestros,
                self._involucrados,
            ]
        else:
            tk.messagebox.showinfo(
                "Advertencia", f"Se detectaron calificaciones no existentes en base."
            )

    def _indexador(self, archivo, index):
        nuevo = []
        for item in archivo:
            nw_item = item.copy()
            nw_item.insert(0, index)
            nuevo.append(nw_item)
            index += 1
        return nuevo

    def _recortar(self, lista):
        a_eliminar = sorted(
            [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 42, 43, 44, 45], reverse=True
        )
        for sub in lista:
            for j in a_eliminar:
                del sub[j]
        return lista
