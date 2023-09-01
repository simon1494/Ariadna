import sys

sys.path.append("../ariadna")
import os
import pandas as pd
import tkinter as tk
from .ventana_base import VentanaBase


class VentanaErrores(tk.Toplevel, VentanaBase):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.title("Módulo errores")
        self.ancho = 720
        self.alto = 200
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.corregido = None
        self.config(bg=self.color_back)
        self.crear_botones()

    def crear_botones(self):
        estilo_fuente = ("Palatino Linotype", 14)
        alto = 50
        ancho = 150
        separacion = 85
        y_pos = (self.alto / 2) - (alto / 2)
        x_pos = 50
        self.boton_original = tk.Button(
            self,
            text="Original",
            bg=self.rojo,
            width=10,
            font=estilo_fuente,
            command=lambda: self.cargar_original(),
        )
        self.boton_original.place(
            x=x_pos,
            y=y_pos,
            width=ancho,
            height=alto,
        )

        self.boton_enmendado = tk.Button(
            self,
            text="Enmendado",
            bg="#EA3830",
            width=10,
            font=estilo_fuente,
            command=lambda: self.cargar_enmendado(),
        )
        self.boton_enmendado.place(
            x=x_pos + (separacion + ancho) * 2,
            y=y_pos,
            width=ancho,
            height=alto,
        )

        self.boton_corregir = tk.Button(
            self,
            text="Corregir Original",
            font=estilo_fuente,
            bg=self.amarillo,
            command=lambda: self.corregir_original(),
        )
        self.boton_corregir.place(
            x=x_pos + (separacion + ancho),
            y=y_pos,
            width=ancho,
            height=alto,
        )

    def corregir_original(self):
        try:
            original = self._cargar(
                self.path_original,
            )
            enmendado = self._cargar(
                self.path_enmendado, no_tiene_encabezados=False, es_original=False
            )

            for error in enmendado:
                original[int(error[0])][0] = error[2]

            nombre_archivo = os.path.splitext(os.path.basename(self.path_original))[0]
            ult = pd.DataFrame(original)
            ult.to_excel(
                rf"{self.DIRECTORIO_PADRE}\Exportaciones\Corregidos\{nombre_archivo} (corregido).xlsx",
                index=False,
                header=False,
            )
            self.boton_corregir.config(bg="#27EA00")
            self.mostrar_mensaje_info("¡El archivo fue corredido correctamente!")
            return rf"{self.DIRECTORIO_PADRE}\Exportaciones\Corregidos\{nombre_archivo} (corregido).xlsx"
        except Exception as error:
            self.mostrar_mensaje_advertencia(
                f"Ha ocurrido el siguiente error:\n {error}"
            )

    def cargar_original(self):
        path = self.seleccionar_archivo("/Exportaciones/Crudos/")
        if path:
            self.path_original = path
            self.boton_original.config(bg=self.verde)
        else:
            self.mostrar_mensaje_advertencia("No se ha seleccionado ningún archivo.")

    def cargar_enmendado(self):
        path = self.seleccionar_archivo("/Exportaciones/Errores/")
        if path:
            self.path_enmendado = path
            self.boton_enmendado.config(bg="#27EA00")
        else:
            self.mostrar_mensaje_advertencia("No se ha seleccionado ningún archivo.")
