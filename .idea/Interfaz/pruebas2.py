import kivy
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class VentanaApp(App):
    def build(self):
        # Crear el diseño principal
        layout = RelativeLayout()

        # Agregar la imagen de fondo


        # Centrar los demás elementos
        center_layout = RelativeLayout(size_hint=(None, None), size=(300, 200), pos_hint={'center_x': 0.5, 'center_y': 0.5})



        # Espaciado entre la imagen y los demás elementos
        img_spacing = 0.01

        # Crear los botones con imágenes y ajustar el tamaño
        button1 = self.crear_boton_con_imagen('imagen1.png', size_hint=(None, None), size=(300, 300))

        img_spacing = 10.01
        button2 = self.crear_boton_con_imagen('imagen2.png', size_hint=(None, None), size=(300, 300))

        img_spacing = 10.01

        button3 = self.crear_boton_con_imagen('imagen3.png', size_hint=(None, None), size=(300, 300))

        # Agregar los botones a la disposición
        center_layout.add_widget(button1)
        center_layout.add_widget(button2)
        center_layout.add_widget(button3)

        return center_layout

    def crear_boton_con_imagen(self, imagen_path, **kwargs):
        # Crear un botón con una imagen y ajustar el tamaño
        button = Button(background_normal=imagen_path, background_down=imagen_path, **kwargs)
        button.bind(size=self.size_callback)  # Vincular el método de devolución de llamada al cambio de tamaño

        return button

    def size_callback(self, instance, value):
        # Ajustar el tamaño del botón según el tamaño de la imagen
        instance.size = instance.background_normal_size

if __name__ == '__main__':
    VentanaApp().run()
