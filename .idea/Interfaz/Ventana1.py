from kivy.app import App
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from conexion import obtener_contrasena
from conexion import obtenerID
from kivy.uix.widget import Widget
from conexion import registrar
from VentanaInicio import Inicio

class RegistrationWindow(BoxLayout):

    def mostrar_popup(self, mensaje):
        popup = Popup(title='Error de Autenticación',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (dp(20), dp(2))


        # Mueve la ventana emergente un poco más arriba
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Agregar etiquetas y campos de registro
        self.add_widget(Label(text='Nombre de usuario:', size_hint=(None, None), height=dp(36), pos_hint={'center_x': 0.5}, font_size=14, bold=True))
        self.username_input = TextInput(hint_text='Ingrese su nombre de usuario', multiline=False, size_hint=(1, None), height=dp(40), pos_hint={'center_x': 0.5})
        self.add_widget(self.username_input)

        self.add_widget(Label(text='Apellidos de usuario:', size_hint=(None, None), height=dp(36), pos_hint={'center_x': 0.5}, font_size=14, bold=True))
        self.lastname_input = TextInput(hint_text='Ingrese su apellido de usuario', multiline=False, size_hint=(1, None), height=dp(40), pos_hint={'center_x': 0.5})
        self.add_widget(self.lastname_input)

        self.add_widget(Label(text='Correo electrónico:', size_hint=(None, None), height=dp(36), pos_hint={'center_x': 0.5}, font_size=14, bold=True))
        self.email_input = TextInput(hint_text='Ingrese su correo electrónico', multiline=False, size_hint=(1, None), height=dp(40), pos_hint={'center_x': 0.5})
        self.add_widget(self.email_input)

        self.add_widget(Label(text='Contraseña:', size_hint=(None, None), height=dp(36), pos_hint={'center_x': 0.5}, font_size=14, bold=True))
        self.password_input = TextInput(hint_text='Ingrese su contraseña', multiline=False, password=True, size_hint=(1, None), height=dp(40), pos_hint={'center_x': 0.5})
        self.add_widget(self.password_input)

        self.add_widget(Label(text='Repite Contraseña:', size_hint=(None, None), height=dp(36), pos_hint={'center_x': 0.5}, font_size=14, bold=True))
        self.password2_input = TextInput(hint_text='Repita su contraseña', multiline=False, password=True, size_hint=(1, None), height=dp(40), pos_hint={'center_x': 0.5})
        self.add_widget(self.password2_input)
        # Agregar un espacio vertical
        self.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Agregar botones en la misma línea horizontal
        buttons_layout = BoxLayout(size_hint=(1, None), height=dp(40), spacing=236, pos_hint={'center_x': 0.5})

        # Botón de Registrar
        btn_register = Button(text='Registrar',
                              on_press=self.on_register_press,
                              size_hint=(None, None),
                              height=dp(40))
        # Establecer el color de fondo a negro
        btn_register.background_color = (0, 0, 0, 1)  # Negro (RGBA)
        # Establecer el color del texto a verde
        btn_register.color = (0.494, 0.851, 0.341, 1)  # Verde (RGBA)
        buttons_layout.add_widget(btn_register)

        # Botón de Cerrar
        btn_close = Button(text='Cerrar',
                           on_press=self.on_close_press,
                           size_hint=(None, None),
                           height=dp(40))

        # Establecer el color de fondo a negro
        btn_close.background_color = (0, 0, 0, 1)  # Negro (RGBA)
        # Establecer el color del texto a verde
        btn_close.color = (0.494, 0.851, 0.341, 1)  # Verde (RGBA)
        buttons_layout.add_widget(btn_close)
        self.add_widget(buttons_layout)

    def on_register_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Registrar" en la ventana de registro
        username = self.username_input.text
        lastname = self.lastname_input.text
        email = self.email_input.text
        password = self.password_input.text
        repassword = self.password2_input.text

        if password != repassword:
            self.mostrar_popup("Las contraseñas no coinciden")
        elif not email or '@' not in email:
            self.mostrar_popup("Ingrese un correo electrónico válido")
        elif not username or not lastname or not email or not password or not repassword:
            self.mostrar_popup("Por favor complete todos los campos")
        elif any(char.isdigit() for char in username) or any(char.isdigit() for char in lastname):
            self.mostrar_popup("Los campos de nombre y apellidos\n"
                               "no pueden contener números")
        elif any(char.isspace() for char in username)  or any(char.isspace() for char in email) or any(char.isspace() for char in password):
            self.mostrar_popup("Los campos no pueden contener espacios en blanco")
        elif len(password) < 6:
            self.mostrar_popup("La contraseña debe tener al menos 6 caracteres")
        else:
            registrar(username, lastname, email, password)
            self.mostrar_popup("Usuario registrado correctamente")
            App.get_running_app().stop()
            Login().run()
    def on_close_press(self, instance):
        App.get_running_app().stop()
        Login().run()


#Clase principal donde está la ventana 1
class Login(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.registration_window = None  # Añade una variable para la ventana de registro

    def mostrar_popup(self, mensaje):
        popup = Popup(title='Error de Autenticación',
                      content=Label(text=mensaje),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def build(self):

        # Crear el diseño principal
        layout = RelativeLayout()

        try:
            Window.borderless = True
            Window.fullscreen = False
            Window.maximize = False
        except Exception as e:
            print(f"No se pudo configurar la ventana sin bordes: {e}")

        # Centrar los demás elementos
        center_layout = RelativeLayout(size_hint=(None, None), size=(dp(300), dp(300)), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Agregar la imagen de fondo
        background = Image(source='verdesitofondito.jpg', allow_stretch=True, keep_ratio=False, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(background)

        # Agregar una imagen principal con un tamaño específico
        img = Image(source='biblioteknegro.png', size=(dp(350), dp(350)), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.80})  # Ajuste en 'center_y'
        center_layout.add_widget(img)

        # Espaciado entre la imagen y los demás elementos
        img_spacing = 0.40

        # Campo de usuario
        user_input = TextInput(hint_text='Usuario', multiline=False, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing}, size=(dp(300), dp(40)))
        center_layout.add_widget(user_input)

        # Espaciado entre el campo de usuario y el campo de contraseña
        input_spacing = 0.19

        # Campo de contraseña
        password_input = TextInput(hint_text='Contraseña', multiline=False, password=True, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5 - img_spacing - input_spacing}, size=(dp(300), dp(40)))
        center_layout.add_widget(password_input)

        # Botón de aceptar
        btn_accept = Button(text='Aceptar',
                            on_press=self.on_button_press,
                            size_hint=(None, None),
                            pos_hint={'center_x': 0.25, 'center_y': 0.5 - img_spacing - 2 * input_spacing},
                            size=(dp(150), dp(40)))

        # Establecer el color de fondo a negro
        btn_accept.background_color = (0, 0, 0, 1)  # Negro (RGBA)

        # Establecer el color del texto a verde
        btn_accept.color = (0.494, 0.851, 0.341, 1)  # Verde (RGBA)

        center_layout.add_widget(btn_accept)

        # Botón de registrar
        btn_register = Button(text='Registrar',
                              on_press=self.on_register_press,
                              size_hint=(None, None),
                              pos_hint={'center_x': 0.75, 'center_y': 0.5 - img_spacing - 2 * input_spacing},
                              size=(dp(150), dp(40)))

        # Establecer el color de fondo a negro
        btn_register.background_color = (0, 0, 0, 1)  # Negro (RGBA)

        # Establecer el color del texto a verde
        btn_register.color = (0.494, 0.851, 0.341, 1)  # Verde (RGBA)

        center_layout.add_widget(btn_register)

        # Botón de salir
        btn_exit = Button(text='Salir',
                          on_press=self.on_exit_press,
                          size_hint=(None, None),
                          pos_hint={'right': 1, 'bottom': 1},
                          size=(dp(80), dp(30)))

        # Establecer el color de fondo a negro
        btn_exit.background_color = (0, 0, 0, 1)  # Negro (RGBA)
        # Establecer el color del texto a verde
        btn_exit.color = (0.494, 0.851, 0.341, 1)  # Verde (RGBA)
        layout.add_widget(btn_exit)

        layout.add_widget(center_layout)

        return layout

    def on_register_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Registrar"
        # Crear y mostrar la ventana de registro
        registration_window = RegistrationWindow()
        popup = Popup(title='Registro de usuario', content=registration_window, size_hint=(None, None), size=(dp(500), dp(500)))

        # Ajustar el estilo del popup
        popup.background_color = [0.49411764705882355, 0.8509803921568627, 0.3411764705882353, 1]  # Fondo verde
        popup.title_color = [1, 1, 1, 1]  # Color del texto del título (blanco)
        popup.separator_color = [1, 1, 1, 1]  # Color del separador (blanco)
        popup.open()

    def on_button_press(self, instance):
        print("Botón presionado")
        # Acción a realizar cuando se presiona el botón "Aceptar"
        user_text = instance.parent.children[3].text  # Obtener el texto del campo de usuario
        password_text = instance.parent.children[2].text  # Obtener el texto del campo de contraseña


        contrasenna = obtener_contrasena(user_text)
        id_usuario = obtenerID(user_text)  # Obtener el ID del usuario

        if password_text != contrasenna:
            self.mostrar_popup("Usuario y/o contraseña incorrecta")

        else:
            print("ELSE ")
            App.get_running_app().stop()
            Inicio(id=id_usuario).run()

    def on_exit_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Cerrar" en la ventana emergente
        App.get_running_app().stop()


if __name__ == '__main__':
    Login().run()