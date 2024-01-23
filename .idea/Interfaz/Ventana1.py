from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyApp(App):
    def build(self):
        # Crear el diseño principal
        layout = RelativeLayout()

        # Agregar la imagen de fondo
        background = Image(source='C:\\Users\\lopez.lujos\\Desktop\\ProyectoPython\\fondointro.jpg', allow_stretch=True, keep_ratio=False, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(background)

        # Centrar los demás elementos
        center_layout = RelativeLayout(size_hint=(None, None), size=(300, 200), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Agregar una imagen principal con un tamaño específico
        img = Image(source='C:\\Users\\lopez.lujos\\Desktop\\ProyectoPython\\bibliotekBuena.png', size=(2000, 2000), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.6})  # Ajuste en 'center_y'
        center_layout.add_widget(img)

        # Espaciado entre la imagen y los demás elementos
        img_spacing = 0

        # Campo de usuario
        user_input = TextInput(hint_text='Usuario', multiline=False, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing}, size=(300, 40))
        center_layout.add_widget(user_input)

        # Espaciado entre el campo de usuario y el campo de contraseña
        input_spacing = 0.25

        # Campo de contraseña
        password_input = TextInput(hint_text='Contraseña', multiline=False, password=True, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing - input_spacing}, size=(300, 40))
        center_layout.add_widget(password_input)

        # Botón de aceptar
        btn_accept = Button(text='Aceptar', on_press=self.on_button_press, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing - 2 * input_spacing}, size=(200, 40))
        center_layout.add_widget(btn_accept)

        layout.add_widget(center_layout)

        return layout

    def on_button_press(self, instance):
        # Acción a realizar cuando se presiona el botón
        user_text = instance.parent.children[2].text  # Obtener el texto del campo de usuario
        password_text = instance.parent.children[3].text  # Obtener el texto del campo de contraseña

        # Puedes realizar alguna acción con los datos, como imprimirlos en la consola
        print(f'Usuario: {user_text}, Contraseña: {password_text}')

if __name__ == '__main__':
    MyApp().run()
