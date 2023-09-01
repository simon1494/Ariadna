import threading

VER = "5.1.5-beta [2023-08-25]"

if __name__ == "__main__":
    from vista.ventana_inicio import VentanaInicio
    from vista.ventana_login import VentanaLogin

    def lanzar_inicio():
        ventana_inicio = VentanaInicio()
        ventana_inicio.show_image()

    hilo = hilo = threading.Thread(target=lanzar_inicio)

    hilo.start()
    hilo.join()
    ventana_login = VentanaLogin(VER)
