# Importar las bibliotecas necesarias de Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


import mysql.connector

def obtener_contrasena(usuario):
    try:
        # Conectar a MySQL
        connection = mysql.connector.connect(
            host='tu_host_mysql',
            user='tu_usuario_mysql',
            password='tu_contrasena_mysql',
            database='tu_base_de_datos'
        )

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Consulta SELECT para obtener la contraseña de un usuario específico
        query = "SELECT contrasena FROM usuarios WHERE nombre_usuario = %s"
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

# Ejemplo de uso
usuario_buscado = 'nombre_de_usuario'
contrasena_obtenida = obtener_contrasena(usuario_buscado)

if contrasena_obtenida is not None:
    print(f'La contraseña de {usuario_buscado} es: {contrasena_obtenida}')
else:
    print(f'No se encontró el usuario {usuario_buscado}')


# Importar la biblioteca para la conexión a MySQL
import mysql.connector

class MyApp(App):
    def build(self):
        # Crear un diseño en caja vertical
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Crear campos de entrada
        self.username_input = TextInput(hint_text='Usuario')
        self.password_input = TextInput(hint_text='Contraseña', password=True)

        # Crear un botón para realizar la conexión
        connect_button = Button(text='Conectar a MySQL', on_press=self.connect_to_mysql)

        # Crear una etiqueta para mostrar el resultado de la conexión
        self.result_label = Label(text='Esperando conexión...')

        # Agregar los widgets al diseño
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(connect_button)
        layout.add_widget(self.result_label)

        return layout

    def connect_to_mysql(self, instance):
        # Obtener datos del usuario y contraseña
        user = self.username_input.text
        password = self.password_input.text

        # Intentar realizar la conexión a MySQL
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user=user,
                password=password,
                database='bitbliotek'
            )

            # Actualizar la etiqueta con el resultado
            self.result_label.text = 'Conexión exitosa.'

            # Aquí podrías realizar más operaciones en la base de datos si es necesario.

        except mysql.connector.Error as err:
            # Manejar errores de conexión
            self.result_label.text = f'Error de conexión: {err}'

# Instanciar y ejecutar la aplicación
if __name__ == '__main__':
    MyApp().run()
