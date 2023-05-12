import re
import checkpoints as ck
import pandas as pd
import tkinter as tk
from pathlib import Path as Ph
from tkinter import filedialog
import checkpoints


class Inicial:
    def __init__(self, path):
        self._root = tk.Tk()
        self._root.withdraw()
        self._path = path
        # checkpoints
        self._checkpoints = ck.cp_iniciales
        self._ident = ck.cp_iden
        self._cortes_datos = ck.cp_datos
        self._cortes_inv = ck.cp_inv
        self._cortes_efectos = ck.cp_efectos
        self._encabezados = ck.encabezados
        self.procesado = self._procesar(
            self._path,
            self._ident,
            self._checkpoints,
            self._cortes_datos,
            self._cortes_inv,
            self._cortes_efectos,
        )
        self._convertir(self.procesado, self._encabezados)

    def _cargar(self, path, no_tiene_encabezados=True):
        if no_tiene_encabezados:
            data = pd.read_excel(path, header=None)
        else:
            data = pd.read_excel(path)
        a = data.values.tolist()
        return a

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
        return b

    def _procesar(self, path, ident, check, cortes_datos, cortes_inv, cortes_efectos):
        crudo = self._cargar(path)
        formateado, identificadores = self._formatear(crudo, ident)
        particiones = self._recuperar_values(self._barrer_inicial(formateado, check))
        datos_hecho = self._descomponer(particiones, cortes_datos, 1)
        for item in datos_hecho:
            item[" CALIFICACIÓN LEGAL DEL HECHO "] = (
                " CALIFICACIÓN LEGAL DEL HECHO "
                + item[" CALIFICACIÓN LEGAL DEL HECHO "]
            )
        datos_inv = self._descomponer(particiones, cortes_inv, 0, encabezados=False)
        datos_efectos = self._descomponer(
            particiones, cortes_efectos, 3, encabezados=False
        )
        general = ck.general
        final = self._unificar(
            identificadores,
            datos_hecho,
            datos_inv,
            datos_efectos,
            particiones,
            general,
        )

        return final

    def _convertir(self, archivo, encabezados):
        # ult = pd.DataFrame(archivo, columns=encabezados)
        # ult.to_excel(
        #    rf"{Ph(__file__).resolve().parent}\Exportaciones\unificada.xlsx",
        #    index=False,
        # )

        ult = pd.DataFrame(self._borrar_duplicados(archivo), columns=encabezados)
        ult.to_excel(
            rf"{Ph(__file__).resolve().parent}\Exportaciones\unificada sin dups.xlsx",
            index=False,
        )

    def _unificar(self, identificadores, hechos, involucrados, efectos, relatos, canon):
        unificada = []
        for i in range(0, len(hechos)):
            item = canon.copy()
            for key in hechos[i].keys():
                if key in item:
                    item[key] = hechos[i][key].strip()
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
                    ]
                elif i == len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] + len(clave) :]
                prueba[clave] = valor
            for k in canonico.keys():
                if k in prueba:
                    canonico[k] = prueba[k]
        elif encabezados is False:
            for i in range(0, len(posiciones)):
                if i < len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] : posiciones[i + 1][1]]
                elif i == len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] :]
                prueba[clave] = valor
            for k in canonico.keys():
                if k in prueba:
                    canonico[k] = prueba[k]
        return canonico

    def _descomponer(self, particiones, canon, paso, encabezados=True):
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

    def _recuperar_values(self, dics):
        a_lista = []
        for i in dics:
            registro = []
            for value in i.values():
                registro.append(value)
            a_lista.append(registro)
        return a_lista

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
            print(f"Hay {len(duplicados)} registros duplicados\n")
            for item in duplicados:
                print("\n")
                contador = 0
                for i in lista:
                    if i[0] == item:
                        contador += 1
                print(f"{item} está {contador} veces repetido")
                while contador > 1:
                    for z in range(0, len(lista)):
                        if lista[z][0] == item:
                            del lista[z]
                            print(f"Borrado 1 elemento de {item}")
                            contador -= 1
                            contador2 += 1
                            break
        print("\n\n\n")
        print(len(lista))
        return lista

    def _clean_regexs(self, text):
        regexp = r"(Nº de Denuncia: | N° de Acta de Procedimiento: )..................................................(FORMULARIO DE DECLARACIÓN |ACTA DE PROCEDIMIENTO ).......................................................................\d+(/)\d+"
        return re.sub(regexp, "", text)


class Segmentado(Inicial):
    def __init__(self, path):
        self._root = tk.Tk()
        self._root.withdraw()
        self._path = path
        self.segmentados = self._cargar(self._path, no_tiene_encabezados=False)
        self.indexados = self._indexador(self.segmentados)
        self.calificaciones = list(
            map(
                lambda x: x.replace("CALIFICACIÓN LEGAL DEL HECHO ", ""),
                self._separar(
                    self._armar_paquete(self.indexados, 26),
                    ck.splitters["calificaciones"],
                ),
            )
        )
        self.armas = self._separar(
            self._armar_paquete(self.indexados, 41), ck.splitters["armas"]
        )
        self.objetos = self._separar(
            self._armar_paquete(self.indexados, 43), ck.splitters["elementos"]
        )
        self.secuestros = self._separar(
            self._armar_paquete(self.indexados, 42), ck.splitters["elementos"]
        )
        self.automotores = self._separar(
            self._armar_paquete(self.indexados, 40), ck.splitters["automotores"]
        )
        self.testigos_procedimiento = self._armar_paquete(self.indexados, 32)
        self.testigos_presenciales = self._armar_paquete(self.indexados, 28)
        self.victimas = self._armar_paquete(self.indexados, 30)
        self.personas_confianza = self._armar_paquete(self.indexados, 34)
        self.aprehendidos = self._armar_paquete(self.indexados, 31)
        self.sospechosos = self._armar_paquete(self.indexados, 29)
        self.denunciados = self._armar_paquete(self.indexados, 36)
        self.denunciante = self._armar_paquete(self.indexados, 35)
        self.representante = self._armar_paquete(self.indexados, 33)
        self.buenas = self._todo_un_campo_involucrado(
            self.representante, checkpoints.representantes
        )

    def comparar(self, path):
        para_comparar = self._cargar(path)
        nuevo = list(map(lambda x: x[0], para_comparar))
        nuevo2 = list(map(lambda x: x[1], self.indexados))
        faltantes = []
        for i in nuevo:
            try:
                nuevo2.index(i)
            except Exception:
                faltantes.append(i)
        print(len(nuevo))
        print(len(nuevo2))
        return faltantes

    def temporal(self):
        palabras = [
            self.calificaciones,
            self.armas,
            self.objetos,
            self.secuestros,
            self.automotores,
        ]

        for i in palabras:
            if len(i) >= 2:
                for j in i:
                    print(j)
            else:
                print("Sin elementos")
            print("\n\n")

    def _indexador(self, archivo, index=1):
        nuevo = []
        for item in archivo:
            nw_item = item.copy()
            nw_item.insert(0, index)
            nuevo.append(nw_item)
            index += 1
        return nuevo

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
        return nuevo

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

    def _descomponer_involucrado(self, texto, canon):
        cortes = list(canon.keys())
        nuevo = self._segmentador(texto, self._posiciones_datos(texto, cortes), canon)
        return nuevo

    def _todo_un_campo_involucrado(self, lista, canon):
        nuevo = []
        nuevo.extend(
            list(map(lambda x: self._descomponer_involucrado(x[1], canon), lista))
        )
        return self._recuperar_values(nuevo)
