import tkinter as tk
import model
import mysql.connector
from tkinter import filedialog
from tkinter import ttk
from tkinter.font import Font
import checkpoints as ck
import pandas as pd
from pathlib import Path as Ph
import os


class Ventana_principal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ventana con botones")
        self.ancho = 600
        self.alto = 250
        self.ventana.geometry(self.centrar_ventana(self.ventana, self.ancho, self.alto))
        self.ventana.configure(bg="dark gray")

        self.setear_indices()
        self.crear_botones()

    def crear_botones(self):
        x_pos = int(self.ancho / 2)
        y_pos = int(self.alto / 2)
        estilo_fuente = ("Palatino Linotype", 16)
        b_alto = 75
        b_ancho = 200

        separacion = 120

        boton_inicial = tk.Button(
            self.ventana,
            text="INICIAL",
            bg="light green",
            fg="black",
            font=estilo_fuente,
            command=lambda: self.procesar_inicial(),
        )
        boton_inicial.place(
            x=x_pos - separacion - (b_ancho / 2),
            y=y_pos - (b_alto / 2),
            width=b_ancho,
            height=b_alto,
        )

        boton_segmentado = tk.Button(
            self.ventana,
            text="SEGMENTADO",
            bg="light green",
            fg="black",
            font=estilo_fuente,
            command=lambda: self.procesar_final(),
        )
        boton_segmentado.place(
            x=x_pos + separacion - (b_ancho / 2),
            y=y_pos - (b_alto / 2),
            width=b_ancho,
            height=b_alto,
        )

        boton_addendum = tk.Button(
            self.ventana,
            text="Addendum",
            bg="light green",
            fg="black",
            font=("Palatino Linotype", 11),
            command=lambda: self.abrir_ventana_addendum(),
        )
        boton_addendum.place(
            x=500,
            y=210,
            width=80,
            height=20,
        )

        boton_compilar = tk.Button(
            self.ventana,
            text="Compilar",
            bg="light green",
            fg="black",
            font=("Palatino Linotype", 11),
            command=lambda: self.compilar_archivos(),
        )
        boton_compilar.place(
            x=410,
            y=210,
            width=80,
            height=20,
        )

        boton_errores = tk.Button(
            self.ventana,
            text="Errores",
            bg="light green",
            fg="black",
            font=("Palatino Linotype", 11),
            command=lambda: self.abrir_ventana_errores(),
        )
        boton_errores.place(
            x=20,
            y=210,
            width=80,
            height=20,
        )

        boton_indices = tk.Button(
            self.ventana,
            text="Indices",
            bg="light green",
            fg="black",
            font=("Palatino Linotype", 11),
            command=lambda: self.abrir_ventana_indices(),
        )
        boton_indices.place(
            x=20,
            y=20,
            width=80,
            height=20,
        )

        boton_ns = tk.Button(
            self.ventana,
            text="Procesar ns",
            bg="light green",
            fg="black",
            font=("Palatino Linotype", 11),
            command=lambda: self.procesar_varios(),
        )
        boton_ns.place(
            x=470,
            y=20,
            width=110,
            height=20,
        )

        boton_crudos = tk.Button(
            self.ventana,
            text="Procesar crudos",
            bg="light green",
            fg="black",
            font=("Palatino Linotype", 11),
            command=lambda: self.procesar_crudos(),
        )
        boton_crudos.place(
            x=330,
            y=20,
            width=130,
            height=20,
        )

    def setear_indices(self):
        self.id_hechos = tk.IntVar()
        self.id_calificaciones = tk.IntVar()
        self.id_automotores = tk.IntVar()
        self.id_armas = tk.IntVar()
        self.id_objetos = tk.IntVar()
        self.id_secuestros = tk.IntVar()
        self.id_involucrados = tk.IntVar()

        self.id_hechos.set(1)
        self.id_calificaciones.set(1)
        self.id_automotores.set(1)
        self.id_armas.set(1)
        self.id_objetos.set(1)
        self.id_secuestros.set(1)
        self.id_involucrados.set(1)

        self.indices = (
            self.id_hechos,
            self.id_calificaciones,
            self.id_armas,
            self.id_automotores,
            self.id_objetos,
            self.id_secuestros,
            self.id_involucrados,
        )

    def iniciar(self):
        self.ventana.mainloop()

    def procesar_inicial(self):
        #::::::::::::::::::::::::procesado inicial:::::::::::::::::::::::::::
        try:
            path = filedialog.askopenfilename()

            nombre_archivo = os.path.splitext(os.path.basename(path))[0]

            formateador = model.Formateador()
            archivo = model.Administrador._cargar(path)
            tester = model.Tester(archivo)
            if len(tester.errores) > 0:
                log_errores = model.Administrador._convertir_inicial(
                    tester.errores,
                    ["indice", "n° registro", "para enmendar"],
                    nombre=nombre_archivo,
                    error=True,
                )
                tk.messagebox.showinfo(
                    "Advertencia",
                    "Hubo errores en los listados.\nSe ha generado un registro errores.",
                )
                os.startfile(log_errores)
            else:
                archivo, identificadores = formateador._formatear(archivo, ck.cp_iden)
                inicial = model.Inicial(archivo, identificadores)
                path = model.Administrador._convertir_inicial(
                    inicial.sin_duplicados, ck.general, nombre=nombre_archivo
                )
                if tk.messagebox.askyesno(
                    "Segmentar", "¿Desea proceder a segmentar el archivo?"
                ):
                    self.procesar_final(path)
        except FileNotFoundError:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ningún archivo."
            )

        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def procesar_final(self, path=False):
        indices = list(map(lambda var: var.get(), self.indices))
        try:
            if path is False:
                archivo1 = model.Administrador._cargar(
                    filedialog.askopenfilename(), no_tiene_encabezados=False
                )
                segmentado = model.Segmentado(archivo1, indices)
            else:
                archivo1 = model.Administrador._cargar(path, no_tiene_encabezados=False)
                segmentado = model.Segmentado(archivo1, indices)
            try:
                try:
                    mensaje = model.Formateador.comprobar_salida(segmentado.final)
                    if mensaje != "":
                        tk.messagebox.showinfo("Advertencia", mensaje)
                except Exception as error:
                    print(error)
                model.Administrador._convertir_segmentado(segmentado.final)
                tk.messagebox.showinfo(
                    "Advertencia", f"El proceso se completo correctamente :)"
                )
            except AttributeError:
                tk.messagebox.showinfo(
                    "Advertencia", f"El proceso de segmentado se ha abortado."
                )
                ventana_errores = Ventana_addendum(
                    self.ventana, archivo=segmentado.errores
                )
        except FileNotFoundError:
            tk.messagebox.showinfo(
                "Advertencia", f"No se ha seleccionado ningún archivo."
            )

    def procesar_crudos(self, path=False):
        carpeta = filedialog.askdirectory()
        archivos = os.listdir(carpeta)
        formateador = model.Formateador()

        for archivo in archivos:
            path = os.path.join(
                carpeta, archivo
            )  # Obtener la ruta completa del archivo
            if os.path.isfile(path):  # Comprobar si es un archivo (no una carpeta)
                try:
                    nombre_archivo = os.path.splitext(os.path.basename(path))[0]
                    archivo0 = model.Administrador._cargar(path)
                    try:
                        tester = model.Tester(archivo0)
                        try:
                            if len(tester.errores) > 0:
                                log_errores = model.Administrador._convertir_inicial(
                                    tester.errores,
                                    ["indice", "n° registro", "para enmendar"],
                                    nombre=nombre_archivo,
                                    error=True,
                                )
                            else:
                                archivo0, identificadores = formateador._formatear(
                                    archivo0, ck.cp_iden
                                )
                                inicial = model.Inicial(archivo0, identificadores)
                                path = model.Administrador._convertir_inicial(
                                    inicial.sin_duplicados,
                                    ck.general,
                                    nombre=nombre_archivo,
                                )
                        except Exception as error:
                            print(
                                f"({archivo}) Error en etapa de procesado del archivo: {error}"
                            )
                    except Exception as error:
                        print(
                            f"({archivo}) Error en etapa de testeo de información entrante: {error}"
                        )
                except Exception as error:
                    print(
                        f"({archivo}) Error en etapa de carga del archivo crudo: {error}"
                    )
            print(f"Listo {archivo}")
        tk.messagebox.showinfo(
            "Aviso",
            "El procesado de crudos ha sido completado.",
        )

    def procesar_varios(self):
        carpeta = filedialog.askdirectory()
        archivos = os.listdir(carpeta)

        indices = list(map(lambda var: var.get(), self.indices))
        for archivo in archivos:
            path = os.path.join(
                carpeta, archivo
            )  # Obtener la ruta completa del archivo
            if os.path.isfile(path):  # Comprobar si es un archivo (no una carpeta)
                try:
                    archivo1 = model.Administrador._cargar(
                        path, no_tiene_encabezados=False
                    )
                    try:
                        segmentado = model.Segmentado(archivo1, indices, carpeta=True)
                        try:
                            mensaje = model.Formateador.comprobar_salida(
                                segmentado.final
                            )
                            if mensaje != "":
                                tk.messagebox.showinfo("Advertencia", mensaje)
                            try:
                                model.Administrador._convertir_segmentado(
                                    segmentado.final, nombre=archivo
                                )
                                print(f"\nPreparando {archivo}")
                                try:
                                    indices_finales = (
                                        model.Administrador._obtener_indices(
                                            segmentado.final, indices
                                        )
                                    )
                                    print(f"Iniciales: {str(indices)}")
                                    print(f"Finales: {str(indices_finales)}")
                                    indices = list(
                                        map(lambda x: x + 1, indices_finales)
                                    )
                                    print(f"Siguientes: {str(indices)}")
                                except Exception as error:
                                    print(
                                        f"({archivo}) Error en la obtención de índices nuevos: {error}"
                                    )
                            except Exception as error:
                                print(
                                    f"({archivo}) Error en conversión final a formato Excel: {error}"
                                )
                        except Exception as error:
                            print(
                                f"({archivo}) Error en la comprobación de datos salientes: {error}"
                            )
                    except Exception as error:
                        print(f"({archivo}) Error en etapa de procesado: {error}")
                except Exception as error:
                    print(f"({archivo}) Error en etapa de carga: {error}")
            print(f"Listo {archivo}")
        tk.messagebox.showinfo(
            "Aviso",
            "El procesado de no segmentados ha sido completado.",
        )

    def compilar_archivos(self):
        carpeta = filedialog.askdirectory()
        print(carpeta)
        archivos = os.listdir(carpeta)

        # Nombre del archivo final
        archivo_final = f"{carpeta}/consolidado.xlsx"

        # Leer la primera hoja de un archivo para obtener los nombres de las hojas
        primer_archivo = f"{carpeta}/{archivos[0]}"
        with pd.ExcelFile(primer_archivo) as xls:
            hojas = xls.sheet_names

        # Almacenar los datos en un diccionario por hoja
        datos = {}
        for hoja in hojas:
            datos[hoja] = pd.DataFrame()

        # Leer los archivos de Excel y almacenar los datos en el diccionario
        for archivo in archivos:
            with pd.ExcelFile(f"{carpeta}/{archivo}") as xls:
                for hoja in hojas:
                    df = pd.read_excel(xls, sheet_name=hoja)
                    if hoja == "datos_hecho":
                        df["Latitud:"] = df["Latitud:"].astype(str)
                        df["Longitud:"] = df["Latitud:"].astype(str)
                    datos[hoja] = pd.concat([datos[hoja], df])
            print("Listo ", archivo)

        # Escribir los datos consolidados en un archivo de Excel
        with pd.ExcelWriter(archivo_final) as writer:
            for hoja, df in datos.items():
                df.to_excel(writer, sheet_name=hoja, index=False)

        print("\nAnalizando coherencia de indexados...")
        try:
            if self.comprobar_indices(f"{carpeta}/consolidado.xlsx"):
                print("Chequeada coherencia de indexados sin errores")
            else:
                print("Se detectaron errores de coherencia en los indexados")
        except Exception as error:
            print(error)
        print("Se ha creado el archivo consolidado:", archivo_final)

    def comprobar_indices(self, archivo):
        # Leer el archivo Excel
        xls = pd.ExcelFile(archivo)

        # Lista para almacenar las tuplas de cada hoja
        tuplas_hojas = []

        # Recorrer cada hoja del archivo

        for hoja_nombre in xls.sheet_names:
            # Leer la hoja y obtener los valores de la primera columna
            df = pd.read_excel(xls, sheet_name=hoja_nombre)
            columna = df.iloc[:, 0]  # Primera columna (index 0)

            # Convertir la columna en una tupla y agregarla a la lista
            tupla_hoja = tuple(columna.values[0:])  # Excluir el encabezado
            tuplas_hojas.append(tupla_hoja)

            # Verificar si la lista contiene enteros consecutivos en orden ascendente
            for tupla in tuplas_hojas:
                if not tupla:  # Si la lista está vacía, no se considera consecutiva
                    return False

                n = tupla[0]  # Primer elemento de la lista
                for num in tupla:
                    if num != n:  # Si el número no es igual a n, no es consecutivo
                        return False
                    n += 1  # Incrementar n para verificar el siguiente número
        return True

    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y-100}"

    def abrir_ventana_addendum(self):
        ventana_addendum = Ventana_addendum(self.ventana)

    def abrir_ventana_errores(self):
        ventana_errores = Ventana_errores(self.ventana)

    def abrir_ventana_indices(self):
        ventana_indices = Ventana_indices(self.ventana, self.indices)


