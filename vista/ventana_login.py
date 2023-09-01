import sys

sys.path.append("../ariadna")
import tkinter as tk
from vista.ventana_base import VentanaBase
import checkpoints as ck


class VentanaLogin(tk.Tk, VentanaBase):
    USUARIOS = ck.USUARIOS

    def __init__(self, version):
        super().__init__()
        self.version = version

        self.ancho = 300
        self.alto = 120
        self.geometry(self.centrar_ventana(self, self.ancho, self.alto))

        self.title("Login")
        self.configure(bg=self.color_back)

        # Crear etiquetas y campos de entrada para usuario y contraseña
        self.etiqueta_usuario = tk.Label(
            self, text="Usuario:", background=self.color_back, fg="white"
        )
        self.etiqueta_usuario.pack()
        self.user = tk.StringVar()
        self.user.set("")
        self.entry_usuario = tk.Entry(self, textvariable=self.user)
        self.entry_usuario.pack()

        self.etiqueta_contrasena = tk.Label(
            self, text="Contraseña:", background=self.color_back, fg="white"
        )
        self.etiqueta_contrasena.pack()
        self.entry_contrasena = tk.Entry(self, show="*")  # Para ocultar la contraseña
        self.entry_contrasena.pack()

        # Botón de login
        self.boton_login = tk.Button(
            self, text="Ingresar", command=lambda: self.verificar()
        )
        self.boton_login.pack()
        self.entry_usuario.bind("<Return>", lambda event: self.verificar())
        self.entry_contrasena.bind("<Return>", lambda event: self.verificar())
        self.mainloop()

    def verificar(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        # Verificar si el usuario y la contraseña son válidos (ejemplo sencillo)
        if usuario in self.USUARIOS and contrasena == self.USUARIOS[usuario]:
            self.destroy()  # Destruir la ventana de logueo
            self.abrir_ventana_principal(usuario)  # Abrir GUI principa
        else:
            self.mostrar_mensaje_advertencia("Usuario o contraseña inválidos")

    def abrir_ventana_principal(self, usuario):
        from controladores.controlador_GUI import Aplicacion

        app = Aplicacion(self.version, usuario)
