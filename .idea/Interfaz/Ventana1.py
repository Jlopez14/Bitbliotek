
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from ventana2 import RegistrationWindow

class Window1(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ... (resto del código de Window1)

    def on_register_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Registrar"
        # Crear y mostrar la ventana de registro
        registration_window = RegistrationWindow()
        popup = Popup(title='Registro', content=registration_window, size_hint=(None, None), size=(dp(300), dp(400)))
        popup.open()

    def on_button_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Aceptar"
        user_text = instance.parent.children[3].text  # Obtener el texto del campo de usuario
        password_text = instance.parent.children[2].text  # Obtener el texto del campo de contraseña

        # Puedes realizar alguna acción con los datos, como imprimirlos en la consola
        print(f'Usuario: {user_text}, Contraseña: {password_text}, Acción: Aceptar')

    def on_exit_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Salir"
        App.get_running_app().stop()

if __name__ == '__main__':
    Window1().run()