class Ventana_addendum(tk.Toplevel):
    def __init__(
        self,
        ventana,
        archivo=[],
    ):
        super().__init__()
        self.title("Módulo Addendum")
        self.ancho = 400
        self.alto = 300
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.registros = archivo
        self.original = ""
        self.crear_widgets()
        self.correr()

    def crear_widgets(self):
        # Crear treeview con 3 columnas
        self.control_entry = tk.StringVar()
        self.control_entry.set("")

        self.treeview = ttk.Treeview(self, columns=("id", "id_hecho", "calificacion"))

        # Configurar headers de las columnas
        self.treeview.heading("id", text="ID")
        self.treeview.heading("id_hecho", text="ID Hecho")
        self.treeview.heading("calificacion", text="Calificación")
        self.treeview.column("#0", minwidth=0, width=0, anchor="center")
        self.treeview.column("id", minwidth=0, width=30, anchor="center")
        self.treeview.column("id_hecho", minwidth=0, width=70, anchor="center")
        self.treeview.column("calificacion", minwidth=0, width=290, anchor="center")

        # Agregar datos al treeview (ejemplo)
        for registro in self.registros:
            self.treeview.insert(
                "", "end", values=(registro[0], registro[1], registro[2])
            )

        self.treeview.bind(
            "<ButtonRelease-1>",
            lambda evento: self.seleccionar_item(self.treeview, self.control_entry),
        )
        self.treeview.pack()

        # Crear entry con label "seleccionado" al lado izquierdo
        self.entry_frame = ttk.Frame(self)
        self.entry_frame = ttk.Entry(self, textvariable=self.control_entry)
        self.entry_frame.pack()

        # Crear botón "Agregar a base"
        self.agregar_boton = ttk.Button(
            self,
            text="Agregar a base",
            command=lambda: self.agregar_a_base(self.entry_frame, self.original),
        )
        self.agregar_boton.pack(pady=10)

    def seleccionar_item(self, tree, entry):
        try:
            item_ = tree.focus()
            datos_registro = tree.item(item_)["values"][2]
            entry.set(datos_registro)
            self.original = datos_registro
        except Exception:
            ...

    def agregar_a_base(self, entry, original):
        # Lógica para agregar los datos a la base de datos
        # Leer el archivo Excel
        df = dict(
            pd.read_excel(
                rf"{Ph(__file__).resolve().parent}\Base calificaciones\calificaciones_db.xlsx",
                header=None,
            ).values.tolist()
        )
        addendum = model.Addendum()
        simplificado = addendum.simplificada(original)

        # Agregar un nuevo registro
        df[simplificado] = entry.get()

        # convierto el dic en df
        df = list(df.items())
        df = pd.DataFrame(df)

        # Guardar los cambios en el archivo Excel
        df.to_excel(
            rf"{Ph(__file__).resolve().parent}\Base calificaciones\calificaciones_db.xlsx",
            index=False,
            header=False,
        )
        tk.messagebox.showinfo(
            "Alta",
            f"Se ha agregado la nueva carátula a la base de datos de calificaciones.",
        )

    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y-100}"

    def correr(self):
        self.mainloop()


