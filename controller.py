import model
from tkinter import filedialog

if __name__ == "__main__":
    # if input("¿Desea procesar el archivo? ") == "si":
    inicial = model.Inicial(filedialog.askopenfilename())
    # if input("¿Desea segmentar el archivo? ") == "si":
    segmentado = model.Segmentado(filedialog.askopenfilename())
