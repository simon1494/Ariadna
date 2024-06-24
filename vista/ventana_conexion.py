import sys

sys.path.append("../ariadna")
import mysql.connector
import tkinter as tk
from tkinter.font import Font
from .ventana_base import VentanaBase
from datetime import datetime


class VentanaConexion(tk.Toplevel, VentanaBase):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.title("Conectar con base")
        self.ancho = 360
        self.alto = 360
        self.geometry(self.centrar_ventana(ventana, self.ancho, self.alto))
        self.configure(bg=self.color_back)

        self.host = tk.StringVar()
        self.port = tk.StringVar()
        self.user = tk.StringVar()
        self.passw = tk.StringVar()
        self.base = tk.StringVar()

        self.host.set("localhost")
        self.port.set("3306")
        self.user.set("root")
        self.passw.set("")
        self.base.set(f"delitos_{datetime.now().year}")

        self.set_vars = [self.host, self.port, self.user, self.passw, self.base]

        self.indices = []

        self.crear_widgets(ventana)

    def crear_widgets(self, ventana):
        etiquetas = ["HOST: ", "PORT: ", "USER: ", "PASS: ", "DATABASE: "]

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
            if i in (0, 1):
                cuadro_texto = tk.Entry(
                    self,
                    textvariable=self.set_vars[i],
                )
            else:
                cuadro_texto = tk.Entry(self, textvariable=self.set_vars[i], show="*")
            cuadro_texto.place(x=160, y=(i + sep_y) * sep_x, anchor=tk.NW)
            self.etiquetas_entries.append(cuadro_texto)

        self.btn_base = tk.Button(
            self,
            text="Conectar a base",
            bg=self.amarillo,
            command=lambda: self.conectar_con_base(ventana),
        )
        self.btn_base.place(x=58, y=310)

        self.crear_base_ = tk.Button(
            self,
            text="Crear base",
            bg=self.amarillo,
            command=lambda: self.crear_base(
                self.etiquetas_entries[0].get(),
                self.etiquetas_entries[1].get(),
                self.etiquetas_entries[2].get(),
                self.etiquetas_entries[3].get(),
                self.etiquetas_entries[4].get(),
            ),
        )
        self.crear_base_.place(x=200, y=310)
        self.etiquetas_entries[0].bind(
            "<Return>", lambda event: self.conectar_con_base(ventana)
        )
        self.etiquetas_entries[1].bind(
            "<Return>", lambda event: self.conectar_con_base(ventana)
        )
        self.etiquetas_entries[2].bind(
            "<Return>", lambda event: self.conectar_con_base(ventana)
        )
        self.etiquetas_entries[3].bind(
            "<Return>", lambda event: self.conectar_con_base(ventana)
        )
        self.etiquetas_entries[4].bind(
            "<Return>", lambda event: self.conectar_con_base(ventana)
        )

    def conectar_con_base(self, ventana):
        output = tk.Text(self, background=self.color_botones)
        output.config(borderwidth=2, relief="sunken")
        output.place(x=58, y=160, width=250, height=140)
        print("\n\n")
        try:
            indices = []

            datos_conexion = [
                self.etiquetas_entries[0].get(),
                self.etiquetas_entries[1].get(),
                self.etiquetas_entries[2].get(),
                self.etiquetas_entries[3].get(),
                self.etiquetas_entries[4].get(),
            ]

            conexion = mysql.connector.connect(
                host=datos_conexion[0],
                port=datos_conexion[1],
                user=datos_conexion[2],
                password=datos_conexion[3],
                database=datos_conexion[4],
            )

            # Crear un cursor para ejecutar consultas
            cursor = conexion.cursor()

            if datos_conexion[4] != "op_sol":
                try:
                    consulta = "SELECT max(id_hecho) FROM datos_hecho"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        if fila[0]:
                            indices.append(fila[0])
                        else:
                            indices.append(0)
                except Exception:
                    self.mostrar_mensaje_advertencia(
                        "No se ha encontrado tabla 'datos_hecho'"
                    )

                try:
                    consulta = "SELECT max(id) FROM armas"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        if fila[0]:
                            indices.append(fila[0])
                        else:
                            indices.append(0)
                except Exception:
                    self.mostrar_mensaje_advertencia(
                        "No se ha encontrado tabla 'armas'"
                    )

                try:
                    consulta = "SELECT max(id) FROM automotores"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        if fila[0]:
                            indices.append(fila[0])
                        else:
                            indices.append(0)
                except Exception:
                    self.mostrar_mensaje_advertencia(
                        f"No se ha encontrado tabla 'automotores'"
                    )

                try:
                    consulta = "SELECT max(id) FROM objetos"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        if fila[0]:
                            indices.append(fila[0])
                        else:
                            indices.append(0)
                except Exception:
                    self.mostrar_mensaje_advertencia(
                        "No se ha encontrado tabla 'objetos'"
                    )

                try:
                    consulta = "SELECT max(id) FROM secuestros"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        if fila[0]:
                            indices.append(fila[0])
                        else:
                            indices.append(0)
                except Exception:
                    self.mostrar_mensaje_advertencia(
                        "No se ha encontrado tabla 'secuestros'"
                    )

                try:
                    consulta = "SELECT max(id) FROM involucrados"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        if fila[0]:
                            indices.append(fila[0])
                        else:
                            indices.append(0)
                except Exception:
                    self.mostrar_mensaje_advertencia(
                        "No se ha encontrado tabla 'involucrados'"
                    )

                try:
                    consulta = "SELECT fecha_carga FROM datos_hecho WHERE id_hecho = (SELECT max(id_hecho) FROM datos_hecho)"
                    cursor.execute(consulta)
                    ultima_fecha = cursor.fetchone()
                    ultima_fecha = ultima_fecha[0].strftime("%d %B %Y")
                except Exception as error:
                    self.mostrar_mensaje_advertencia(
                        "No se ha podido recuperar la ultima fecha cargada: \n{error}'",
                    )

                ventana.datos_de_conexion = datos_conexion
                ventana.indices = indices
                # Cerrar el cursor y la conexión
                cursor.close()
                conexion.close()

                self.btn_base.config(bg=self.verde)

                self.imprimir_con_color("Establecida conexión con base.", "verde")
                self.imprimir_con_color(f"Host: {datos_conexion[0]}", "blanco")
                self.imprimir_con_color(f"User: {datos_conexion[2]}", "blanco")
                self.imprimir_con_color(
                    f"Nombre de la base: {datos_conexion[4]}", "blanco"
                )
                self.imprimir_con_color(
                    f"Ultima fecha en base: {ultima_fecha}", "blanco"
                )

                ventana.botones[0].config(bg=self.verde)

                ventana.conexion = datos_conexion.copy()

                texto = f"Conexión satisfactoria!\n\nÚltima fecha: {ultima_fecha}\n\n"
                tags = (
                    "Hechos: ",
                    "Armas: ",
                    "Automotores: ",
                    "Objetos: ",
                    "Secuestros: ",
                    "Involucrados: ",
                )
                for i in range(0, len(indices)):
                    texto += tags[i] + str(indices[i]) + "\n"

                output.insert(tk.END, texto)
                ventana.indices = indices
            else:
                try:
                    consulta = "SELECT max(id_hecho) FROM datos_hecho"
                    cursor.execute(consulta)
                    resultados = cursor.fetchall()
                    for fila in resultados:
                        if fila[0]:
                            indices.append(fila[0])
                        else:
                            indices.append(0)
                except Exception as e:
                    self.mostrar_mensaje_advertencia(
                        f"No se ha encontrado tabla 'datos_hecho'. Error: {e}"
                    )
                try:
                    consulta = "SELECT fecha_carga FROM datos_hecho WHERE id_hecho = (SELECT max(id_hecho) FROM datos_hecho)"
                    cursor.execute(consulta)
                    ultima_fecha = cursor.fetchone()
                    ultima_fecha = ultima_fecha[0]
                except Exception as error:
                    self.mostrar_mensaje_advertencia(
                        f"No se ha podido recuperar la ultima fecha cargada: \n{error}'",
                    )
                indices.append(0)
                indices.append(0)
                indices.append(0)
                indices.append(0)
                indices.append(0)
                cursor.close()
                conexion.close()

                ventana.indices = indices
                # Cerrar el cursor y la conexión
                cursor.close()
                conexion.close()

                self.btn_base.config(bg=self.verde)

                self.imprimir_con_color("Establecida conexión con base.", "verde")
                self.imprimir_con_color(f"Host: {datos_conexion[0]}", "blanco")
                self.imprimir_con_color(f"User: {datos_conexion[2]}", "blanco")
                self.imprimir_con_color(
                    f"Nombre de la base: {datos_conexion[4]}", "blanco"
                )
                self.imprimir_con_color(
                    f"Ultima fecha en base: {ultima_fecha}", "blanco"
                )

                ventana.botones[0].config(bg=self.verde)

                ventana.conexion = datos_conexion.copy()

                texto = f"Conexión satisfactoria!\n\nÚltima fecha: {ultima_fecha}\n\n"
                tags = (
                    "Hechos: ",
                    "Armas: ",
                    "Automotores: ",
                    "Objetos: ",
                    "Secuestros: ",
                    "Involucrados: ",
                )
                for i in range(0, len(indices)):
                    texto += tags[i] + str(indices[i]) + "\n"

                output.insert(tk.END, texto)
                ventana.indices = indices
        except Exception as error:
            self.mostrar_mensaje_error(error)
            texto = "No se ha podido establecer conexión..."
            output.insert(tk.END, texto)

    def crear_base(self, host, port, user, passw, base):
        self.imprimir_con_color("Creando base de datos...", "blanco")
        self.imprimir_con_color(f"Host: {host}", "blanco")
        self.imprimir_con_color(f"Puerto: {port}", "blanco")
        self.imprimir_con_color(f"User: {user}", "blanco")
        self.imprimir_con_color(f"Nombre de la base: {base}", "blanco")
        conn = mysql.connector.connect(host=host, port=port, user=user, password=passw)
        cursor = conn.cursor()
        cursor.execute(f"SHOW DATABASES")
        databases = cursor.fetchall()
        if (base,) in databases:
            self.mostrar_mensaje_advertencia("La base de datos ya existe.")
        else:
            try:
                conn = mysql.connector.connect(
                    host=host, port=port, user=user, password=passw
                )
                conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {base}")
                conn.database = base
                cursor = conn.cursor()

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS datos_hecho (
                        id_hecho INT PRIMARY KEY,
                        nro_registro VARCHAR(30) NOT NULL,
                        fecha_carga DATE NOT NULL NOT NULL,
                        hora_carga TIME NOT NULL,
                        dependencia VARCHAR(100) NOT NULL,
                        fecha_inicio_hecho DATE,
                        hora_inicio_hecho TIME,
                        partido_hecho VARCHAR(50) NOT NULL,
                        localidad_hecho VARCHAR(50),
                        latitud VARCHAR(50),
                        calle VARCHAR(50),
                        longitud VARCHAR(50),
                        altura VARCHAR(10),
                        entre VARCHAR(50),
                        calificaciones VARCHAR(5000) NOT NULL,
                        relato VARCHAR(32767) NOT NULL
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_datos_hecho_partido_hecho ON datos_hecho(partido_hecho)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_datos_hecho_fecha_carga ON datos_hecho(fecha_carga)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_datos_hecho_localidad_hecho ON datos_hecho(localidad_hecho)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_datos_hecho_nro_registro ON datos_hecho(nro_registro)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS automotores (
                        id INT PRIMARY KEY,
                        id_hecho INT NOT NULL,
                        marca VARCHAR(50) NOT NULL,
                        modelo VARCHAR(50),
                        color VARCHAR(50),
                        dominio VARCHAR(50),
                        nro_motor VARCHAR(50),
                        nro_chasis VARCHAR(50),
                        vinculo VARCHAR(50) NOT NULL,
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_automotores_marca ON automotores(marca)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_automotores_modelo ON automotores(modelo)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_automotores_dominio ON automotores(dominio)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_automotores_vinculo ON automotores(vinculo)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS armas (
                        id INT PRIMARY KEY,
                        id_hecho INT NOT NULL,
                        tipo_arma VARCHAR(100) NOT NULL,
                        marca VARCHAR(50) NOT NULL,
                        modelo VARCHAR(50),
                        nro_serie VARCHAR(50),
                        calibre VARCHAR(50),
                        observaciones VARCHAR(1000),
                        implicacion VARCHAR(50) NOT NULL,
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_armas_marca ON armas(marca)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS secuestros (
                        id INT PRIMARY KEY,
                        id_hecho INT NOT NULL,
                        tipo VARCHAR(50) NOT NULL,
                        marca VARCHAR(50),
                        modelo VARCHAR(50),
                        cantidad VARCHAR(50),
                        valor VARCHAR(50),
                        descripcion VARCHAR(1000),
                        implicacion VARCHAR(50) NOT NULL,
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_secuestros_implicacion ON secuestros(implicacion)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS objetos (
                        id INT PRIMARY KEY,
                        id_hecho INT NOT NULL,
                        tipo VARCHAR(50) NOT NULL,
                        marca VARCHAR(50),
                        modelo VARCHAR(50),
                        cantidad VARCHAR(50),
                        valor VARCHAR(50),
                        descripcion VARCHAR(1000),
                        implicacion VARCHAR(50) NOT NULL,
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_objetos_implicacion ON objetos(implicacion)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS involucrados (
                        id INT PRIMARY KEY,
                        id_hecho INT,
                        involucrado VARCHAR(30),
                        pais_origen VARCHAR(50),
                        tipo_dni VARCHAR(10),
                        nro_dni VARCHAR(20),
                        genero VARCHAR(20),
                        apellido VARCHAR(50),
                        nombre VARCHAR(50),
                        provincia_nacimiento VARCHAR(50),
                        ciudad_nacimiento VARCHAR(50),
                        fecha_nacimiento DATE,
                        observaciones VARCHAR(1000),
                        provincia_domicilio VARCHAR(50),
                        partido_domicilio VARCHAR(50),
                        localidad_domicilio VARCHAR(50),
                        calle_domicilio VARCHAR(50),
                        nro_domicilio VARCHAR(20),
                        entre VARCHAR(50),
                        piso VARCHAR(20),
                        departamento VARCHAR(20),
                        caracteristicas_fisicas VARCHAR(500),
                        FOREIGN KEY (id_hecho) REFERENCES datos_hecho(id_hecho) ON DELETE CASCADE
                    )
                """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_involucrado ON involucrados(involucrado)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_nombre ON involucrados(nombre)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_apellido ON involucrados(apellido)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_pais_origen ON involucrados(pais_origen)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_partido_domicilio ON involucrados(partido_domicilio)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_involucrados_nro_dni ON involucrados(nro_dni)"
                )

                conn.commit()
                conn.close()
                self.mostrar_mensaje_info("Base de datos creada.")
                self.imprimir_con_color(f"Base de datos creada", "verde")
            except Exception as error:
                self.mostrar_mensaje_error(f"No se ha podido crear la base: {error}")
                self.imprimir_con_color(
                    f"No se ha podido crear la base: {error}", "rojo"
                )
