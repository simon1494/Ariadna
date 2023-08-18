import threading

VER = "5.0.3-beta [2023-08-18]"

if __name__ == "__main__":
    from modelos.logo_inicio import LogoInicio
    from modelos.registro_de_usuario import VentanaLogueo

    def lanzar_logo_inicio():
        logueo = LogoInicio()
        logueo.show_image()

    hilo = hilo = threading.Thread(target=lanzar_logo_inicio)

    hilo.start()
    hilo.join()
    ventana_login = VentanaLogueo(VER)
