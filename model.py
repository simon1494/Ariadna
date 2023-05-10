import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog
from pathlib import Path as Ph
from checkpoints import encabezados


class Inicial:
    def __init__(self, cp_iniciales, cp_ident, cp_datos, cp_inv, cp_efectos, canon):
        self.root = tk.Tk()
        self.root.withdraw()
        self.path = filedialog.askopenfilename()
        # checkpoints
        self.checkpoints = cp_iniciales
        self.ident = cp_ident
        self.cortes_datos = cp_datos
        self.cortes_inv = cp_inv
        self.cortes_efectos = cp_efectos
        # instancias de archivo
        self.crudo = self.cargar()
        self.formateado, self.identificadores = self.formatear(self.crudo)
        self.particiones = self.recuperar_values(
            self.barrer_inicial(self.formateado, self.checkpoints)
        )
        self.datos_hecho = self.descomponer(self.particiones, self.cortes_datos, 1)
        self.datos_inv = self.descomponer(
            self.particiones, self.cortes_inv, 0, encabezados=False
        )
        self.datos_efectos = self.descomponer(
            self.particiones, self.cortes_efectos, 3, encabezados=False
        )
        self.general = canon
        self.final = self.unificar(
            self.identificadores,
            self.datos_hecho,
            self.datos_inv,
            self.datos_efectos,
            self.particiones,
            self.general,
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
        identificadores = []
        for i in lista:
            texto = i[0]
            que_uso = (
                self.ident[0] if texto.find("Nº de Denuncia: ") != -1 else self.ident[1]
            )
            iden = self.segmentador(
                texto,
                self.posiciones_datos(texto, que_uso),
                que_uso,
            )
            texto2 = texto.replace("\n", " ")
            texto2 = texto2.replace("  ", " ")
            texto2 = self.clean_regexs(texto2)
            final.append(texto2)
            valor = iden.pop(que_uso[0])
            iden[" Nro registro: "] = valor
            del iden[que_uso[2]]
            identificadores.append(iden.copy())
        return final, identificadores

    def barrer_inicial(self, listado, cortes):
        b = []
        for i in listado:
            if i.find(cortes[0][0]) == 0:
                x = self.segmentador(
                    i,
                    self.posiciones_datos(i, cortes[0]),
                    cortes[0],
                )
                b.append(x)
            else:
                x = self.segmentador(
                    i,
                    self.posiciones_datos(i, cortes[1]),
                    cortes[1],
                )
                b.append(x)
        return b

    def descomponer(self, particiones, canon, paso, encabezados=True):
        b = []
        for i in particiones:
            x = self.segmentador(
                i[paso],
                self.posiciones_datos(i[paso], canon),
                canon,
                encabezados=encabezados,
            )
            b.append(x)
        return b

    def convertir(self, archivo):
        ult = pd.DataFrame(archivo, columns=encabezados)
        ult.to_excel(rf"{Ph(__file__).resolve().parent}\Exportaciones\unificada.xlsx")

        ult = pd.DataFrame(self.borrar_duplicados(archivo), columns=encabezados)
        ult.to_excel(
            rf"{Ph(__file__).resolve().parent}\Exportaciones\unificada sin dups.xlsx"
        )

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

    def segmentador(self, texto, puntos_de_corte, canon, encabezados=True):
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

    def unificar(self, identificadores, hechos, involucrados, efectos, relatos, canon):
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
        return self.recuperar_values(unificada)

    def borrar_duplicados(self, archivo):
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
