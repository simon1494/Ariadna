import pandas as pd


def cargar_fd():
    data = pd.read_excel(r"C:\Users\Simon\Documents\GitHub\minos\fd.xlsx")
    a = data.values.tolist()
    return a


def cargar_ap():
    data = pd.read_excel(r"C:\Users\Simon\Documents\GitHub\minos\ap.xlsx")
    a = data.values.tolist()
    return a
