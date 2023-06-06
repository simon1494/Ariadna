import tkinter as tk
import model
from tkinter import filedialog
from tkinter import ttk
import checkpoints as ck
import pandas as pd
from pathlib import Path as Ph
from model import Addendum


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

        boton_errores = tk.Button(
            self.ventana,
            text="ERRORES",
            bg="light green",
            fg="black",
            font=("Palatino Linotype", 11),
            command=lambda: self.abrir_ventana_errores(),
        )
        boton_errores.place(
            x=500,
            y=210,
            width=80,
            height=20,
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
                    ["indice", "n° registro", "errores"],
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
                segmentado = model.Segmentado(archivo1)
            else:
                archivo1 = model.Administrador._cargar(path, no_tiene_encabezados=False)
                segmentado = model.Segmentado(archivo1)
            try:
                model.Administrador._convertir_segmentado(segmentado.final)
            except AttributeError:
                tk.messagebox.showinfo(
                    "Advertencia", f"El proceso de segmentado se ha abortado."
                )
                ventana_errores = VentanaErrores(segmentado.errores)
                self.ventana.wait_window(ventana_errores)
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

    def abrir_ventana_errores(self):
        ventana_errores = VentanaErrores()


class VentanaErrores(tk.Toplevel):
    def __init__(self, archivo=[]):
        super().__init__()
        self.title("Ventana de Ejemplo")
        self.geometry("400x300")
        self.registros = archivo

        self.crear_widgets()
        self.correr()

    def crear_widgets(self):
        # Crear treeview con 3 columnas
        self.control_entry = tk.StringVar()
        self.control_entry.set("")

        self.treeview = ttk.Treeview(self, columns=("id", "id_hecho", "calificacion"))

        # Configurar headers de las columnas
        self.treeview.heading("id", text="ID")
        self.treeview.heading("id_hecho", text="ID Hecho")
        self.treeview.heading("calificacion", text="Calificación")
        self.treeview.column("#0", minwidth=0, width=0, anchor="center")
        self.treeview.column("id", minwidth=0, width=30, anchor="center")
        self.treeview.column("id_hecho", minwidth=0, width=70, anchor="center")
        self.treeview.column("calificacion", minwidth=0, width=290, anchor="center")

        # Agregar datos al treeview (ejemplo)
        for registro in self.registros:
            self.treeview.insert(
                "", "end", values=(registro[0], registro[1], registro[2])
            )

        self.treeview.bind(
            "<ButtonRelease-1>",
            lambda evento: self.seleccionar_item(self.treeview, self.control_entry),
        )
        self.treeview.pack()

        # Crear entry con label "seleccionado" al lado izquierdo
        self.entry_frame = ttk.Frame(self)
        self.entry_frame = ttk.Entry(self, textvariable=self.control_entry)
        self.entry_frame.pack()

        # Crear botón "Agregar a base"
        self.agregar_boton = ttk.Button(
            self,
            text="Agregar a base",
            command=lambda: self.agregar_a_base(self.entry_frame.get()),
        )
        self.agregar_boton.pack(pady=10)

    def seleccionar_item(self, tree, entry):
        item_ = tree.focus()
        datos_registro = tree.item(item_)["values"][2]
        entry.set(datos_registro)

    def agregar_a_base(self, valor):
        # Lógica para agregar los datos a la base de datos
        # Leer el archivo Excel
        df = dict(
            pd.read_excel(
                rf"{Ph(__file__).resolve().parent}\Base calificaciones\calificaciones_db.xlsx",
                header=None,
            ).values.tolist()
        )
        addendum = Addendum()
        simplificado = addendum.simplificada(valor)

        # Agregar un nuevo registro
        df[simplificado] = valor

        # convierto el dic en df
        df = list(df.items())
        df = pd.DataFrame(df)

        # Guardar los cambios en el archivo Excel
        df.to_excel(
            rf"{Ph(__file__).resolve().parent}\Base calificaciones\calificaciones_db.xlsx",
            index=False,
        )
        tk.messagebox.showinfo(
            "Alta",
            f"Se ha agregado la nueva carátula a la base de datos de calificaciones.",
        )

    def correr(self):
        self.mainloop()
