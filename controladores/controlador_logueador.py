import sys

sys.path.append("../ariadna")
import os
import datetime
from modelos.logueador import Logueador


def iniciar_logueador():
    CARPETA_DE_LOGS = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../Exportaciones/Logs")
    )
    NOMBRE_ARCHIVO = (
        f'{CARPETA_DE_LOGS}/{datetime.datetime.now().strftime("%Y-%m-%d    %H.%M")}.log'
    )

    logger = Logueador(NOMBRE_ARCHIVO)
    return logger