class Ventana_errores(tk.Toplevel):
    def __init__(self, ventana):
        super().__init__()
        self.title("Módulo errores")
        self.ancho = 400
        self.alto = 300
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.geometry("400x100")
        self.corregido = None
        self.crear_botones()
        self.correr()

    def crear_botones(self):
        # Crear un contenedor para los botones
        contenedor_botones = tk.Frame(self)
        contenedor_botones.pack(pady=10)

        self.boton_original = tk.Button(
            contenedor_botones,
            text="Original",
            width=10,
            command=lambda: self.cargar_original(),
        )
        self.boton_original.pack(side=tk.LEFT, padx=40)

        self.boton_enmendado = tk.Button(
            contenedor_botones,
            text="Enmendado",
            width=10,
            command=lambda: self.cargar_enmendado(),
        )
        self.boton_enmendado.pack(side=tk.RIGHT, padx=40)

        self.boton_corregir = tk.Button(
            self, text="Corregir Original", command=lambda: self.corregir_original()
        )
        self.boton_corregir.pack(pady=10)

    def corregir_original(self):
        original = model.Administrador._cargar(
            self.path_original,
        )
        enmendado = model.Administrador._cargar(
            self.path_enmendado, no_tiene_encabezados=False, es_original=False
        )

        for error in enmendado:
            original[int(error[0])][0] = error[2]

        nombre_archivo = os.path.splitext(os.path.basename(self.path_original))[0]
        ult = pd.DataFrame(original)
        ult.to_excel(
            rf"{Ph(__file__).resolve().parent}\Exportaciones\Corregidos\{nombre_archivo}.xlsx",
            index=False,
            header=False,
        )
        print("Corregidos correctamente")
        return rf"{Ph(__file__).resolve().parent}\Exportaciones\Corregidos\{nombre_archivo}.xlsx"

    def cargar_original(self):
        self.path_original = filedialog.askopenfilename()

    def cargar_enmendado(self):
        self.path_enmendado = filedialog.askopenfilename()

    def correr(self):
        self.mainloop()

    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y-100}"


