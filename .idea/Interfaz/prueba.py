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
from kivy.graphics import Color, Rectangle

class ImageButton(ButtonBehavior, Image):
    pass

class CustomScrollView(ScrollView):
    def on_scroll_wheel(self, instance, value):
        super().on_scroll_wheel(instance, value)

class EditPopup(Popup):
    def __init__(self, data, connection, cursor, refresh_callback, **kwargs):
        super(EditPopup, self).__init__(**kwargs)
        self.title = "Editar Canción"
        self.size_hint=(None, None)
        self.size=(dp(500), dp(500))
        self.data = data
        self.connection = connection
        self.cursor = cursor
        self.refresh_callback = refresh_callback

        # Ajustar el estilo del popup
        self.background_color = [0.49411764705882355, 0.8509803921568627, 0.3411764705882353, 1]  # Fondo verde
        self.title_color = [1, 1, 1, 1]  # Color del texto del título (blanco)
        self.separator_color = [1, 1, 1, 1]  # Color del separador (blanco)


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
                    pos_hint={'right': 0.55},
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

class RegistroPopup(Popup):
    def __init__(self, connection, cursor, refresh_callback, **kwargs):
        super(RegistroPopup, self).__init__(**kwargs)
        self.title = "Registrar Nueva Canción"
        self.size_hint = (None, None)
        self.size = (dp(500), dp(500))
        self.connection = connection
        self.cursor = cursor
        self.refresh_callback = refresh_callback

        # Ajustar el estilo del popup
        self.background_color = [0.49411764705882355, 0.8509803921568627, 0.3411764705882353, 1]  # Fondo verde
        self.title_color = [1, 1, 1, 1]  # Color del texto del título (blanco)
        self.separator_color = [1, 1, 1, 1]  # Color del separador (blanco)

        layout = BoxLayout(orientation='vertical')

        # Crea los widgets de formulario
        self.input_widgets = []
        for idx, col_name in enumerate(column_names[1:]):
            label = Label(text=col_name)
            if col_name.lower() == 'rating':
                spinner = Spinner(
                    text='0',
                    values=[str(i) for i in range(6)],
                    size_hint=(None, 1),
                    pos_hint={'right': 0.55},
                    width=50
                )
                layout.add_widget(label)
                layout.add_widget(spinner)
                self.input_widgets.append(spinner)
            else:
                input_text = TextInput(multiline=False)
                layout.add_widget(label)
                layout.add_widget(input_text)
                self.input_widgets.append(input_text)

        save_button = Button(text="Guardar Canción", on_press=self.save_song)
        layout.add_widget(save_button)

        self.content = layout

    def save_song(self, instance):
        # Obtener los valores ingresados por el usuario
        values = [input_widget.text if isinstance(input_widget, TextInput) else input_widget.text for input_widget in self.input_widgets]

        # Insertar la nueva canción en la base de datos
        insert_query = f"INSERT INTO musica ({', '.join(column_names[1:])}) VALUES ({', '.join(['%s' for _ in range(len(column_names)-1)])})"
        try:
            self.cursor.execute(insert_query, values)
            self.connection.commit()
            print("Canción registrada exitosamente.")
        except Exception as e:
            print(f"Error al registrar la canción: {e}")

        self.dismiss()
        self.refresh_callback()  # Actualizar la interfaz

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
            password="lopez",
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


        # Agrega una imagen encima del recuadro de búsqueda
        search_image = Image(source='musicasinfondo.png', size_hint=(None, None), size=(300, 300),
                             pos_hint={'right': 0.77, 'top': 0.98})  # Ajusta la posición según tu preferencia
        root_layout.add_widget(search_image)

        # Agrega una barra de búsqueda
        search_input = TextInput(
            hint_text='Buscar...',
            multiline=False,
            size_hint=(None, None),
            size=(210, 38),
            pos_hint={'right': 0.90, 'top': 0.75}  # Ajusta los valores según tu preferencia
        )
        search_input.bind(text=self.filter_results)
        root_layout.add_widget(search_input)

        # Agregar el Spinner y los botones
        spinner_layout = BoxLayout(size_hint=(None, None), size=(200, 50), pos_hint={'right': 0.96, 'top': 0.815})
        self.spinner = Spinner(text='Filtro', values=('Ascendente', 'Descendente', 'Peor valoradas', 'Mejor valoradas'), size_hint=(None, None), size=(200, 50))
        self.spinner.background_color = (0, 0, 0, 1)  # Negro (RGBA)
        self.spinner.color = (0.494, 0.851, 0.341, 1)  # Verde (RGBA)
        self.spinner.bind(text=self.refresh_ui)  # Actualizar la interfaz cuando se cambie el valor del Spinner
        spinner_layout.add_widget(self.spinner)
        root_layout.add_widget(spinner_layout)

        # Botón de Registrar
        btn_register = Button(text='Añadir',
                              on_press=self.anadir_press,
                              size_hint=(None, None),
                              height=dp(39),
                              pos_hint={'right': 0.96, 'top': 0.75})
        # Establecer el color de fondo a negro
        btn_register.background_color = (0, 0, 0, 1)  # Negro (RGBA)
        # Establecer el color del texto a verde
        btn_register.color = (0.494, 0.851, 0.341, 1)  # Verde (RGBA)
        root_layout.add_widget(btn_register)

        header_scroll_view = CustomScrollView(size_hint=(1, None), do_scroll_x=False, size=(400, 60),
                                              pos_hint={'center_x': 0.52, 'top': 0.72}, scroll_y=0)

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
                                      pos_hint={'top': 0.56})

        # Guarda una copia sin filtrar de los resultados para poder aplicar el filtro más adelante
        self.filtered_resultados = self.resultados.copy()

        for idx, fila in enumerate(self.resultados):
            for col_idx, dato in enumerate(fila):
                if col_idx == 0:
                    continue

                label = Label(text=str(dato), size_hint_y=None, height=row_height, color=(0, 0, 0, 1))
                self.data_layout.add_widget(label)

            image_button1 = ImageButton(source='pabloreal.png', size_hint_y=None, height=row_height, width=50, size=(23,23))
            image_button2 = ImageButton(source='IMODIFICAR.png', size_hint_y=None, height=row_height, width=50)
            image_button2.bind(on_release=lambda btn, row_id=idx: self.edit_row(row_id))

            image_button1.bind(on_release=lambda btn, row_id=idx: self.delete_row(row_id))  # Asociar la función de eliminación al botón

            self.data_layout.add_widget(image_button1)
            self.data_layout.add_widget(image_button2)

        container_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=self.data_layout.height + header_layout.height,
            spacing=0,
            padding=(20, 20)
        )

        spacer_widget = Widget(size_hint=(1, None), height=10)

        container_layout.add_widget(spacer_widget)
        container_layout.add_widget(self.data_layout)

        scroll_view = CustomScrollView(size_hint=(1, None), do_scroll_x=False, size=(350, 500),
                                       pos_hint={'center_x': 0.5, 'center_y': 0.45}, scroll_y=1)
        scroll_view.add_widget(container_layout)

        root_layout.add_widget(scroll_view)

        exit_button = Button(text="Salir", size_hint=(None, None), size=(dp(80), dp(30)),
                             pos_hint={'right': 1, 'bottom': 1})
        exit_button.bind(on_press=self.close_app)
        root_layout.add_widget(exit_button)

        # Implementación del código proporcionado
        label_layout = RelativeLayout(size_hint=(None, None), size=(dp(180), dp(36)), pos_hint={'top': 0.96, 'right': 0.96})

        label = Label(text="Portugordo", size_hint=(None, None), size=(dp(144), dp(36)),
                      pos_hint={'top': 1, 'right': 0.5}, color=(0, 1, 0, 1), font_size='18sp',
                      halign='right', valign='middle', text_size=(dp(144), None))

        with label_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=label.pos, size=label.size)

        label_layout.add_widget(label)

        button = Button(size_hint=(None, None), size=(dp(40), dp(40)), pos_hint={'right': 1, 'top': 1},
                        background_normal='cerral.png')
        button.bind(on_press=self.on_close_press)
        label_layout.add_widget(button)

        root_layout.add_widget(label_layout)

        return root_layout

    def on_close_press(self, instance):
        pass

    def close_app(self, instance):
        App.get_running_app().stop()

    def edit_row(self, row_id):
        data = self.filtered_resultados[row_id]
        original_row_index = self.resultados.index(data)
        edit_popup = EditPopup(data, self.conexion, self.cursor, self.refresh_data)
        edit_popup.open()

    # Dentro del método delete_row de la clase Musica

    def delete_row(self, row_id):
        data = self.filtered_resultados[row_id]
        original_row_index = self.resultados.index(data)

        # Popup de confirmación de eliminación
        confirmation_popup = Popup(title='Confirmar Eliminación',
                                   size_hint=(None, None), size=(400, 112))
        # Ajustar el estilo del popup
        confirmation_popup.background_color = [0.49411764705882355, 0.8509803921568627, 0.3411764705882353, 1]  # Fondo verde
        confirmation_popup.title_color = [1, 1, 1, 1]  # Color del texto del título (blanco)
        confirmation_popup.separator_color = [1, 1, 1, 1]  # Color del separador (blanco)

        # Contenedor para los botones
        button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 50), spacing=177)

        # Botón para confirmar la eliminación
        btn_confirm_delete = Button(text='Sí', size_hint=(None, None), size=(100, 50))
        btn_confirm_delete.bind(on_press=lambda btn: self.confirm_delete(row_id, confirmation_popup))

        # Botón para cancelar la eliminación
        btn_cancel_delete = Button(text='No', size_hint=(None, None), size=(100, 50))
        btn_cancel_delete.bind(on_press=confirmation_popup.dismiss)

        # Agregar los botones al layout
        button_layout.add_widget(btn_confirm_delete)
        button_layout.add_widget(btn_cancel_delete)

        # Agregar el layout de botones al contenido del popup de confirmación
        confirmation_popup.content = button_layout

        # Mostrar el popup de confirmación
        confirmation_popup.open()



    def confirm_delete(self, row_id, confirmation_popup):
        data = self.filtered_resultados[row_id]
        print("Data:", data)  # Agregar este mensaje para verificar los datos
        original_row_index = self.resultados.index(data)
        print("Original row index:", original_row_index)  # Agregar este mensaje para verificar el índice del registro

        # Eliminar el registro de la base de datos
        delete_query = "DELETE FROM musica WHERE idCancion = %s"
        try:
            self.cursor.execute(delete_query, (data[0],))  # data[0] es el id del registro
            self.conexion.commit()  # Confirmar la eliminación
            print("Registro eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar el registro: {e}")

        # Cerrar el popup de confirmación
        confirmation_popup.dismiss()

        # Actualizar la interfaz
        self.refresh_data()


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

    def refresh_ui(self, *args):
        self.data_layout.clear_widgets()

        # Obtener el valor actual seleccionado en el Spinner
        spinner_value = self.spinner.text

        # Ordenar los resultados filtrados según el valor del Spinner
        if spinner_value == 'Ascendente':
            self.filtered_resultados.sort(key=lambda x: x[1])
        elif spinner_value == 'Descendente':
            self.filtered_resultados.sort(key=lambda x: x[1], reverse=True)
        elif spinner_value == 'Peor valoradas':
            self.filtered_resultados.sort(key=lambda x: x[4])
        elif spinner_value == 'Mejor valoradas':
            self.filtered_resultados.sort(key=lambda x: x[4], reverse=True)

        # Código para mostrar los resultados en la interfaz
        for idx, fila in enumerate(self.filtered_resultados):
            for col_idx, dato in enumerate(fila):
                if col_idx == 0:
                    continue

                label = Label(text=str(dato), size_hint_y=None, height=26, color=(0, 0, 0, 1))
                self.data_layout.add_widget(label)

            image_button1 = ImageButton(source='pabloreal.png', size_hint_y=None, width=50, size=(23,23))
            image_button2 = ImageButton(source='IMODIFICAR.png', size_hint_y=None, height=26, width=50)
            image_button2.bind(on_release=lambda btn, row_id=idx: self.edit_row(row_id))

            self.data_layout.add_widget(image_button1)
            self.data_layout.add_widget(image_button2)

        self.data_layout.height = len(self.filtered_resultados) * 26 + 10


    def anadir_press(self, instance):
        registro_popup = RegistroPopup(self.conexion, self.cursor, self.refresh_data)
        registro_popup.open()

if __name__ == "__main__":
    Musica().run()
