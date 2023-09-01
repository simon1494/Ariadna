import sys

sys.path.append("../ariadna")
import copy
import os
import settings as ck
import pandas as pd
from modelos.motores.motor_segmentado import MotorSegmentado
from modelos.motores.motor_calificaciones import MotorCalificaciones

DIRECTORIO_PADRE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


class Segmentado(MotorSegmentado, MotorCalificaciones):
    def __init__(self, archivo, indices, carpeta=False):
        # enlaza con la base de calificaciones actual y lo almanece en forma de diccionario
        self.base_calificaciones = dict(
            pd.read_excel(
                rf"{DIRECTORIO_PADRE}\Base calificaciones\calificaciones_db.xlsx",
                header=None,
            ).values.tolist()
        )
        # preparación e indexado del archivo inicial
        self.segmentados = archivo
        self.indexados = self._indexador(self.segmentados, indices[0])
        # indexado de entidades simples)
        self.calificaciones = list(
            map(
                lambda x: x.replace("CALIFICACIÓN LEGAL DEL HECHO ", ""),
                self._armar_paquete(self.indexados, 26),
            )
        )

        self.armas = self._armar_paquete(self.indexados, 43)
        self.objetos = self._armar_paquete(self.indexados, 45)
        self.secuestros = self._armar_paquete(self.indexados, 44)
        self.automotores = self._armar_paquete(self.indexados, 42)

        # indexado de involucrados
        self.testigos_procedimiento = self._armar_paquete(self.indexados, 34)
        self.testigos_presenciales = self._armar_paquete(self.indexados, 29)  #
        self.victimas = self._armar_paquete(self.indexados, 31)  #
        self.personas_confianza = self._armar_paquete(self.indexados, 36)
        self.aprehendidos = self._armar_paquete(self.indexados, 32)  #
        self.sospechosos = self._armar_paquete(self.indexados, 30)  #
        self.denunciados = self._armar_paquete(self.indexados, 38)
        self.denunciante = self._armar_paquete(self.indexados, 37)
        self.representante = self._armar_paquete(self.indexados, 35)
        self.profugos = self._armar_paquete(self.indexados, 33)
        self.involucrados = [
            self.testigos_procedimiento,
            self.testigos_presenciales,
            self.victimas,
            self.personas_confianza,
            self.aprehendidos,
            self.sospechosos,
            self.denunciados,
            self.denunciante,
            self.representante,
            self.profugos,
        ]

        # segmentado de entidades simples
        self._automotores = self._descomponer(
            self.automotores, ck.general_automotores, indices[3]
        )
        self._armas = self._descomponer(self.armas, ck.general_armas, indices[2])
        self._objetos = self._descomponer(
            self.objetos, ck.general_elementos, indices[4]
        )
        self._secuestros = self._descomponer(
            self.secuestros, ck.general_elementos, indices[5]
        )
        self._calificaciones = self._descomponer(
            self.calificaciones, ck.general_calificaciones, indices[1]
        )
        self._calificaciones_chequeadas = list(
            map(
                lambda registro: self.rearmar_calificacion(
                    registro, self.base_calificaciones, son_registros=False
                ),
                copy.deepcopy(self._calificaciones),
            )
        )
        self.errores = self.identificar_errores(
            self._calificaciones, self._calificaciones_chequeadas
        )
        if not len(self.errores):
            self.indexados = list(
                map(
                    lambda registro: self.rearmar_calificacion(
                        registro, self.base_calificaciones
                    ),
                    self.indexados,
                )
            )
            self.datos = self._recortar(self.indexados)
            # segmentado y consolidación de todos los involucrados
            self._involucrados = self._todos_los_involucrados(
                self.involucrados, indices[6], limpiar=True
            )

            self._involucrados = list(
                map(
                    lambda lista: self._formatear_fecha(lista, inicial=False),
                    self._involucrados,
                )  # da el formato correcto a las columnas "fecha_nacimiento" en todos los involucrados
            )

            # limpieza de campos "Sin especificar".
            if not carpeta:
                self.datos = list(map(lambda x: self._limpiar_registro(x), self.datos))
                self._automotores = list(
                    map(lambda x: self._limpiar_registro(x), self._automotores)
                )
                self._armas = list(
                    map(lambda x: self._limpiar_registro(x), self._armas)
                )
                self._objetos = list(
                    map(lambda x: self._limpiar_registro(x), self._objetos)
                )
                self._secuestros = list(
                    map(lambda x: self._limpiar_registro(x), self._secuestros)
                )
                self._involucrados = list(
                    map(lambda x: self._limpiar_registro(x), self._involucrados)
                )

            # archivo final segmentado
            self.final = [
                self.datos,
                self._calificaciones,
                self._armas,
                self._automotores,
                self._objetos,
                self._secuestros,
                self._involucrados,
            ]
        else:
            self.mostrar_mensaje_info(
                "Se detectaron calificaciones no existentes en base."
            )

    def _indexador(self, archivo, index):
        nuevo = []
        for item in archivo:
            nw_item = item.copy()
            nw_item.insert(0, index)
            nuevo.append(nw_item)
            index += 1
        return nuevo

    def _recortar(self, lista):
        a_eliminar = sorted(
            [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 42, 43, 44, 45], reverse=True
        )
        for sub in lista:
            for j in a_eliminar:
                del sub[j]
        return lista
