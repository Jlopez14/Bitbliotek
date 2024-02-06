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
        buttons_layout.add_widget(Button(text='Registrar', on_press=self.on_register_press, size_hint=(None, None), height=dp(40)))

        # Agregar el botón "Cerrar" a la derecha y un poco más a la derecha
        buttons_layout.add_widget(Button(text='Cerrar', on_press=self.on_close_press, size_hint=(None, None), height=dp(40), pos_hint={'right': 1}))
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

        elif username == '' or lastname == '' or email == '' or password == '' or repassword == '':
            self.mostrar_popup("Por favor complete todos los campos")

        else:
            registrar(username,lastname,email,password)
            self.mostrar_popup("Usuario registrado correctamente")
            App.get_running_app().stop()
            Login().run()

    def on_close_press(self, instance):
        App.get_running_app().stop()
        Login().run()

#Clase principal donde está la ventana 1
class Login(App):
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
        btn_accept = Button(text='Aceptar', on_press=self.on_button_press, size_hint=(None, None), pos_hint={'center_x': 0.25, 'center_y': 0.5 - img_spacing - 2 * input_spacing}, size=(dp(150), dp(40)))
        center_layout.add_widget(btn_accept)

        # Botón de registrar
        btn_register = Button(text='Registrar', on_press=self.on_register_press, size_hint=(None, None), pos_hint={'center_x': 0.75, 'center_y': 0.5 - img_spacing - 2 * input_spacing}, size=(dp(150), dp(40)))
        center_layout.add_widget(btn_register)

        # Botón de salir
        btn_exit = Button(text='Salir', on_press=self.on_exit_press, size_hint=(None, None), pos_hint={'right': 1, 'bottom': 1}, size=(dp(80), dp(30)))
        layout.add_widget(btn_exit)

        layout.add_widget(center_layout)

        return layout

    def on_register_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Registrar"
        # Crear y mostrar la ventana de registro
        registration_window = RegistrationWindow()
        popup = Popup(title='Registro de usuario', content=registration_window, size_hint=(None, None), size=(dp(500), dp(500),))
        popup.open()

    def on_button_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Aceptar"
        user_text = instance.parent.children[3].text  # Obtener el texto del campo de usuario
        password_text = instance.parent.children[2].text  # Obtener el texto del campo de contraseña

        contrasenna=obtener_contrasena(user_text)
        id=obtenerID(user_text) #Obtiene el ID


        App.get_running_app().stop #Cierra la ventana actual
        Inicio(id).run() #Abre la nueva ventana mandando el ID

        if password_text!=contrasenna:
            self.mostrar_popup("Usuario y/o contraseña incorrecta")


    def on_exit_press(self, instance):
        # Acción a realizar cuando se presiona el botón "Cerrar" en la ventana emergente
        if self.popup_instance:
            self.popup_instance.dismiss()

if __name__ == '__main__':
    Login().run()
