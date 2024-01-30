from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp

class RegistrationWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ... (resto del código de RegistrationWindow)

    def on_register_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Registrar" en la ventana de registro
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        # Puedes realizar alguna acción con los datos, como imprimirlos en la consola
        print(f'Nuevo Usuario: {username}, Correo electrónico: {email}, Nueva Contraseña: {password}')

        # Aquí podrías agregar lógica adicional, como almacenar la información en una base de datos, etc.

        # Puedes realizar alguna acción con los datos, como imprimirlos en la consola
        print(f'Nuevo Usuario: {username}, Correo electrónico: {email}, Nueva Contraseña: {password}')

if __name__ == '__main__':
    RegistrationWindow().run()
