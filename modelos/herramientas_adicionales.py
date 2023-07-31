import colorama

colorama.init(convert=True)


def imprimir_con_color(mensaje, color="normal"):
    if color == "normal":
        print(mensaje)
    elif color == "azul":
        print(colorama.Back.BLUE + mensaje + colorama.Style.RESET_ALL)
    elif color == "blanco":
        print(
            colorama.Back.WHITE
            + colorama.Fore.BLACK
            + mensaje
            + colorama.Style.RESET_ALL
        )
    elif color == "lila":
        print(colorama.Back.MAGENTA + mensaje + colorama.Style.RESET_ALL)
    elif color == "verde":
        print(colorama.Back.GREEN + mensaje + colorama.Style.RESET_ALL)
    elif color == "amarillo":
        print(colorama.Back.YELLOW + mensaje + colorama.Style.RESET_ALL)
    elif color == "rojo":
        print(colorama.Back.RED + mensaje + colorama.Style.RESET_ALL)
