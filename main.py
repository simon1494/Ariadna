import suba
import pandas as pd
import re


def clean_regexs(text):
    regexp = r"(Nº de Denuncia: | N° de Acta de Procedimiento: )..................................................(FORMULARIO DE DECLARACIÓN |ACTA DE PROCEDIMIENTO ).......................................................................\d+(/)\d+"
    return re.sub(regexp, "", text)


def oulala(lista, texto2):
    a = []
    for i in range(0, len(lista)):
        if texto2.find(lista[i]) != -1:
            if i < len(lista) - 1:
                new_text = texto2[
                    texto2.find(lista[i]) + len(lista[i]) : texto2.find(lista[i + 1])
                ]
                a.append(new_text)
            else:
                new_text = texto2[texto2.find(lista[i]) + len(lista[i]) :]
                a.append(new_text)
        else:
            a.append("")
    return a


def imprimir(res):
    for i in range(0, len(res)):
        print(res[i] + "\n\n\n")


def formatear(lista):
    final = []
    for i in lista:
        texto = i[0]
        texto2 = texto.replace("\n", " ")
        texto2 = texto2.replace("  ", " ")
        texto2 = clean_regexs(texto2)
        final.append(texto2)
    return final


def barrer(lista, cortes):
    b = []
    for i in lista:
        if i.find(cortes[0][0]) == 0:
            x = oulala(cortes[0], i)
            b.append(x)
        else:
            x = oulala(cortes[1], i)
            b.append(x)
    return b


checkpoints = (
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
cortes = (
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


def convertir(checkpoints):

    archivo = suba.cargar_fd()
    listo = formatear(archivo)
    asdf = barrer(listo, checkpoints)
    ult = pd.DataFrame(asdf, columns=["paso1", "paso2", "paso3", "paso4", "paso5"])
    ult.to_excel(r"C:\Users\Simon\Documents\GitHub\minos\ult_fd.xlsx")


convertir(checkpoints)
