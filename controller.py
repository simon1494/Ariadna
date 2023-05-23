import model
from tkinter import filedialog
import checkpoints as ck


if __name__ == "__main__":
    #::::::::::::::::::::::::procesado inicial:::::::::::::::::::::::::::
    formateador = model.Formateador()
    archivo = model.Administrador._cargar(filedialog.askopenfilename())
    tester = model.Tester(archivo)
    if len(tester.errores) > 0:
        model.Administrador._convertir_inicial(
            tester.errores,
            ["n° registro", "errores"],
            error=True,
        )
        print("Hubo errores en los listados.\nSe ha generado un registro errores.")

    else:
        archivo, identificadores = formateador._formatear(archivo, ck.cp_iden)
        inicial = model.Inicial(archivo, identificadores)
        path_inicial = model.Administrador._convertir_inicial(
            inicial.sin_duplicados, ck.general
        )
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    #::::::::::::::::::::::::procesado final:::::::::::::::::::::::::::::
    try:
        archivo1 = model.Administrador._cargar(
            filedialog.askopenfilename(), no_tiene_encabezados=False
        )
        segmentado = model.Segmentado(archivo1)
        model.Administrador._convertir_segmentado(segmentado.final)
    except Exception as error:
        print(error)
