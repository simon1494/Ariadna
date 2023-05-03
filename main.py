import suba


def oulala(lista, texto2):
    a = []
    for i in range(0, len(lista)):
        if i < len(lista) - 1:
            new_text = texto2[
                texto2.find(lista[i]) + len(lista[i]) : texto2.find(lista[i + 1])
            ]
            a.append(new_text)
        else:
            new_text = texto2[texto2.find(lista[i]) + len(lista[i]) :]
            a.append(new_text)
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
        final.append(texto2)
    return final


def barrer(lista, cortes, cortes2):
    b = []
    for i in lista:
        x = oulala(cortes, i)
        y = oulala(cortes2, x[1])
        b.append(y)
    return b


checkpoints = (
    "Paso 1 - Declaración Testimonial ",
    "Paso 2 - Declaración Testimonial ",
    "Paso 3 - Declaración Testimonial ",
    "Paso 4 - Declaración Testimonial ",
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


archivo = suba.cargar()
listo = formatear(archivo)
asdf = barrer(listo, checkpoints, cortes)

for i in asdf:
    print(len(i[15]))


# b = oulala(cortes, a[1])
# imprimir(a)
# imprimir(b)
