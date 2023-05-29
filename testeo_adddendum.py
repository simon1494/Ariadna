import pandas as pd
from pathlib import Path as Ph


def rearmar_calificacion(calificacion, base):
    if calificacion.find("tipificación"):
        resultado = calificacion.split("CALIFICACIÓN LEGAL DEL HECHO Tipificación: ")
    else:
        resultado = calificacion.split("CALIFICACIÓN LEGAL DEL HECHO Delito: ")
    del resultado[0]
    resultado = list(map(lambda item: item.strip(), resultado))
    for i in resultado:
        print(i)
    cotejar_todas(resultado, base)
    final = "; ".join(resultado)
    return final


def simplificada(calificacion):
    print(calificacion)
    calificacion3 = calificacion.replace("Consumado: Si", "")
    calificacion4 = calificacion3.replace("Consumado: No", "")
    calificacion0 = calificacion4.replace(" ", "")
    calificacion1 = calificacion0.replace("-", "")
    calificacion2 = calificacion1.replace(".", "")
    return calificacion2


def cotejar_una(calificacion, data):
    a_cotejar = simplificada(calificacion)
    if a_cotejar in data:
        resultado = data[a_cotejar]
        return resultado
    else:
        return "error"


def cotejar_todas(elementos, data):
    final = list(map(lambda item: cotejar_una(item, data), elementos))
    return print(final)


texto = "CALIFICACIÓN LEGAL DEL HECHO Tipificación: Abso sexual - Art.119 párr. 1ro Consumado: Si CALIFICACIÓN LEGAL DEL HECHO Tipificación: Resistencia a la autoridad - Art.239 Consumado: Si CALIFICACIÓN LEGAL DEL HECHO Tipificación: Atentado contra la autoridad - Art.237 Consumado: Si CALIFICACIÓN LEGAL DEL HECHO Tipificación: Lesiones leves - Art.89 Consumado: Si"

base = pd.read_excel(
    rf"{Ph(__file__).resolve().parent}\Base calificaciones\calificaciones_db.xlsx",
    header=None,
)
data = base.values.tolist()
data = dict(data)

rearmar_calificacion(texto, data)
