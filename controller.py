import model
from tkinter import filedialog
from pathlib import Path as Ph

if __name__ == "__main__":
    inicial = model.Inicial(filedialog.askopenfilename())
    segmentado = model.Segmentado(
        rf"{Ph(__file__).resolve().parent}\Exportaciones\unificada.xlsx"
    )
