import model


def estructura(cortes, quitar=False):
    for i in proceso.posiciones_datos(cortes, quitar):
        print(i)
    print(cortes)
    print(len(proceso.posiciones_datos(cortes, quitar)))


if __name__ == "__main__":
    proceso = model.Inicial()
    # proceso.convertir()
    # estructura(proceso.cortes_datos)
    # estructura(proceso.cortes_inv)
    estructura(proceso.cortes_datos, quitar=True)
