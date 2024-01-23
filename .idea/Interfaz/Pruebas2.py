from kivy.app import App
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

class MyApp(App):
    def build(self):
        # Crear el diseño principal
        layout = RelativeLayout()

        try:
            Window.borderless = True
            Window.fullscreen = False
            Window.maximize = False
        except Exception as e:
            print(f"No se pudo configurar la ventana sin bordes: {e}")

        # Espaciado entre la imagen y los demás elementos
        img_spacing = 0.2

        # Espaciado entre el campo de usuario y el campo de contraseña
        input_spacing = 0.19

        # Calcular el espacio total requerido
        total_spacing = img_spacing + 2 * input_spacing

        # Centrar los demás elementos
        center_layout = RelativeLayout(size_hint=(None, None), size=(dp(300), dp(300)), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Agregar la imagen de fondo
        background = Image(source='fondointro.jpg', allow_stretch=True, keep_ratio=False, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(background)

        # Agregar una imagen principal con un tamaño específico
        img = Image(source='bibliotekBuena.png', size=(dp(320), dp(320)), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 + total_spacing / 2})  # Ajuste en 'center_y'
        center_layout.add_widget(img)

        # Campo de usuario
        user_input = TextInput(hint_text='Usuario', multiline=False, text_align='center', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing + total_spacing / 2}, size=(dp(300), dp(40)))
        center_layout.add_widget(user_input)

        # Campo de contraseña
        password_input = TextInput(hint_text='Contraseña', multiline=False, password=True, text_align='center', size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing - input_spacing + total_spacing / 2}, size=(dp(300), dp(40)))
        center_layout.add_widget(password_input)

        # Botón de aceptar
        btn_accept = Button(text='Aceptar', on_press=self.on_button_press, size_hint=(None, None), pos_hint={'center_x': 0.25, 'center_y': 0.5 - img_spacing - 2 * input_spacing + total_spacing / 2}, size=(dp(150), dp(40)))
        center_layout.add_widget(btn_accept)

        # Botón de registrar
        btn_register = Button(text='Registrar', on_press=self.on_register_press, size_hint=(None, None), pos_hint={'center_x': 0.75, 'center_y': 0.5 - img_spacing - 2 * input_spacing + total_spacing / 2}, size=(dp(150), dp(40)))
        center_layout.add_widget(btn_register)

        # Botón de salir
        btn_exit = Button(text='Salir', on_press=self.on_exit_press, size_hint=(None, None), pos_hint={'right': 1, 'bottom': 1}, size=(dp(80), dp(30)))
        layout.add_widget(btn_exit)

        layout.add_widget(center_layout)

        return layout

    def on_button_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Aceptar"
        user_text = instance.parent.children[3].text  # Obtener el texto del campo de usuario
        password_text = instance.parent.children[2].text  # Obtener el texto del campo de contraseña

        # Puedes realizar alguna acción con los datos, como imprimirlos en la consola
        print(f'Usuario: {user_text}, Contraseña: {password_text}, Acción: Aceptar')

    def on_register_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Registrar"
        user_text = instance.parent.children[3].text  # Obtener el texto del campo de usuario
        password_text = instance.parent.children[2].text  # Obtener el texto del campo de contraseña

        # Puedes realizar alguna acción con los datos, como imprimirlos en la consola
        print(f'Usuario: {user_text}, Contraseña: {password_text}, Acción: Registrar')

    def on_exit_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Salir"
        App.get_running_app().stop()

if __name__ == '__main__':
    MyApp().run()
