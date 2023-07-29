import view
import tkinter as tk


if __name__ == "__main__":
    version = "3.0.1-beta [2023-07-29]"
    master = tk.Tk()
    app = view.Ventana_Principal(master, version)
    app.iniciar()
