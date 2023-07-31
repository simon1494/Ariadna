if __name__ == "__main__":
    import mysql.connector

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="delitos",
    )

    cursor = conexion.cursor()

    consulta = (
        r"SELECT * FROM involucrados WHERE provincia_nacimiento LIKE '%Ciudad Natal%'"
    )

    cursor.execute(consulta)

    data = cursor.fetchall()
    indices_recogidos = []
    for i in data:
        indices_recogidos.append(i[0])

    contador_regresivo = len(indices_recogidos)
    for indice in indices_recogidos:

        consulta = rf"SELECT * FROM involucrados WHERE id = {indice}"
        cursor.execute(consulta)
        registro = cursor.fetchone()
        info = registro[9].split(" Ciudad Natal: ")
        consulta2 = rf""" UPDATE involucrados
                    SET provincia_nacimiento = "{info[0]}", ciudad_nacimiento = "{info[1]}" 
                    WHERE id = {indice}"""
        cursor.execute(consulta2)
        contador_regresivo -= 1
        print(f"Faltan {contador_regresivo-1}")
    print("ejecutando commit...")
    conexion.commit()
    print("Listo commit")
    conexion.close()
