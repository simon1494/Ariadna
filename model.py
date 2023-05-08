import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog
from pathlib import Path as Ph
from checkpoints import cascaron


class Inicial:
    def __init__(self, cp_iniciales, cp_hecho, cp_inv, cp_efectos):
        self.root = tk.Tk()
        self.root.withdraw()
        self.path = filedialog.askopenfilename()
        self.checkpoints = cp_iniciales
        self.cortes_datos = cp_hecho
        self.cortes_inv = cp_inv
        self.cortes_efectos = cp_efectos
        self.formateado = self.formatear(self.cargar())

    def cargar(self):
        data = pd.read_excel(self.path)
        a = data.values.tolist()
        return a

    def clean_regexs(self, text):
        regexp = r"(Nº de Denuncia: | N° de Acta de Procedimiento: )..................................................(FORMULARIO DE DECLARACIÓN |ACTA DE PROCEDIMIENTO ).......................................................................\d+(/)\d+"
        return re.sub(regexp, "", text)

    def oulala(self, texto2, pos_item):
        a = []
        for i in range(0, len(pos_item)):
            if i < len(pos_item) - 1:
                new_text = texto2[pos_item[i] : pos_item[i + 1]]
                a.append(new_text)
            else:
                new_text = texto2[pos_item[i] :]
                a.append(new_text)
        if len(a) < 5:
            a.insert(1, "")
        return a

    def oulala2(self, texto2, pos_item):
        a = []
        for i in range(0, len(pos_item)):
            if i < len(pos_item) - 1:
                new_text = texto2[pos_item[i] : pos_item[i + 1]]
                a.append(new_text)
            else:
                new_text = texto2[pos_item[i] :]
                a.append(new_text)
        if len(a) < 5:
            a.insert(1, "")
        return a

    def imprimir(self, res):
        for i in range(0, len(res)):
            print(res[i] + "\n\n\n")

    def formatear(self, lista):
        final = []
        for i in lista:
            texto = i[0]
            texto2 = texto.replace("\n", " ")
            texto2 = texto2.replace("  ", " ")
            texto2 = self.clean_regexs(texto2)
            final.append(texto2)
        return final

    def barrer(self, lista):
        b = []
        pos = self.posiciones()
        counter = 0
        for i in lista:
            if i.find(self.checkpoints[0][0]) == 0:
                x = self.oulala(i, pos[counter])
                b.append(x)
            else:
                x = self.oulala(i, pos[counter])
                b.append(x)
            counter += 1
        return b

    def convertir(self):
        archivo = self.cargar()
        listo = self.formatear(archivo)
        asdf = self.barrer(listo)
        ult = pd.DataFrame(asdf, columns=["paso1", "paso2", "paso3", "paso4", "paso5"])
        ult.to_excel(rf"{Ph(__file__).resolve().parent}\ult.xlsx")

    def posiciones(self, quitar=True):
        posiciones = []
        archivo = self.cargar()
        listo = self.formatear(archivo)
        for i in listo:
            item = []
            if i.find(self.checkpoints[0][0]) == 0:
                for j in self.checkpoints[0]:
                    item.append(i.find(j))
                posiciones.append(item)
            else:
                for k in self.checkpoints[1]:
                    item.append(i.find(k))
                posiciones.append(item)
            if quitar is True:
                try:
                    item.remove(-1)
                except Exception:
                    pass
        return posiciones

    def posiciones_datos(self, cortes, quitar=False):
        posiciones = []
        contador = 1
        archivo = self.cargar()
        listo = self.formatear(archivo)
        for i in listo:
            item = [contador]
            for j in cortes:
                item.append(i.find(j))
            if quitar is True:
                for i in range(0, len(item)):
                    try:
                        item.remove(-1)
                    except Exception:
                        pass
            posiciones.append(item)
            contador += 1
        posiciones.append(item)
        return posiciones

    def reordenar(self, quitar=False):
        estructura = {}
        keys = self.cortes_datos
        posiciones = self.posiciones_datos(self.cortes_datos)
        contador = 1
        for h in posiciones:
            registro = {}
            for i in range(0, len(keys)):
                registro[keys[i]] = h[i]
            # registro = sorted(registro.items(), key=lambda x: x[1])
            if quitar is True:
                for i in range(0, len(registro)):
                    try:
                        registro[i].index(-1)
                        registro = registro.pop[i]
                    except Exception:
                        pass
            estructura[contador] = registro
            contador += 1
        return estructura

    def rearmar(self, archivo):
        estructura = self.reordenar(quitar=True)
        rearmado = {}
        index = 1
        for i in archivo:
            new_registro = {}
            for j in estructura.keys():
                new_registro[j]
