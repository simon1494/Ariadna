import pandas as pd


def cargar():
    data = pd.read_excel(r"C:\Users\Simon\Documents\GitHub\minos\prueba.xlsx")
    a = data.values.tolist()
    return a
