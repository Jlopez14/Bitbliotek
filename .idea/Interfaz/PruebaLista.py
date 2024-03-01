import mysql.connector
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


class ImageButton(ButtonBehavior, Image):
    pass


class CustomScrollView(ScrollView):
    def on_scroll_wheel(self, instance, value):
        super().on_scroll_wheel(instance, value)


class Musica(App):
    def __init__(self, **kwargs):
        super(Musica, self).__init__(**kwargs)

    def build(self):
        Window.fullscreen = 'auto'
        Window.show_cursor = True

        with mysql.connector.connect(
                host="localhost",
                user="root",
                password="pablo2",
                database="bitbliotek",
        ) as conexion:
            cursor = conexion.cursor()
            consulta = "SELECT * FROM musica"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]

            root_layout = RelativeLayout()

            background = Image(source='verdesitofondito.jpg',
                               allow_stretch=True,
                               keep_ratio=False,
                               pos_hint={'center_x': 0.5, 'center_y': 0.5})
            root_layout.add_widget(background)

            logo_image = Image(source='Cabecera.png',
                               size_hint=(None, None),
                               size=(1000, 600),
                               pos_hint={'center_x': 0.35, 'top': 1.1})
            root_layout.add_widget(logo_image)

            header_layout = BoxLayout(size_hint=(1, None), height=30)
            for col_name in column_names:
                header_label = Label(text=col_name, size_hint=(None, 1), width=200, color=(0, 0, 0, 1))
                header_layout.add_widget(header_label)

            # Calcula la altura total de las filas
            total_rows = len(resultados)
            row_height = 28  # Ajusta según la altura de cada fila
            total_rows_height = total_rows  * row_height +20

            # Crea el GridLayout con la altura total
            data_layout = GridLayout(cols=len(column_names) + 2, size_hint_y=None, height=total_rows_height)

            for fila in resultados:
                for dato in fila:
                    label = Label(text=str(dato), size_hint_y=None, height=row_height, color=(0, 0, 0, 1))
                    data_layout.add_widget(label)

                image_button1 = ImageButton(source='IGUARDAR.png', size_hint_y=None, height=row_height, width=50)
                image_button2 = ImageButton(source='IMODIFICAR.png', size_hint_y=None, height=row_height, width=50)
                data_layout.add_widget(image_button1)
                data_layout.add_widget(image_button2)

            container_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=data_layout.height + header_layout.height,
                spacing=10,
                padding=(20, 20)
            )

            spacer_widget = Widget(size_hint=(1, None), height=10)

            container_layout.add_widget(header_layout)
            container_layout.add_widget(spacer_widget)
            container_layout.add_widget(data_layout)

            # Ajusta el tamaño del CustomScrollView al tamaño del GridLayout
            scroll_view = CustomScrollView(size_hint=(1, None), do_scroll_x=False, size=(400, total_rows_height),
                                           pos_hint={'center_x': 0.5, 'center_y': 0.38}, scroll_y=0)
            scroll_view.add_widget(container_layout)

            root_layout.add_widget(scroll_view)

            exit_button = Button(text="Salir", size_hint=(None, None), size=(dp(80), dp(30)),
                                 pos_hint={'right': 1, 'bottom': 1})
            exit_button.bind(on_press=self.close_app)
            root_layout.add_widget(exit_button)

        return root_layout

    def close_app(self, instance):
        App.get_running_app().stop()

if __name__ == "__main__":
    Musica().run()
