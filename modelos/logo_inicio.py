import sys

sys.path.append("../ariadna")
import tkinter as tk
from PIL import Image, ImageTk
from vista.view import Ventana_Base
from modelos.registro_de_usuario import VentanaLogueo
import threading

VER = "4.2.2-beta [2023-03-08]"


class LogoInicio(Ventana_Base):
    def __init__(
        self,
        display_time=5000,
    ):
        self.image_path = "Ariadna1.jpg"
        self.width = 504
        self.height = 316
        self.display_time = display_time
        self.root = tk.Tk()
        self.root.title("")
        self.root.protocol("WM_DELETE_WINDOW", self.hacer_nada)
        self.root.geometry(self.centrar_ventana(self.root, self.width, self.height))

    def show_image(self):
        # Carga la imagen usando PIL
        image = Image.open(self.image_path)
        image = image.resize((self.width, self.height))
        photo = ImageTk.PhotoImage(image)

        # Crea un widget Label y configúralo para mostrar la imagen
        label = tk.Label(self.root, image=photo)
        label.pack()
        self.root.after(6000, self.root.destroy)
        self.root.mainloop()

    def hacer_nada(self):
        ...
