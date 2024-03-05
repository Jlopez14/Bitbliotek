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
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

class ImageButton(ButtonBehavior, Image):
    pass

class CustomScrollView(ScrollView):
    def on_scroll_wheel(self, instance, value):
        super().on_scroll_wheel(instance, value)

class EditPopup(Popup):
    def __init__(self, data, connection, cursor, refresh_callback, **kwargs):
        super(EditPopup, self).__init__(**kwargs)
        self.title = "Editar Fila"
        self.size_hint = (0.8, 0.8)
        self.data = data
        self.connection = connection
        self.cursor = cursor
        self.refresh_callback = refresh_callback

        layout = BoxLayout(orientation='vertical')

        # Crea los widgets de formulario y asigna los valores de la fila seleccionada
        self.input_widgets = []
        for idx, col_name in enumerate(column_names[1:]):
            label = Label(text=col_name)
            if col_name.lower() == 'rating':
                spinner = Spinner(
                    text=str(data[idx + 1]),
                    values=[str(i) for i in range(1, 6)],
                    size_hint=(None, 1),
                    width=50
                )
                layout.add_widget(label)
                layout.add_widget(spinner)
                self.input_widgets.append(spinner)
            else:
                input_text = TextInput(text=str(data[idx + 1]), multiline=False)
                layout.add_widget(label)
                layout.add_widget(input_text)
                self.input_widgets.append(input_text)

        save_button = Button(text="Guardar Cambios", on_press=self.save_changes)
        layout.add_widget(save_button)

        self.content = layout

    def save_changes(self, instance):
        updated_values = [input_widget.text if isinstance(input_widget, TextInput) else input_widget.text for input_widget in self.input_widgets]

        update_query = f"UPDATE musica SET {', '.join([f'{col_name} = %s' for col_name in column_names[1:]])} WHERE idCancion = %s"

        print(f"Longitud de updated_values: {len(updated_values)}")
        print(f"Consulta de actualización: {update_query}")
        print(f"Valores actualizados: {updated_values}")

        try:
            self.cursor.execute(update_query, tuple(updated_values + [self.data[0]]))
            self.connection.commit()

        except Exception as e:
            print(f"Error al actualizar la fila: {e}")

        self.dismiss()
        self.refresh_callback()  # Llama al callback para actualizar los datos y la interfaz

