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
        self.image_path = "C:/Users/simon/Documents/Ariadna1.jpg"
        self.width = 504
        self.height = 316
        self.display_time = display_time
        self.root = tk.Tk()
        self.root.geometry(self.centrar_ventana(self.root, self.width, self.height))

    def show_image(self):
        # Carga la imagen usando PIL
        image = Image.open(self.image_path)
        image = image.resize((self.width, self.height))
        photo = ImageTk.PhotoImage(image)

        # Crea un widget Label y configúralo para mostrar la imagen
        label = tk.Label(self.root, image=photo)
        label.pack()

        # Cierra la ventana después de un tiempo definido (en milisegundos)
        threading.Timer(5, self.create_b).start()

        self.root.mainloop()

    def create_b(self):
        self.destroy()
        obj_a = VentanaLogueo(VER)


if __name__ == "__main__":
    image_viewer = LogoInicio()
    image_viewer.show_image()
