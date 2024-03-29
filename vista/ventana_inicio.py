import sys

sys.path.append("../ariadna")
import tkinter as tk
from PIL import Image, ImageTk
from vista.ventana_base import VentanaBase


class VentanaInicio(VentanaBase):
    def __init__(
        self,
        display_time=5000,
    ):
        self.image_path = "media\Ariadna1.jpg"
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