class Musica(App):
    def __init__(self, **kwargs):
        super(Musica, self).__init__(**kwargs)
        self.resultados = None
        self.filtered_resultados = None
        self.root_layout = None  # Nuevo atributo para mantener la referencia al layout principal
        self.conexion = None  # Añadir atributo de conexión
        self.cursor = None  # Añadir atributo de cursor

    def build(self):
        Window.fullscreen = 'auto'
        Window.show_cursor = True

        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pablo2",
            database="bitbliotek",
        )
        self.cursor = self.conexion.cursor()
        consulta = "SELECT * FROM musica"
        self.cursor.execute(consulta)
        self.resultados = self.cursor.fetchall()
        global column_names
        column_names = [i[0] for i in self.cursor.description]

        root_layout = RelativeLayout()
        self.root_layout = root_layout  # Almacena la referencia al layout principal

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

        # Agrega una barra de búsqueda
        search_input = TextInput(
            hint_text='Buscar...',
            multiline=False,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'right': 0.85, 'top': 0.95}  # Ajusta los valores según tu preferencia
        )
        search_input.bind(text=self.filter_results)
        root_layout.add_widget(search_input)

        header_scroll_view = CustomScrollView(size_hint=(1, None), do_scroll_x=False, size=(400, 60),
                                              pos_hint={'center_x': 0.52, 'top': 0.88}, scroll_y=0)

        header_layout = BoxLayout(size_hint=(1, None), spacing=35, height=60, padding=(0, 10))
        for col_name in column_names[1:]:
            header_label = Label(text=col_name, size_hint=(None, 1), width=200, color=(0, 0, 0, 1))
            header_layout.add_widget(header_label)
        header_scroll_view.add_widget(header_layout)
        root_layout.add_widget(header_scroll_view)

        total_rows = len(self.resultados)
        row_height = 26
        total_rows_height = total_rows * row_height + 10

        self.data_layout = GridLayout(cols=len(column_names) + 1, size_hint_y=None, height=total_rows_height,
                                      pos_hint={'top': 0.54})

        # Guarda una copia sin filtrar de los resultados para poder aplicar el filtro más adelante
        self.filtered_resultados = self.resultados.copy()

        for idx, fila in enumerate(self.resultados):
            for col_idx, dato in enumerate(fila):
                if col_idx == 0:
                    continue

                label = Label(text=str(dato), size_hint_y=None, height=row_height, color=(0, 0, 0, 1))
                self.data_layout.add_widget(label)

            image_button1 = ImageButton(source='IGUARDAR.png', size_hint_y=None, height=row_height, width=50)
            image_button2 = ImageButton(source='IMODIFICAR.png', size_hint_y=None, height=row_height, width=50)
            image_button2.bind(on_release=lambda btn, row_id=idx: self.edit_row(row_id))

            self.data_layout.add_widget(image_button1)
            self.data_layout.add_widget(image_button2)

        container_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=self.data_layout.height + header_layout.height,
            spacing=10,
            padding=(20, 20)
        )

        spacer_widget = Widget(size_hint=(1, None), height=10)

        container_layout.add_widget(spacer_widget)
        container_layout.add_widget(self.data_layout)

        scroll_view = CustomScrollView(size_hint=(1, None), do_scroll_x=False, size=(400, total_rows_height),
                                       pos_hint={'center_x': 0.5, 'center_y': 0.54}, scroll_y=0)
        scroll_view.add_widget(container_layout)

        root_layout.add_widget(scroll_view)

        exit_button = Button(text="Salir", size_hint=(None, None), size=(dp(80), dp(30)),
                             pos_hint={'right': 1, 'bottom': 1})
        exit_button.bind(on_press=self.close_app)
        root_layout.add_widget(exit_button)

        return root_layout

    def close_app(self, instance):
        App.get_running_app().stop()

    def edit_row(self, row_id):
        data = self.filtered_resultados[row_id]
        original_row_index = self.resultados.index(data)  # Obtener el índice en la lista original
        edit_popup = EditPopup(data, self.conexion, self.cursor, self.refresh_data)
        edit_popup.open()

    def refresh_data(self):
        consulta = "SELECT * FROM musica"
        self.cursor.execute(consulta)
        self.resultados = self.cursor.fetchall()
        self.filtered_resultados = self.resultados.copy()
        self.refresh_ui()

    def filter_results(self, instance, value):
        if value:
            self.filtered_resultados = [fila for fila in self.resultados if any(str(value).lower() in str(dato).lower() for dato in fila)]
        else:
            self.filtered_resultados = self.resultados.copy()

        self.refresh_ui()

    def refresh_ui(self):
        self.data_layout.clear_widgets()

        for idx, fila in enumerate(self.filtered_resultados):
            for col_idx, dato in enumerate(fila):
                if col_idx == 0:
                    continue

                label = Label(text=str(dato), size_hint_y=None, height=26, color=(0, 0, 0, 1))
                self.data_layout.add_widget(label)

            image_button1 = ImageButton(source='IGUARDAR.png', size_hint_y=None, height=26, width=50)
            image_button2 = ImageButton(source='IMODIFICAR.png', size_hint_y=None, height=26, width=50)
            image_button2.bind(on_release=lambda btn, row_id=idx: self.edit_row(row_id))

            self.data_layout.add_widget(image_button1)
            self.data_layout.add_widget(image_button2)

        self.data_layout.height = len(self.filtered_resultados) * 26 + 10

if __name__ == "__main__":
    Musica().run()