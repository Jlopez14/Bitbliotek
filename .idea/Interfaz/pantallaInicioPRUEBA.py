from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp

class Inicio(App):
    def build(self):
        Window.fullscreen = 'auto'  # Configura la aplicación para abrirse a pantalla completa
        Window.show_cursor = True   # Muestra el cursor en pantalla completa

        # Layout principal
        root_layout = RelativeLayout()

        background = Image(source='verdesitofondito.jpg',
                           allow_stretch=True,
                           keep_ratio=False,
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        root_layout.add_widget(background)



            # Calcula la posición y el tamaño de la imagen
        margen_izquierdo = 5  # 5 centímetros desde el margen izquierdo
        margen_superior = Window.height - 4 - 4  # 4 centímetros desde el margen superior

        # Tamaño de la imagen: 5x5 centímetros
        ancho_imagen_cm = 5
        alto_imagen_cm = 5

        # Convertir centímetros a proporciones relativas
        ancho_imagen_rel = ancho_imagen_cm / Window.width
        alto_imagen_rel = alto_imagen_cm / Window.height

        # Imagen
        imagen = Image(source='bibliotekCabecera.png',
                    allow_stretch=True,
                    keep_ratio=False,
                    size_hint=(ancho_imagen_rel, alto_imagen_rel),
                    pos_hint={'x': margen_izquierdo / Window.width, 'top': 1 - margen_superior / Window.height})

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

        # Cuadro de texto en la esquina superior derecha
        text_input = TextInput(text='',
                               size_hint=(0.1, 0.05),
                               pos_hint={'top': 1, 'right': 1},
                               multiline=False,
                               border=(2, 2, 2, 2))
        root_layout.add_widget(text_input)

        # Añadir el layout centrado al layout principal
        root_layout.add_widget(container_layout)

        return root_layout

    def on_exit_press(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':
    Inicio().run()
