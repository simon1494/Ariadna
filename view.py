import tkinter as tk
import model
from tkinter import filedialog
import checkpoints as ck


class VentanaBotones:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ventana con botones")
        self.ancho = 600
        self.alto = 250
        self.ventana.geometry(self.centrar_ventana(self.ventana, self.ancho, self.alto))
        self.ventana.configure(bg="dark gray")
        self.crear_botones()

    def crear_botones(self):
        x_pos = int(self.ancho / 2)
        y_pos = int(self.alto / 2)
        estilo_fuente = ("Palatino Linotype", 16)
        b_alto = 75
        b_ancho = 200

        separacion = 120

        boton_inicial = tk.Button(
            self.ventana,
            text="INICIAL",
            bg="light green",
            fg="black",
            font=estilo_fuente,
            command=lambda: self.procesar_inicial(),
        )
        boton_inicial.place(
            x=x_pos - separacion - (b_ancho / 2),
            y=y_pos - (b_alto / 2),
            width=b_ancho,
            height=b_alto,
        )

        boton_segmentado = tk.Button(
            self.ventana,
            text="SEGMENTADO",
            bg="light green",
            fg="black",
            font=estilo_fuente,
            command=lambda: self.procesar_final(),
        )
        boton_segmentado.place(
            x=x_pos + separacion - (b_ancho / 2),
            y=y_pos - (b_alto / 2),
            width=b_ancho,
            height=b_alto,
        )

    def iniciar(self):
        self.ventana.mainloop()

    def procesar_inicial(self):
        #::::::::::::::::::::::::procesado inicial:::::::::::::::::::::::::::
        try:
            formateador = model.Formateador()
            archivo = model.Administrador._cargar(filedialog.askopenfilename())
            tester = model.Tester(archivo)
            if len(tester.errores) > 0:
                model.Administrador._convertir_inicial(
                    tester.errores,
                    ["n° registro", "errores"],
                    error=True,
                )
                print(
                    "Hubo errores en los listados.\nSe ha generado un registro errores."
                )

            else:
                archivo, identificadores = formateador._formatear(archivo, ck.cp_iden)
                inicial = model.Inicial(archivo, identificadores)
                path = model.Administrador._convertir_inicial(
                    inicial.sin_duplicados, ck.general
                )
                if tk.messagebox.askyesno(
                    "Segmentar", "¿Desea proceder a segmentar el archivo?"
                ):
                    self.procesar_final(path)
        except FileNotFoundError:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ningún archivo."
            )

        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def procesar_final(self, path=False):
        try:
            if path is False:
                archivo1 = model.Administrador._cargar(
                    filedialog.askopenfilename(), no_tiene_encabezados=False
                )
            else:
                archivo1 = model.Administrador._cargar(path, no_tiene_encabezados=False)
            segmentado = model.Segmentado(archivo1)
            model.Administrador._convertir_segmentado(segmentado.final)

        except FileNotFoundError:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ningún archivo."
            )

    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y-100}"
