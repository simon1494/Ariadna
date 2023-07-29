import view
import tkinter as tk


if __name__ == "__main__":
    version = "3.0.0-beta [2023-07-28]"
    master = tk.Tk()
    app = view.Ventana_Principal(master, version)
    app.iniciar()
