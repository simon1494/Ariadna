import tkinter as tk


class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Corrección de archivos")
        self.geometry("400x100")

        # Crear un contenedor para los botones
        contenedor_botones = tk.Frame(self)
        contenedor_botones.pack(pady=10)

        self.boton_original = tk.Button(contenedor_botones, text="Original", width=10)
        self.boton_original.pack(side=tk.LEFT, padx=40)

        self.boton_enmendado = tk.Button(contenedor_botones, text="Enmendado", width=10)
        self.boton_enmendado.pack(side=tk.RIGHT, padx=40)

        self.boton_corregir = tk.Button(
            self, text="Corregir Original", command=self.corregir_original
        )
        self.boton_corregir.pack(pady=10)

    def corregir_original(self):
        # Lógica para corregir el archivo original
        pass


# Crear una instancia de la clase Ventana
ventana = Ventana()

# Iniciar el bucle principal
ventana.mainloop()
