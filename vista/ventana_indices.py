import sys

sys.path.append("../ariadna")
import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter.font import Font
from .ventana_base import VentanaBase
from tkinter import ttk


class VentanaIndices(tk.Toplevel, VentanaBase):
    def __init__(self, ventana, indices):
        super().__init__(ventana)
        self.title("Setear índices")
        self.ancho = 360
        self.alto = 330
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.configure(bg=self.color_back)
        self.crear_widgets(indices)

    def crear_widgets(self, indices):
        etiquetas = [
            "Hechos",
            "Calificaciones",
            "Armas",
            "Automotores",
            "Objetos",
            "Secuestros",
            "Involucrados",
        ]

        sep_x = 30
        sep_y = 0.5
        font_label = Font(weight="bold", size=9)
        self.etiquetas_labels = []
        self.etiquetas_entries = []

        for i, etiqueta_texto in enumerate(etiquetas):
            etiqueta = tk.Label(
                self,
                text=etiqueta_texto,
                font=font_label,
                fg="white",
                bg=self.color_back,
            )
            etiqueta.place(x=70, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_labels.append(etiqueta)

            cuadro_texto = tk.Entry(
                self,
                textvariable=indices[i],
            )
            cuadro_texto.place(x=160, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_entries.append(cuadro_texto)

        btn_base = tk.Button(
            self,
            text="Desde la Base",
            bg="orange",
            command=lambda: self.conectar_con_base(),
        )
        btn_base.place(x=155, y=275)

        btn_archivo = tk.Button(
            self,
            text="Desde archivo",
            bg="sky blue",
            command=lambda: self.conectar_con_archivo(),
        )
        btn_archivo.place(x=40, y=275)

        btn_setear_ids = tk.Button(
            self,
            text="Setear IDs",
            bg="light green",
            command=lambda: self.actualizar_indices(indices, self.etiquetas_entries),
        )
        btn_setear_ids.place(x=270, y=275)

        etiqueta_base = tk.Label(
            self,
            text="Nombre Base",
            font=font_label,
            fg="white",
            bg=self.color_back,
        )
        etiqueta_base.place(x=70, y=225, anchor=tk.NW)

        opciones_base = [
            "delitos_2021 LOCAL",
            "delitos_2022 LOCAL",
            "delitos_2023 LOCAL",
            "delitos_2024 LOCAL",
            "delitos_2021 SERVER",
            "delitos_2022 SERVER",
            "delitos_2023 SERVER",
            "delitos_2024 SERVER",
            "OPERATIVO SOL",
        ]
        self.opcion_seleccionada = tk.StringVar(self)
        self.opcion_seleccionada.set(
            opciones_base[0]
        )  # Establecer la opción predeterminada

        # Cuadro de lista desplegable
        cuadro_texto_base = ttk.Combobox(
            self, textvariable=self.opcion_seleccionada, values=opciones_base
        )
        cuadro_texto_base.place(x=160, y=225, anchor=tk.NW)

    def actualizar_indices(self, indices, entries):
        for i, ind in enumerate(indices):
            ind.set(entries[i].get())
        self.mostrar_mensaje_info("Los índices fueron configurados correctamente")
        self.destroy()

    def conectar_con_base(self):
        try:
            indices = []
            base = self.opcion_seleccionada.get()
            if base != "":
                try:
                    if base == "delitos_2021 LOCAL":
                        conexion = mysql.connector.connect(
                            host="localhost",
                            port="3306",
                            user="root",
                            password="",
                            database="delitos_2021",
                        )
                    elif base == "delitos_2022 LOCAL":
                        conexion = mysql.connector.connect(
                            host="localhost",
                            port="3306",
                            user="root",
                            password="",
                            database="delitos_2022",
                        )
                    elif base == "delitos_2023 LOCAL":
                        conexion = mysql.connector.connect(
                            host="localhost",
                            port="3306",
                            user="root",
                            password="",
                            database="delitos_2023",
                        )
                    elif base == "delitos_2024 LOCAL":
                        conexion = mysql.connector.connect(
                            host="localhost",
                            port="3306",
                            user="root",
                            password="",
                            database="delitos_2024",
                        )
                    elif base == "delitos_2021 SERVER":
                        conexion = mysql.connector.connect(
                            host="192.168.1.125",
                            port="3307",
                            user="simon",
                            password="monitoreo",
                            database="delitos_2021",
                        )
                    elif base == "delitos_2022 SERVER":
                        conexion = mysql.connector.connect(
                            host="192.168.1.125",
                            port="3307",
                            user="simon",
                            password="monitoreo",
                            database="delitos_2022",
                        )
                    elif base == "delitos_2023 SERVER":
                        conexion = mysql.connector.connect(
                            host="192.168.1.125",
                            port="3307",
                            user="simon",
                            password="monitoreo",
                            database="delitos_2023",
                        )
                    elif base == "delitos_2024 SERVER":
                        conexion = mysql.connector.connect(
                            host="192.168.1.125",
                            port="3307",
                            user="simon",
                            password="monitoreo",
                            database="delitos_2024",
                        )
                    elif base == "OPERATIVO SOL":
                        conexion = mysql.connector.connect(
                            host="192.168.1.125",
                            port="3307",
                            user="simon",
                            password="monitoreo",
                            database="op_sol",
                        )

                except Exception as error:
                    print(error)
                # Crear un cursor para ejecutar consultas
                cursor = conexion.cursor()
                if base != "OPERATIVO SOL":
                    consulta = "SELECT max(id_hecho) FROM datos_hecho"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        indices.append(fila[0])

                    indices.append(0)

                    consulta = "SELECT max(id) FROM armas"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        indices.append(fila[0])

                    consulta = "SELECT max(id) FROM automotores"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        indices.append(fila[0])

                    consulta = "SELECT max(id) FROM objetos"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        indices.append(fila[0])

                    consulta = "SELECT max(id) FROM secuestros"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        indices.append(fila[0])

                    consulta = "SELECT max(id) FROM involucrados"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        indices.append(fila[0])

                    # Cerrar el cursor y la conexión
                    cursor.close()
                    conexion.close()

                    for i, ind in enumerate(indices):
                        self.etiquetas_entries[i].delete(0, "end")
                        self.etiquetas_entries[i].insert(0, ind + 1)
                else:
                    consulta = "SELECT max(id_hecho) FROM datos_hecho"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        indices.append(fila[0])

                    indices.append(0)
                    indices.append(0)
                    indices.append(0)
                    indices.append(0)
                    indices.append(0)
                    indices.append(0)

                    for i, ind in enumerate(indices):
                        self.etiquetas_entries[i].delete(0, "end")
                        self.etiquetas_entries[i].insert(0, ind + 1)

            else:
                self.mostrar_mensaje_advertencia("Seleccione una base primero")

        except Exception as error:
            self.mostrar_mensaje_error(error)

    def conectar_con_archivo(self):
        ruta_archivo = self.seleccionar_archivo("/Exportaciones/Segmentados/")
        try:
            # Cargar el archivo Excel
            df = pd.read_excel(ruta_archivo, sheet_name=None)

            # Lista para almacenar los últimos registros
            ultimos_registros = []

            # Iterar sobre cada hoja del archivo
            for hoja, datos in df.items():
                # Obtener el último valor de la primera columna
                try:
                    ultimo_registro = datos.iloc[-1, 0]
                    ultimos_registros.append(ultimo_registro)
                except Exception:
                    raise ValueError(
                        "Una de las tablas se encuentra vacía y no fue posible recuperar ningún índice. Por favor, setea los índices a través de la base"
                    )

            for i, ind in enumerate(ultimos_registros):
                self.etiquetas_entries[i].delete(0, "end")
                self.etiquetas_entries[i].insert(0, ind + 1)

        except FileNotFoundError:
            self.mostrar_mensaje_info("No se ha seleccionado ningún archivo")

        except Exception as a:
            self.mostrar_mensaje_advertencia(a)
