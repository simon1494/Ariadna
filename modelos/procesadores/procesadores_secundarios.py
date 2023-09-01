"""class Addendum:
    def rearmar_calificacion(self, registro, base, son_registros=True):
        if son_registros:
            calificacion = registro[26]
            base_nueva = base.copy()
            if calificacion.find("tipificación"):
                resultado = calificacion.split(
                    "CALIFICACIÓN LEGAL DEL HECHO Tipificación: "
                )
            else:
                resultado = calificacion.split("CALIFICACIÓN LEGAL DEL HECHO Delito: ")
            del resultado[0]
            resultado = list(map(lambda item: item.strip(), resultado))
            resultado = self.cotejar_todas(resultado, base_nueva)
            final = "; ".join(resultado)
            registro[26] = final
            return registro
        else:
            calificacion = registro[2]
            base_nueva = base.copy()
            calificacion = [calificacion.strip()]
            calificacion = self.cotejar_todas(calificacion, base_nueva)
            final = "; ".join(calificacion)
            registro[2] = final
            return registro

    @staticmethod
    def simplificada(calificacion):
        calificacion3 = calificacion.split(" Consumado: ")  # MODIFICADO 28-07-23
        calificacion4 = calificacion3[0]  # MODIFICADO 28-07-23
        calificacion0 = calificacion4.replace(" ", "")
        calificacion1 = calificacion0.replace("-", "")
        calificacion2 = calificacion1.replace(".", "")
        return calificacion2

    def cotejar_una(self, calificacion, data):
        a_cotejar = self.simplificada(calificacion)
        if a_cotejar in data:
            resultado = data[a_cotejar]
            if calificacion.find(" Consumado: Si"):
                resultado = resultado + " Consumado: Si"
            elif calificacion.find(" Consumado: No"):
                resultado = resultado + " Consumado: No"
            return resultado
        else:
            return "error"

    def cotejar_todas(self, elementos, data):
        final = list(map(lambda item: self.cotejar_una(item, data), elementos))
        return final

    @staticmethod
    def identificar_errores(archivo_original, modificado):
        errores = []
        for i in range(0, len(modificado)):
            if modificado[i][2].find("error") > -1:
                errores.append(
                    [
                        modificado[i][0],
                        modificado[i][1],
                        archivo_original[i][2],
                    ]
                )
        return errores
"""