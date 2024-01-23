from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image

class MyApp(App):
    def build(self):
        # Layout principal
        root_layout = RelativeLayout()

        background = Image(source='fondointro.jpg', 
                           allow_stretch=True, 
                           keep_ratio=False, 
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        root_layout.add_widget(background)

        # Botones utilizando RelativeLayout
        button_size = (400, 150)
        button1 = Button(text='Música', 
                         size_hint=(None, None), 
                         size=button_size, 
                         pos_hint={'center_x': 0.5, 'center_y': 0.75},  # Ajustar la posición y hacia arriba
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(2, 2, 2, 2))
        button2 = Button(text='Películas', 
                         size_hint=(None, None), 
                         size=button_size, 
                         pos_hint={'center_x': 0.5, 'center_y': 0.55},  # Ajustar la posición y hacia arriba
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(2, 2, 2, 2))
        button3 = Button(text='Libros', 
                         size_hint=(None, None), 
                         size=button_size, 
                         pos_hint={'center_x': 0.5, 'center_y': 0.35},  # Ajustar la posición y hacia arriba
                         background_color=(0.53, 0.86, 0.83, 1),
                         border=(2, 2, 2, 2))

        # Botón de salida en la parte inferior
        exit_button = Button(text='Salir', 
                             size_hint=(None, None), 
                             size=(150, 40), 
                             pos_hint={'center_x': 0.5, 'y': 0.1},  # Ajustar la posición y hacia abajo
                             background_color=(0.12, 0.25, 0.21, 1))

        # Añadir botones al layout principal
        root_layout.add_widget(button1)
        root_layout.add_widget(button2)
        root_layout.add_widget(button3)
        root_layout.add_widget(exit_button)

        return root_layout

if __name__ == '__main__':
    MyApp().run()
