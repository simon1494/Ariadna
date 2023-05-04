import pandas as pd
import re
from pathlib import Path as ph


class Inicial:
    def __init__(self):
        self.path = ph.cwd()
        self.checkpoints = (
            (
                "Paso 1 - Declaración Testimonial ",
                "Paso 2 - Declaración Testimonial ",
                "Paso 3 - Declaración Testimonial ",
                "Paso 4 - Declaración Testimonial ",
                "Paso 5 - Declaración Testimonial ",
            ),
            (
                "Paso 1 - Funcionarios intervinientes ",
                "Paso 2 - Partes intervinientes ",
                "Paso 3 - Relato del procedimiento ",
                "Paso 4 - Elementos secuestrados y pruebas Elementos secuestrados y pruebas ",
                "Paso 5 - Firmas ",
            ),
        )
        self.cortes = (
            "Fecha: ",
            "Hora: ",
            "Funcionario: ",
            "Jerarquía: ",
            "Dependencia: ",
            "Legajo: ",
            "FUNCIONARIO INTERVINIENTES DEL ACTA",
            "FECHA Y HORA DEL HECHO Fecha de Inicio: ",
            "Hora de Inicio: ",
            "Fecha de finalización: ",
            "Hora de finalización: ",
            "LUGAR DEL HECHO Partido: ",
            "Localidad: ",
            "Modo de Ingreso: ",
            "Latitud: ",
            "Calle: ",
            "Longitud: ",
            "Altura: ",
            "Piso: ",
            "Departamento: ",
            "Lugar Exacto: ",
            "Entre: ",
            "Descripcion: ",
            "CALIFICACIÓN LEGAL DEL HECHO",
            "INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada Deja constancia de la manifestación respecto a sí insta o no insta la acción: ",
            "N° de Acta de Procedimiento: ",
            "Nº de Denuncia: ",
            "PP: ",
            "ACTA DE PROCEDIMIENTO Emitido por el Sistema de Información Delictual el: ",
        )
        self.cortes_datos = (
            "Fecha:",
            "Hora:",
            "Funcionario:",
            "Jerarquía:",
            "Dependencia:",
            "Legajo:",
            "FUNCIONARIO INTERVINIENTES DEL ACTA",
            "FECHA Y HORA DEL HECHO Fecha de Inicio:",
            "Hora de Inicio:",
            "Fecha de finalización:",
            "Hora de finalización:",
            "LUGAR DEL HECHO Partido:",
            "Localidad:",
            "Modo de Ingreso:",
            "Latitud:",
            "Calle:",
            "Longitud:",
            "Altura:",
            "Piso:",
            "Departamento:",
            "Lugar Exacto:",
            "Entre:",
            "Descripcion:",
            "CALIFICACIÓN LEGAL DEL HECHO",
            "INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada Deja constancia de la manifestación respecto a sí insta o no insta la acción:",
            "¿Aporta documentación en este acto?",
            "¿Aporta efectos en este acto?",
        )
        self.cortes_inv = (
            "INVOLUCRADO - TESTIGO DATOS",
            "INVOLUCRADO - SOSPECHOSO DATOS",
            "INVOLUCRADO - VICTIMA DATOS",
            "INVOLUCRADO - APREHENDIDO DATOS",
            "INVOLUCRADO - TESTIGO DEL PROCEDIMIENTO DATOS",
            "INVOLUCRADO - REPRESENTANTE DATOS",
            "INVOLUCRADO - PERSONA DE CONFIANZA DATOS",
            "DENUNCIANTE DATOS",
            "INVOLUCRADO - DENUNCIADO DATOS",
        )
        self.cortes_efectos = (
            "AUTOMOTORES Marca",
            "ARMA/S Tipo",
            "ELEMENTOS SECUESTRADOS Tipo",
            "OTROS OBJETOS Tipo",
        )

    def cargar(self):
        data = pd.read_excel(rf"{self.path}\fd.xlsx")
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
        ult.to_excel(rf"{self.path}\ult.xlsx")

    def posiciones(self):
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
                try:
                    item.remove(-1)
                except:
                    pass
                posiciones.append(item)
        return posiciones

    def posiciones_datos(self, cortes, quitar=False):
        posiciones = []
        archivo = self.cargar()
        listo = self.formatear(archivo)
        for i in listo:
            item = []
            for j in cortes:
                item.append(i.find(j))
            if quitar is True:
                for i in range(0, len(item)):
                    try:
                        item.remove(-1)
                    except:
                        pass
            posiciones.append(item)
        posiciones.append(item)
        return posiciones
