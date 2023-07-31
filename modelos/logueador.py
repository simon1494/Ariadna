import logging


class Logueador:
    def __init__(self, archivo):
        self.archivo = archivo
        logging.basicConfig(
            filename=archivo, level="DEBUG", format="%(asctime)s - %(message)s"
        )

    def loguear_info(self, info_a_agregar):
        logging.info(info_a_agregar)

    def loguear_warning(self, advertencia_a_agregar):
        logging.warning(advertencia_a_agregar)

    def loguear_error(self, error_a_agregar):
        logging.warning(error_a_agregar)

    def loguear_critical(self, critico_a_agregar):
        logging.warning(critico_a_agregar)
