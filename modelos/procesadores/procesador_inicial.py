import sys

sys.path.append("../ariadna")
import copy
import re
import settings as ck
from modelos.motores.motor_inicial import MotorInicial


class Inicial(MotorInicial):
    def __init__(
        self,
        archivo,
        identificadores,
    ):
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
