import sys

sys.path.append("../ariadna")
from datetime import datetime
from modelos.gestores_de_informacion.logueador import Logueador
from modelos.gestores_de_informacion.mensajeador import Mensajeador


class MotorBase(Mensajeador, Logueador):
    def _posiciones_datos(self, texto, cortes, quitar=True):
        contador = 0
        item = []
        for j in cortes:
            lista = []
            lista.append(j)
            lista.append(texto.find(j))
            if quitar is False:
                item.append(lista)
            elif quitar is True:
                if lista[1] == -1:
                    pass
                else:
                    item.append(lista)
        item = dict(item)
        item = sorted(item.items(), key=lambda x: x[1])
        contador += 1
        return item

    def _segmentador(self, texto, puntos_de_corte, canon, encabezados=True):
        para_buscar = texto
        posiciones = puntos_de_corte
        canonico = {}
        for i in canon:
            canonico[i] = ""
        prueba = {}
        if encabezados is True:
            for i in range(0, len(posiciones)):
                if i < len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[
                        posiciones[i][1] + len(clave) : posiciones[i + 1][1]
                    ].strip()
                elif i == len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] + len(clave) :].strip()
                prueba[clave] = valor
            for k in canonico.keys():
                if k in prueba:
                    canonico[k] = prueba[k]
        elif encabezados is False:
            for i in range(0, len(posiciones)):
                if i < len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] : posiciones[i + 1][1]].strip()
                elif i == len(posiciones) - 1:
                    clave = posiciones[i][0]
                    valor = para_buscar[posiciones[i][1] :].strip()
                prueba[clave] = valor
            for k in canonico.keys():
                if k in prueba:
                    canonico[k] = prueba[k]
        return canonico

    def _descomponer(self, particiones, canon, paso, encabezados=True):
        if paso != 1:
            b = []
            for i in particiones:
                x = self._segmentador(
                    i[paso],
                    self._posiciones_datos(i[paso], canon),
                    canon,
                    encabezados=encabezados,
                )
                b.append(x)
            return b
        elif paso == 1:
            b = []
            for i in particiones:
                if i[paso].find(" Descripcion:") > -1:
                    x = self._segmentador(
                        i[paso],
                        self._posiciones_datos(i[paso], canon[0]),
                        canon[0],
                        encabezados=encabezados,
                    )
                    b.append(x)
                elif i[paso].find(" Descripcion:") == -1:
                    x = self._segmentador(
                        i[paso],
                        self._posiciones_datos(i[paso], canon[1]),
                        canon[1],
                        encabezados=encabezados,
                    )
                    b.append(x)
            return b

    def _recuperar_values(self, dics):
        a_lista = []
        for i in dics:
            registro = []
            for value in i.values():
                registro.append(value)
            a_lista.append(registro)
        return a_lista

    def _limpiar_registro(self, registro):
        nuevo = registro.copy()
        for i in range(len(nuevo)):
            if nuevo[i] == "Sin especificar" or nuevo[i] == "Sin especifica":
                nuevo[i] = ""
        return nuevo

    def _formatear_fecha(self, registro, inicial=True):
        _registro = registro.copy()
        if inicial:
            try:
                if len(_registro[2]) > 4:
                    fecha_objeto = datetime.strptime(_registro[2], "%d %B %Y")
                    fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
                    _registro[2] = fecha_formateada

                if len(_registro[9]) > 4:
                    fecha_objeto = datetime.strptime(_registro[9], "%d %B %Y")
                    fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
                    _registro[9] = fecha_formateada

                if len(_registro[11]) > 4:
                    fecha_objeto = datetime.strptime(_registro[11], "%d %B %Y")
                    fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
                    _registro[11] = fecha_formateada
            except Exception as error:
                self.imprimir_con_color(error, "rojo")
            return _registro
        else:
            try:
                if len(_registro[15]) > 4 and _registro[15] != "Sin especifica":
                    fecha_objeto = datetime.strptime(_registro[15], "%d %B %Y")
                    fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")
                    _registro[15] = fecha_formateada
            except Exception as error:
                self.imprimir_con_color(error, "rojo")
            return _registro
