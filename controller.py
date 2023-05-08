import model
import checkpoints

if __name__ == "__main__":
    proceso = model.Inicial(
        checkpoints.cp_iniciales,
        checkpoints.cp_datos,
        checkpoints.cp_inv,
        checkpoints.cp_efectos,
        checkpoints.general,
    )
    x = 0
    print(proceso.final[x])
    print("\n\n")
    print(proceso.datos_hecho[x])
    print("\n\n")
    print(proceso.datos_inv[x])
    print("\n\n")
    print(proceso.datos_efectos[x])
