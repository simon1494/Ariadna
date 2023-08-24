import sys

sys.path.append("../ariadna")
import os
import pandas as pd
import re
from tkinter import filedialog
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

DIRECTORIO_PADRE = os.path.abspath(os.path.join(os.path.dirname(__file__)))

def seleccionar_archivo() -> str:
    ruta_del_archivo = filedialog.askopenfilename(
    )
    return ruta_del_archivo

def find_paso_columns(df):
    paso_columns = []

    # Obtiene los nombres de las columnas en base a las posiciones del primer registro
    first_row = df.iloc[0]
    column_names = [i for i in range(len(first_row))]

    # Busca las columnas que empiezan con "paso"
    for i, column_value in enumerate(first_row):
        if str(column_value).lower().startswith("paso"):
            paso_columns.append(column_names[i])

    return paso_columns

def extract_dates_between_strings(text, start_string, end_string):
    dates = []
    pattern = re.compile(f"{start_string}(.*?){end_string}")
    matches = pattern.findall(text)
    for match in matches:
        dates.append(match.strip())
    return dates

def get_paso_dates(df, paso_columns):
    paso_dates = []

    for column in paso_columns:
        for cell in df[column]:
            if isinstance(cell, str):
                extracted_dates = extract_dates_between_strings(cell, 'Fecha: ', ' Hora:')
                paso_dates.extend(extracted_dates)

    return paso_dates

def get_paso_data(df, paso_columns):
    paso_data = df[paso_columns]
    return paso_data

def convertir_fecha(fecha):
    fecha_str = fecha

    # Convertir la fecha en un objeto datetime
    fecha_obj = datetime.strptime(fecha_str, '%d %B %Y')

    # Obtener el número del mes y el día del mes como strings
    numero_mes = fecha_obj.strftime('%m')
    dia_mes = fecha_obj.strftime('%d')

    # Crear el formato deseado 'MM-DD'
    formato_deseado = f'{numero_mes}-{dia_mes}'

    return formato_deseado

def filtrar_y_guardar_campo(df, fecha,destino):
    search_string = f'Fecha: {fecha} Hora: '
    filtered_df = df[df[df.columns[0]].str.contains(search_string, case=True)]
    nombre = convertir_fecha(fecha)
    if not os.path.isfile(rf"{destino}\{nombre}.xlsx"):
        filtered_df.to_excel(rf"{destino}\{nombre}.xlsx", header=False, index=False)
        print(f"Listo {fecha}. {len(filtered_df)} registros.")



directorio = filedialog.askdirectory()
destino = filedialog.askdirectory()

# Obtén la lista de nombres de archivos en el directorio
nombres_archivos = os.listdir(directorio)

# Itera sobre los nombres de archivos
for nombre_archivo in nombres_archivos:
    ruta_archivo = os.path.join(directorio, nombre_archivo)
    
    if os.path.isfile(ruta_archivo):
        """try:"""
        df = pd.read_excel(ruta_archivo,header=None)

        # Llama a la función para encontrar las columnas que empiezan con "paso"
        paso_columns = find_paso_columns(df)

        paso_data = get_paso_data(df, paso_columns)

        # Obtiene las fechas de las columnas "paso"
        paso_dates = get_paso_dates(df, paso_columns)
        paso_dates = set(paso_dates)

        print("")
        print(f"Fechas en el archivo: {paso_dates}")
        for fecha in paso_dates:   
            filtrar_y_guardar_campo(paso_data, fecha,destino)
        """except Exception as error:
            print(f"Error con el archivo {nombre_archivo}: {error}")"""
