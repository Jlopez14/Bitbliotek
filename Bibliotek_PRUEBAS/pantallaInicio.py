from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class VentanaPrincipal(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Configurar fondo del FloatLayout
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Color blanco en formato RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Crear FloatLayout para contener los botones
        contenedor_botones = FloatLayout(size_hint=(1, 1))

        # Botones de categorías en Kivy
        boton_libros = Button(text="Libros", 
                              on_press=self.mostrar_libros, 
                              size_hint=(None, None), 
                              size=(200, 80), 
                              pos_hint={'center_x': 0.5, 'center_y': 0.7})
        boton_musica = Button(text="Música", 
                              on_press=self.mostrar_musica, 
                              size_hint=(None, None), 
                              size=(200, 80), 
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        boton_peliculas = Button(text="Películas", 
                                 on_press=self.mostrar_peliculas, 
                                 size_hint=(None, None), 
                                 size=(200, 80), 
                                 pos_hint={'center_x': 0.5, 'center_y': 0.3})

        # Botón de salir en Kivy
        boton_salir = Button(text="Salir", 
                             on_press=self.salir, 
                             size_hint=(None, None), 
                             size=(200, 80), 
                             pos_hint={'x': 0, 'y': 0})

        # Añadir widgets al FloatLayout contenedor
        contenedor_botones.add_widget(boton_libros)
        contenedor_botones.add_widget(boton_musica)
        contenedor_botones.add_widget(boton_peliculas)
        contenedor_botones.add_widget(boton_salir)

        # Añadir FloatLayout contenedor al layout principal
        self.add_widget(contenedor_botones)

    def mostrar_libros(self, instance):
        # Lógica para mostrar la ventana de libros
        pass

    def mostrar_musica(self, instance):
        # Lógica para mostrar la ventana de música
        pass

    def mostrar_peliculas(self, instance):
        # Lógica para mostrar la ventana de películas
        pass

    def salir(self, instance):
        # Lógica para salir de la aplicación
        App.get_running_app().stop()

class MiApp(App):
    def build(self):
        return VentanaPrincipal()

if __name__ == '__main__':
    MiApp().run()
