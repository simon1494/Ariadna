import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog
from pathlib import Path as Ph


class Inicial:
    def __init__(self, cp_iniciales, cp_datos, cp_inv, cp_efectos, canon):
        self.root = tk.Tk()
        self.root.withdraw()
        self.path = filedialog.askopenfilename()
        # checkpoints
        self.checkpoints = cp_iniciales
        self.cortes_datos = cp_datos
        self.cortes_inv = cp_inv
        self.cortes_efectos = cp_efectos
        # instancias de archivo
        self.crudo = self.cargar()
        self.formateado = self.formatear(self.crudo)
        self.particiones = self.barrer_inicial(self.formateado)
        self.datos_hecho = self.descomponer(self.particiones, self.cortes_datos, 1)
        self.datos_inv = self.descomponer(self.particiones, self.cortes_inv, 0)
        self.datos_efectos = self.descomponer(self.particiones, self.cortes_efectos, 3)
        self.general = canon
        self.final = self.unificada(
            self.datos_hecho, self.datos_inv, self.datos_efectos, self.general
        )

    def cargar(self):
        data = pd.read_excel(self.path)
        a = data.values.tolist()
        return a

    def clean_regexs(self, text):
        regexp = r"(Nº de Denuncia: | N° de Acta de Procedimiento: )..................................................(FORMULARIO DE DECLARACIÓN |ACTA DE PROCEDIMIENTO ).......................................................................\d+(/)\d+"
        return re.sub(regexp, "", text)

    def formatear(self, lista):
        final = []
        for i in lista:
            texto = i[0]
            texto2 = texto.replace("\n", " ")
            texto2 = texto2.replace("  ", " ")
            texto2 = self.clean_regexs(texto2)
            final.append(texto2)
        return final

    def barrer_inicial(self, listado):
        b = []
        for i in listado:
            if i.find(self.checkpoints[0][0]) == 0:
                x = self.segmentador(
                    i,
                    self.posiciones_datos(i, self.checkpoints[0]),
                    self.checkpoints[0],
                )
                b.append(x)
            else:
                x = self.segmentador(
                    i,
                    self.posiciones_datos(i, self.checkpoints[1]),
                    self.checkpoints[1],
                )
                b.append(x)
        return self.recuperar_values(b)

    def descomponer(self, particiones, canon, paso):
        b = []
        for i in particiones:
            x = self.segmentador(
                i[paso],
                self.posiciones_datos(i[paso], canon),
                canon,
            )
            b.append(x)
        return b

    def convertir(self, archivo):
        ult = pd.DataFrame(
            archivo, columns=["paso1", "paso2", "paso3", "paso4", "paso5"]
        )
        ult.to_excel(rf"{Ph(__file__).resolve().parent}\ult.xlsx")

    def recuperar_values(self, dics):
        a_lista = []
        for i in dics:
            registro = []
            for value in i.values():
                registro.append(value)
            a_lista.append(registro)
        return a_lista

    def posiciones_datos(self, texto, cortes, quitar=True):
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

    def segmentador(self, texto, puntos_de_corte, canon):
        para_buscar = texto
        posiciones = puntos_de_corte
        canonico = {}
        for i in canon:
            canonico[i] = ""
        prueba = {}
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
        return canonico

    def unificada(self, hechos, involucrados, efectos, canon):
        unificada = []
        canonico = canon
        for i in range(0, len(hechos)):
            item = canonico
            for key in hechos[i].keys():
                item[key] = hechos[i][key]
            for key in involucrados[i].keys():
                item[key] = involucrados[i][key]
            for key in efectos[i].keys():
                item[key] = efectos[i][key]
            unificada.append(item)
        return unificada
