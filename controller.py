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
    proceso.unificada(
        proceso.datos_hecho[0],
        proceso.datos_inv[0],
        proceso.datos_efectos[0],
        proceso.general,
    )
