import sys

sys.path.append("../ariadna")
from vista import view
import tkinter as tk


class Aplicacion:
    def __init__(self, version):
        self.version = version
        master = tk.Tk()
        app = view.Ventana_Principal(master, self.version)
        app.iniciar()
