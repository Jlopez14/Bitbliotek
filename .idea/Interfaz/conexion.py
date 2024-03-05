import mysql.connector

# Configuración de la conexión a la base de datos
configuracion_db = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pablo2',
    'database': 'bitbliotek'
}

def obtener_contrasena(usuario):
    try:
        # Conectar a MySQL utilizando la configuración global
        connection = mysql.connector.connect(**configuracion_db)
        cursor = connection.cursor()

        query = "SELECT contrasenna FROM usuarios WHERE email = %s"
        cursor.execute(query, (usuario,))
        resultado = cursor.fetchone()

        cursor.close()
        connection.close()

        if resultado:
            return resultado[0]
        else:
            return None

    except mysql.connector.Error as err:
        print(f'Error de conexión: {err}')
        return None

def registrar(nombre, apellidos, correo, contrasenna):
    try:
        # Conectar a MySQL utilizando la configuración global
        conexion = mysql.connector.connect(**configuracion_db)
        cursor = conexion.cursor()

        sql_insert = "INSERT INTO usuarios (nombre, apellidos, email, contrasenna) VALUES (%s, %s, %s, %s)"
        datos = (nombre, apellidos, correo, contrasenna)

        cursor.execute(sql_insert, datos)
        conexion.commit()

        print(f"Registro insertado correctamente en la tabla 'usuarios'")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conexion.close()

def obtenerID(usuario):
    try:
        # Conectar a MySQL utilizando la configuración global
        connection = mysql.connector.connect(**configuracion_db)
        cursor = connection.cursor()

        query = "SELECT idusuarios FROM usuarios WHERE email = %s"
        cursor.execute(query, (usuario,))
        resultado = cursor.fetchone()

        cursor.close()
        connection.close()

        if resultado:
            return resultado[0]
        else:
            return None

    except mysql.connector.Error as err:
        print(f'Error de conexión: {err}')
        return None


def obtenerNombre(id):
    try:
        # Conectar a MySQL utilizando la configuración global
        connection = mysql.connector.connect(**configuracion_db)
        cursor = connection.cursor()

        query = "SELECT concat(nombre,' ',apellidos) FROM usuarios WHERE idusuarios = %s"
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()

        cursor.close()
        connection.close()

        if resultado:
            return resultado[0]
        else:
            return None

    except mysql.connector.Error as err:
        print(f'Error de conexión: {err}')
        return None



# Ejemplos de uso
# obtener_contrasena('usuario1')
# registrar('Nombre', 'Apellido', 'correo@example.com', 'contrasenna')
# obtenerID('usuario1')
