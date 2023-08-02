import sys

sys.path.append("../ariadna")
from vista import view
import tkinter as tk


class Aplicacion:
    def __init__(self, version, usuario):
        self.usuario = usuario
        self.version = version
        master = tk.Tk()
        app = view.Ventana_Principal(master, self.version, self.usuario)
        app.iniciar()
