import sys

sys.path.append("../ariadna")
import copy
import re
import os
import checkpoints as ck
import pandas as pd
from .procesadores_secundarios import Addendum
from .motores import Core_Inicial
from .motores import Core_Final


# Obtener la ruta del directorio padre del archivo actual (tu_proyecto)
DIRECTORIO_PADRE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Inicial(Core_Inicial):
    def __init__(self, archivo, identificadores):
        # checkpoints
        self._checkpoints = ck.cp_iniciales
        self._ident = ck.cp_iden
        self._cortes_datos = ck.cp_datos
        self._cortes_inv = ck.cp_inv
        self._cortes_efectos = ck.efectos_combinado
        self._encabezados = ck.encabezados
        self._general = ck.general

        # preparación y formateado de pasos iniciales
        self.formateado, self.identificadores = archivo, identificadores
        self.particiones = self._barrer_inicial(self.formateado, self._checkpoints)

        # procesamiento de campos iniciales
        self.datos_inv = self._todos(self.particiones, self._cortes_inv, 0)
        self.datos_efectos = self._efectos(self.particiones, self._cortes_efectos)
        self.datos_hecho = self._descomponer(self.particiones, self._cortes_datos, 1)
        self.datos_hecho = list(
            map(
                lambda item: {
                    **item,
                    "CALIFICACIÓN LEGAL DEL HECHO ": "CALIFICACIÓN LEGAL DEL HECHO "
                    + item["CALIFICACIÓN LEGAL DEL HECHO "],
                },
                self.datos_hecho,
            )
        )
        self.datos_hecho = list(
            map(
                lambda item: {
                    **item,
                    " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada": item[
                        " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada"
                    ].replace(
                        ": ", ""
                    ),
                },
                self.datos_hecho,
            )
        )

        # unificado de campos iniciales
        self.procesados = self._unificar(
            self.identificadores,
            self.datos_hecho,
            self.datos_inv,
            self.datos_efectos,
            self.particiones,
            self._general,
        )
        self.sin_duplicados = self._borrar_duplicados(self.procesados)

        self.sin_duplicados = list(
            map(
                lambda lista: self._formatear_fecha(lista), self.sin_duplicados
            )  # da el formato correcto a las columnas "fecha_carga","fecha_inicio_hecho" y "fecha_final_hecho"
        )
        self.sin_duplicados = list(
            map(lambda registro: self.limpiar_relato(registro), self.sin_duplicados)
        )

    def _barrer_inicial(self, listado, cortes):
        b = []
        for i in listado:
            if i.find(cortes[0][0]) == 0:
                x = self._segmentador(
                    i,
                    self._posiciones_datos(i, cortes[0]),
                    cortes[0],
                )
                b.append(x)
            else:
                x = self._segmentador(
                    i,
                    self._posiciones_datos(i, cortes[1]),
                    cortes[1],
                )
                b.append(x)
        return self._recuperar_values(b)

    def _unificar(self, identificadores, hechos, involucrados, efectos, relatos, canon):
        unificada = []
        for i in range(0, len(hechos)):
            item = canon.copy()
            for key in hechos[i].keys():
                if key in item:
                    item[key] = hechos[i][key].strip()
            if item[" Descripción:"] == "":
                try:
                    item[" Descripción:"] = hechos[i][" Descripcion:"]
                except Exception as error:
                    self.imprimir_con_color(
                        f"Error en la 'Descripcion' del index {i}: {error}", "amarillo"
                    )
            for key in involucrados[i].keys():
                if key in item:
                    item[key] = involucrados[i][key].strip()
            for key in efectos[i].keys():
                if key in item:
                    item[key] = efectos[i][key].strip()
            for key in identificadores[i].keys():
                if key in item:
                    item[key] = identificadores[i][key].strip()
            item[" Relato: "] = relatos[i][2].strip()
            unificada.append(item.copy())
        return self._recuperar_values(unificada)

    @staticmethod
    def limpiar_relato(registro):
        registro_nuevo = copy.deepcopy(registro)
        texto = registro[38]
        regex1 = r"(Relato del procedimiento ).*RELATO DEL PROCEDIMIENTO: "
        regex2 = r"Relato del hecho RELATO DEL HECHO: "
        texto = re.sub(regex1, "", texto)
        texto = re.sub(regex2, "", texto)
        registro_nuevo[38] = texto
        return registro_nuevo

    def _borrar_duplicados(self, archivo):
        lista = archivo.copy()
        lista_nros = []
        duplicados = []
        contador2 = 0

        for i in range(0, len(lista)):
            lista_nros.append(lista[i][0])

        for i in range(0, len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i][0] == lista[j][0]:
                    duplicados.append(lista[j][0])

        duplicados = list(set(duplicados))

        if len(duplicados) > 0:
            for item in duplicados:
                contador = 0
                for i in lista:
                    if i[0] == item:
                        contador += 1
                while contador > 1:
                    for z in range(0, len(lista)):
                        if lista[z][0] == item:
                            del lista[z]
                            contador -= 1
                            contador2 += 1
                            break
            if len(duplicados) > 0:
                print("\n")
                self.imprimir_con_color(
                    f"Se han eliminado {contador2} duplicados.", "blanco"
                )
        return lista


class Segmentado(Core_Final, Addendum):
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
