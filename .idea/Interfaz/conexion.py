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



def registrar(nombre, apellidos, correo, contrasenna):
    # Configuración de la conexión a la base de datos
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'pablo2',
        'database': 'bitbliotek'
    }

    try:
        # Establecer conexión a la base de datos
        conexion = mysql.connector.connect(**config)

        # Crear un objeto cursor para ejecutar consultas SQL
        cursor = conexion.cursor()

        # Ejemplo de INSERT INTO
        inombre = nombre
        iapellidos = apellidos
        icorreo = correo
        icontrasenna = contrasenna

        # Sentencia SQL con placeholders para evitar SQL injection
        sql_insert = "INSERT INTO usuarios (nombre, apellidos, email, contrasenna) VALUES (%s, %s, %s, %s)"

        # Datos a insertar
        datos = (inombre, iapellidos, icorreo, icontrasenna)

        # Ejecutar la consulta
        cursor.execute(sql_insert, datos)

        # Confirmar la transacción
        conexion.commit()

        print(f"Registro insertado correctamente en la tabla 'usuarios'")
    except mysql.connector.Error as err:
        # Manejar errores
        print(f"Error: {err}")
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()


def obtenerID(usuario):
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
        query = "SELECT idusuarios FROM usuarios WHERE email = %s"
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

