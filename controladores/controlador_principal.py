import sys

sys.path.append("../ariadna")
from vista import view
import tkinter as tk

version = "3.0.1-beta [2023-07-29]"
master = tk.Tk()
app = view.Ventana_Principal(master, version)
app.iniciar()
