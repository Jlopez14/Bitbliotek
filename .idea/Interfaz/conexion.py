import mysql.connector

def obtener_contrasena(usuario):
    try:
        # Conectar a MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='pablo2',
            database='bitbliotek'
        )

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Consulta SELECT para obtener la contraseña de un usuario específico
        query = "SELECT contrasenna FROM usuarios WHERE email = %s"
        cursor.execute(query, (usuario,))

        # Obtener el resultado de la consulta
        resultado = cursor.fetchone()

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        if resultado:
            # Si se encuentra el usuario, retornar la contraseña
            return resultado[0]
        else:
            # Si el usuario no se encuentra, retornar None
            return None

    except mysql.connector.Error as err:
        # Manejar errores de conexión
        print(f'Error de conexión: {err}')
        return None

