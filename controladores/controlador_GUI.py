import sys

sys.path.append("../ariadna")
from vista.ventana_principal import VentanaPrincipal
import tkinter as tk


class Aplicacion:
    def __init__(self, version, usuario):
        self.usuario = usuario
        self.version = version
        master = tk.Tk()
        app = VentanaPrincipal(master, self.version, self.usuario)
        app.iniciar()
