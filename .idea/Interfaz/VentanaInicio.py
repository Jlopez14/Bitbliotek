from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp
from conexion import obtenerNombre

class Inicio(App):

    def __init__(self, id, **kwargs):
        super(Inicio, self).__init__(**kwargs)
        self.id = id

    def build(self):
        Window.fullscreen = 'auto'  # Configura la aplicación para abrirse a pantalla completa
        Window.show_cursor = True   # Muestra el cursor en pantalla completa

        # Layout principal
        root_layout = RelativeLayout()

        # Fondo de la ventana
        background = Image(source='verdesitofondito.jpg',
                           allow_stretch=True,
                           keep_ratio=False,
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        root_layout.add_widget(background)

        # Agregar imagen en la parte superior de la pantalla
        logo_image = Image(source='Cabecera.png',  # Ruta de la imagen
                           size_hint=(None, None),  # Deshabilitar el ajuste automático del tamaño
                           size=(1000, 600),  # Tamaño de la imagen triplicado (200 * 3)
                           pos_hint={'center_x': 0.35, 'top': 1.1})  # Posicionar en la parte superior de la pantalla
        root_layout.add_widget(logo_image)


        # BoxLayout vertical para centrar los elementos
        container_layout = BoxLayout(orientation='vertical',
                                     size_hint=(0.8, 0.8),  # Ajusta el tamaño de la ventana principal
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # BoxLayout horizontal para los botones
        button_layout = BoxLayout(orientation='horizontal',
                                  size_hint=(1, 0.5),  # Ajusta la altura del layout
                                  spacing=10)

        # Botones utilizando RelativeLayout

        button1 = Button(size_hint=(1/3, 0.7),
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(1, 0, 1, 0),
                         background_normal='musica.png',  # Nombre de la imagen de fondo normal
                         background_down='musicaPresionada.png')

        button2 = Button(size_hint=(1/3, 0.7),
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(1, 0, 1, 0),
                         background_normal='cine.png',  # Nombre de la imagen de fondo normal
                         background_down='cinePresionado.png')

        button3 = Button(size_hint=(1/3, 0.7),
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(1, 0, 1, 0),
                         background_normal='libro.png',  # Nombre de la imagen de fondo normal
                         background_down='libroPresionado.png')


        # Añadir botones al BoxLayout
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        button_layout.add_widget(button3)

        # Añadir el BoxLayout de los botones al layout principal
        container_layout.add_widget(button_layout)

        # Botón de salida en la esquina inferior derecha
        exit_button = Button(text='Salir',
                             on_press=self.on_exit_press,
                             size_hint=(None, None),
                             size=(dp(80), dp(30)),
                             pos_hint={'right': 1, 'bottom': 1},
                             background_color=(0.12, 0.25, 0.21, 1),
                             border=(1, 0, 1, 0))
        root_layout.add_widget(exit_button)

        nombre_usuario=obtenerNombre(self.id)
        print(self.id)

        # Cuadro de texto en la esquina superior derecha
        text_input = TextInput(text=str(nombre_usuario),
                               size_hint=(0.14, 0.09),  # Aumentar el tamaño en un 40%
                               pos_hint={'top': 0.96, 'right': 0.96},  # Separar 4 centímetros de arriba y del margen derecho
                               multiline=False,
                               border=(2, 2, 2, 2))
        root_layout.add_widget(text_input)


        # Añadir el layout centrado al layout principal
        root_layout.add_widget(container_layout)

        return root_layout

    def on_exit_press(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':
    Inicio().run(self.id)