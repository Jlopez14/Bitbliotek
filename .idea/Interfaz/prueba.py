from kivy.app import App
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from conexion import obtener_contrasena
from kivy.uix.popup import Popup
from kivy.uix.label import Label





class MyApp(App):

    def mostrar_popup(self, mensaje):
        popup = Popup(title='Error de Autenticación',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()


    def build(self):
        # Crear el diseño principal
        layout = RelativeLayout()

        # Agregar la imagen de fondo
        background = Image(source='fondointro.jpg', allow_stretch=True, keep_ratio=False, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(background)

        # Centrar los demás elementos
        center_layout = RelativeLayout(size_hint=(None, None), size=(dp(500), dp(400)), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Agregar una imagen principal con un tamaño específico
        img = Image(source='bibliotekBuena.png', size=(dp(400), dp(400)), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.6})  # Ajuste en 'center_y'
        center_layout.add_widget(img)

        # Espaciado entre la imagen y los demás elementos
        img_spacing = 0.01

        # Campo de usuario
        user_input = TextInput(hint_text='Usuario', multiline=False, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing}, size=(dp(300), dp(40)))
        center_layout.add_widget(user_input)

        # Espaciado entre el campo de usuario y el campo de contraseña
        input_spacing = 0.25

        # Campo de contraseña
        password_input = TextInput(hint_text='Contraseña', multiline=False, password=True, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing - input_spacing}, size=(dp(300), dp(40)))
        center_layout.add_widget(password_input)

        # Botón de aceptar
        btn_accept = Button(text='Aceptar', on_press=self.on_button_press, size_hint=(None, None), pos_hint={'center_x': 0.4, 'center_y': 0.5 - img_spacing - 2 * input_spacing}, size=(dp(150), dp(40)))
        center_layout.add_widget(btn_accept)

        # Botón de registrar
        btn_register = Button(text='Registrar', on_press=self.on_register_press, size_hint=(None, None), pos_hint={'center_x': 0.6, 'center_y': 0.5 - img_spacing - 2 * input_spacing}, size=(dp(150), dp(40)))
        center_layout.add_widget(btn_register)

        layout.add_widget(center_layout)

        return layout

    def on_button_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Aceptar"
        user_text = instance.parent.children[3].text  # Obtener el texto del campo de usuario
        password_text = instance.parent.children[2].text  # Obtener el texto del campo de contraseña

        contrasenna=obtener_contrasena(user_text)

        if password_text!=contrasenna:
            self.mostrar_popup("Contraseña incorrecta")



    def on_register_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Registrar"
        user_text = instance.parent.children[2].text  # Obtener el texto del campo de usuario
        password_text = instance.parent.children[3].text  # Obtener el texto del campo de contraseña

        # Puedes realizar alguna acción con los datos, como imprimirlos en la consola
        print(f'Usuario: {user_text}, Contraseña: {password_text}, Acción: Registrar')


if __name__ == '__main__':
    MyApp().run()
