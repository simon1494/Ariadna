import sys

sys.path.append("../ariadna")
import copy
import tkinter as tk
from .ventana_base import VentanaBase


class VentanaIntermedia(tk.Toplevel, VentanaBase):
    def __init__(self, ventana_principal, widgets, titulo, color_botones):
        super().__init__(ventana_principal)
        self.widgets = widgets
        self.title(titulo)
        self.ancho = 400
        self.alto = 450
        self.geometry(self.centrar_ventana(ventana_principal, self.ancho, self.alto))
        self.configure(bg=self.color_back)
        self.crear_widgets(widgets, color_botones)

    def crear_widgets(self, wid, colores):
        widgets = copy.deepcopy(wid)
        color_botones = colores
        widgets.append(
            {
                "nombre": "volver",
                "texto": "Volver al menú",
                "callback": lambda: self.volver_a_principal(),
            }
        )

        estilo_fuente = ("Palatino Linotype", 16)
        b_alto = 50
        b_ancho = 250

        separacion = b_alto * 1.8
        x_pos = int(self.ancho / 2) - int(b_ancho / 2)
        y_pos = (self.alto / 2) - (
            ((b_alto * len(widgets)) + (separacion * (len(widgets) - 1))) / 1.5
        ) / 2

        self.botones = []

        for widget in widgets:
            widget["nombre"] = tk.Button(
                self,
                text=widget["texto"],
                bg=color_botones,
                fg="black",
                font=estilo_fuente,
                command=widget["callback"],
            )
            widget["nombre"].place(
                x=x_pos,
                y=y_pos,
                width=b_ancho,
                height=b_alto,
            )

            self.botones.append(widget["nombre"])

            y_pos += separacion

    def volver_a_principal(self):
        self.winfo_toplevel().deiconify()
        self.destroy()
