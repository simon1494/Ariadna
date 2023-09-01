import sys

sys.path.append("../ariadna")
from modelos.gestores_de_informacion.mensajeador import Mensajeador
from modelos.gestores_de_archivos.administrador import Administrador

class VentanaBase(Mensajeador, Administrador):
    usuario = None
    color_botones = "#D0F2EF"
    botones_iniciales = "#F2F2F2"
    botones_segmentado = "#F2F2F2"
    botones_subir = "#F2F2F2"
    amarillo = "#EBDD04"
    rojo = "#EA3830"
    verde = "#27EA00"
    color_back = "#2493BF"

    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y-100}"

