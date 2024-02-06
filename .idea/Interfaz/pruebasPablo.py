from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

class Inicio(App):
    def __init__(self, id_usuario, **kwargs):
        super().__init__(**kwargs)
        self.id_usuario = id_usuario

    def build(self):
        # Layout principal
        root_layout = RelativeLayout()

        background = Image(source='verdesitofondito.jpg',
                           allow_stretch=True,
                           keep_ratio=False,
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        root_layout.add_widget(background)

        # BoxLayout vertical para contener Label y botones
        vertical_layout = BoxLayout(orientation='vertical',
                                    size_hint=(None, None),
                                    size=(600, 400),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Label para mostrar el valor de id_usuario
        label_usuario = Label(text=f'ID Usuario: {self.id_usuario}', font_size=20)
        vertical_layout.add_widget(label_usuario)

        # BoxLayout horizontal para los botones
        button_layout = BoxLayout(orientation='horizontal',
                                  size_hint=(None, None),
                                  size=(600, 150),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Botones utilizando RelativeLayout
        button1 = Button(text='Música',
                         size_hint=(None, None),
                         size=(200, 150),
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(1, 0, 1, 0))
        button2 = Button(text='Películas',
                         size_hint=(None, None),
                         size=(200, 150),
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(1, 0, 1, 0))
        button3 = Button(text='Libros',
                         size_hint=(None, None),
                         size=(200, 150),
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(1, 0, 1, 0))

        # Añadir botones al BoxLayout
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        button_layout.add_widget(button3)

        # Añadir el Label y el BoxLayout de botones al layout principal
        vertical_layout.add_widget(button_layout)
        root_layout.add_widget(vertical_layout)

        # Botón de salida en la parte inferior
        exit_button = Button(text='Salir',
                             size_hint=(None, None),
                             size=(150, 40),
                             pos_hint={'center_x': 0.5, 'y': 0.1},
                             background_color=(0.12, 0.25, 0.21, 1),
                             border=(1, 0, 1, 0))

        root_layout.add_widget(exit_button)

        return root_layout

if __name__ == '__main__':
    Inicio(id_usuario='123').run()  # Puedes cambiar '123' por el valor real de id_usuario
