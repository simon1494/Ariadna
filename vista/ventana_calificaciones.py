import sys

sys.path.append("../ariadna")
import pandas as pd
import tkinter as tk
from tkinter import ttk
from .ventana_base import VentanaBase
from modelos.motores.motor_calificaciones import MotorCalificaciones


class VentanaCalificaciones(tk.Toplevel, VentanaBase):
    def __init__(
        self,
        ventana,
        archivo=[],
    ):
        super().__init__(ventana)
        self.title("Módulo Addendum")
        self.ancho = 400
        self.alto = 300
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.registros = archivo
        self.original = ""
        self.crear_widgets()

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
        if len(self.registros) > 0:
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
            command=lambda: self.agregar_a_base(self.entry_frame, self.original),
        )
        self.agregar_boton.pack(pady=10)

    def seleccionar_item(self, tree, entry):
        try:
            item_ = tree.focus()
            datos_registro = tree.item(item_)["values"][2]
            entry.set(datos_registro)
            self.original = datos_registro
        except Exception:
            ...

    def agregar_a_base(self, entry, original):
        # Lógica para agregar los datos a la base de datos
        # Leer el archivo Excel
        df = dict(
            pd.read_excel(
                rf"{self.DIRECTORIO_PADRE}\Base calificaciones\calificaciones_db.xlsx",
                header=None,
            ).values.tolist()
        )
        motor_calificaciones = MotorCalificaciones()
        simplificado = motor_calificaciones.simplificada(original)

        # Agregar un nuevo registro
        df[simplificado] = entry.get()

        # convierto el dic en df
        df = list(df.items())
        df = pd.DataFrame(df)

        # Guardar los cambios en el archivo Excel
        df.to_excel(
            rf"{self.DIRECTORIO_PADRE}\Base calificaciones\calificaciones_db.xlsx",
            index=False,
            header=False,
        )
        self.mostrar_mensaje_info(
            "Se ha agregado la nueva carátula a la base de datos de calificaciones.",
        )