class Ventana_indices(tk.Toplevel):
    def __init__(self, ventana, indices):
        super().__init__()
        self.title("Etiquetas y Cuadros de Texto")
        self.ancho = 360
        self.alto = 300
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.configure(bg="gray")
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
                bg="gray",
            )
            etiqueta.place(x=70, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_labels.append(etiqueta)

            cuadro_texto = tk.Entry(
                self,
                textvariable=indices[i],
            )
            cuadro_texto.place(x=160, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_entries.append(cuadro_texto)

        btn_conectar = tk.Button(
            self,
            text="Conectar con Base",
            bg="light green",
            command=lambda: self.conectar_con_base(),
        )
        btn_conectar.place(x=50, y=250)

        btn_setear_ids = tk.Button(
            self,
            text="Setear IDs",
            bg="light green",
            command=lambda: self.actualizar_indices(indices, self.etiquetas_entries),
        )
        btn_setear_ids.place(x=240, y=250)

    def actualizar_indices(self, indices, entries):
        for i, ind in enumerate(indices):
            ind.set(entries[i].get())
        self.withdraw()
        tk.messagebox.showinfo(
            "Indices configurados", f"Los índices fueron configurados correctamente"
        )
        self.destroy()

    @staticmethod
    def centrar_ventana(win, window_width, window_height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        return f"{window_width}x{window_height}+{center_x}+{center_y-100}"

    def conectar_con_base(self):
        try:
            indices = []

            conexion = mysql.connector.connect(
                host="localhost", user="root", password="", database="monitoreo"
            )

            # Crear un cursor para ejecutar consultas
            cursor = conexion.cursor()

            consulta = "SELECT max(id_hecho) FROM hechos"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for fila in resultados:
                indices.append(fila[0])

            indices.append(1)

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

        except Exception as error:
            tk.messagebox.showinfo("!!", error)
