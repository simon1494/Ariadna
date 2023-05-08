import model
import checkpoints


def estructura(cortes, quitar=False):
    for i in proceso.posiciones_datos(cortes, quitar):
        print(i)
    print(cortes)
    print(len(proceso.posiciones_datos(cortes, quitar)))


if __name__ == "__main__":
    proceso = model.Inicial(
        checkpoints.cp_iniciales,
        checkpoints.cp_datos,
        checkpoints.cp_inv,
        checkpoints.cp_efectos,
    )
    # proceso.convertir()
    # estructura(proceso.cortes_datos)
    # estructura(proceso.cortes_inv)
    # estructura(proceso.cortes_datos)7
    print(len(proceso.formateado))
    print(proceso.posiciones_datos(proceso.cortes_datos)[1299])
    print(proceso.reordenar()[1300])

    """contador = 1
    print(proceso.posiciones(quitar=False))
    for i in proceso.posiciones(quitar=False):
        if 250 < contador < 400:
            print(i)
            print(contador)
        contador += 1"""
