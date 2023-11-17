import logging
import colorama
import os
import datetime


class Logueador:
    colorama.init(convert=True)
    CARPETA_DEL_ARCHIVO_LOGS = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
    ARCHIVO_LOGS = f"{CARPETA_DEL_ARCHIVO_LOGS}/Exportaciones/Logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

    try:
        logging.basicConfig(
            filename=ARCHIVO_LOGS,
            level=logging.DEBUG,
            format="%(asctime)s:   %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
    except FileNotFoundError as error:
        print(error)

    @classmethod
    def loguear_info(cls, info_a_agregar):
        logging.info(info_a_agregar)

    @classmethod
    def loguear_warning(cls, advertencia_a_agregar):
        logging.warning(advertencia_a_agregar)

    @classmethod
    def loguear_error(cls, error_a_agregar):
        logging.warning(error_a_agregar)

    @classmethod
    def loguear_critical(cls, critico_a_agregar):
        logging.warning(critico_a_agregar)

    def imprimir_con_color(self, mensaje, color="normal", loguear=True):
        if color == "normal":
            print(
                colorama.Back.WHITE
                + colorama.Fore.BLACK
                + mensaje
                + colorama.Style.RESET_ALL
            )
        elif color == "azul":
            print(colorama.Back.BLUE + mensaje + colorama.Style.RESET_ALL)
            if loguear:
                self.loguear_info(mensaje)
        elif color == "blanco":
            print(
                colorama.Back.WHITE
                + colorama.Fore.BLACK
                + mensaje
                + colorama.Style.RESET_ALL
            )
            if loguear:
                self.loguear_info(mensaje)
        elif color == "lila":
            print(colorama.Back.MAGENTA + mensaje + colorama.Style.RESET_ALL)
            if loguear:
                self.loguear_info(mensaje)
        elif color == "verde":
            print(colorama.Back.GREEN + mensaje + colorama.Style.RESET_ALL)
            if loguear:
                self.loguear_info(mensaje)
        elif color == "amarillo":
            print(colorama.Back.YELLOW + mensaje + colorama.Style.RESET_ALL)
            if loguear:
                self.loguear_warning(mensaje)
        elif color == "rojo":
            print(colorama.Back.RED + mensaje + colorama.Style.RESET_ALL)
            if loguear:
                self.loguear_critical(mensaje)
