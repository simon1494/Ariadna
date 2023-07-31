import sys

sys.path.append("../ariadna")
import copy
import checkpoints as ck
from .formateador import Formateador


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
