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
print(proceso.final[50])
print("\n\n")
print(proceso.datos_inv[50])
