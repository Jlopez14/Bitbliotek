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
from conexion import obtenerNombre
from datetime import date

class ImageButton(ButtonBehavior, Image):
    pass

class CustomScrollView(ScrollView):
    def on_scroll_wheel(self, instance, value):
        super().on_scroll_wheel(instance, value)

class EditPopup(Popup):
    def __init__(self, data, connection, cursor, refresh_callback, column_names, **kwargs):
        super(EditPopup, self).__init__(**kwargs)
        self.title = "Editar Canción"
        self.size_hint = (None, None)
        self.size = (dp(700), dp(700))
        self.data = data
        self.connection = connection
        self.cursor = cursor
        self.refresh_callback = refresh_callback
        self.column_names = column_names

        # Ajustar el estilo del popup
        self.background_color = [0.49411764705882355, 0.8509803921568627, 0.3411764705882353, 1]  # Fondo verde
        self.title_color = [1, 1, 1, 1]  # Color del texto del título (blanco)
        self.separator_color = [1, 1, 1, 1]  # Color del separador (blanco)

        layout = BoxLayout(orientation='vertical')

        # Crea los widgets de formulario y asigna los valores de la fila seleccionada
        self.input_widgets = []

        for col_name, col_value in zip(self.column_names[1:], self.data[1:]):
            label = Label(text=col_name)
            if col_name.lower() == 'rating':
                spinner = Spinner(
                    text=str(col_value),
                    values=[str(i) for i in range(1, 6)],
                    size_hint=(None, 1),
                    pos_hint={'right': 0.55},
                    width=50
                )
                layout.add_widget(label)
                layout.add_widget(spinner)
                self.input_widgets.append(spinner)

            elif col_name.lower() == 'fechavisualizacion':
                date_input_with_dash = TextInput(multiline=False, readonly=False, text=str(col_value))
                layout.add_widget(label)
                layout.add_widget(date_input_with_dash)
                self.input_widgets.append(date_input_with_dash)

            elif col_name.lower() == 'idusuario':
                input_text = TextInput(text=str(col_value), multiline=False, readonly=True)
                layout.add_widget(label)
                layout.add_widget(input_text)
                self.input_widgets.append(input_text)
            else:
                input_text = TextInput(text=str(col_value), multiline=False)
                layout.add_widget(label)
                layout.add_widget(input_text)
                self.input_widgets.append(input_text)

        save_button = Button(text="Guardar Cambios", on_press=self.save_changes)
        layout.add_widget(save_button)

        self.content = layout

    def save_changes(self, instance):
        updated_values = []

        for input_widget, col_name in zip(self.input_widgets, self.column_names[1:]):
            if col_name.lower() == 'rating':
                try:
                    updated_values.append(int(input_widget.text))
                except ValueError:
                    print(f"Error: El valor '{input_widget.text}' no es un número entero válido.")
                    updated_values.append(None)  # Otra opción es manejar este caso de manera específica para tu aplicación
            elif col_name.lower() == 'fechalectura':
                # Verificar si hay guiones en la fecha
                if '-' in input_widget.text:
                    # Si hay guiones, quitarlos antes de agregar al resultado
                    updated_values.append(input_widget.text.replace("-", ""))
                else:
                    updated_values.append(input_widget.text)
            else:
                updated_values.append(input_widget.text)

        # Crear una cadena con los nombres de las columnas y sus valores para la actualización
        update_query = f"UPDATE cine SET {', '.join([f'{col_name} = %s' for col_name in self.column_names[1:]])} WHERE idPelicula = %s AND idusuario = %s"


        try:
            # Utilizar la función execute con la tupla de valores actualizados
            self.cursor.execute(update_query, tuple(updated_values + [self.data[0], self.data[6]]))

            self.connection.commit()
            print("Fila actualizada exitosamente.")
        except Exception as e:
            print(f"Error al actualizar la fila: {e}")

        self.dismiss()
        self.refresh_callback()  # Llama al callback para actualizar los datos y la interfaz





class RegistroPopup(Popup):
    def __init__(self, connection, cursor, refresh_callback, id_usuario, column_names, **kwargs):
        super(RegistroPopup, self).__init__(**kwargs)
        self.title = "Registrar Nueva Pelicula"
        self.size_hint = (None, None)
        self.size = (dp(700), dp(700))
        self.connection = connection
        self.cursor = cursor
        self.id_usuario = id_usuario
        self.refresh_callback = refresh_callback
        self.column_names = column_names

        # Ajustar el estilo del popup
        self.background_color = [0.49411764705882355, 0.8509803921568627, 0.3411764705882353, 1]  # Fondo verde
        self.title_color = [1, 1, 1, 1]  # Color del texto del título (blanco)
        self.separator_color = [1, 1, 1, 1]  # Color del separador (blanco)

        layout = BoxLayout(orientation='vertical')

        # Crea los widgets de formulario
        self.input_widgets = []
        for idx, col_name in enumerate(self.column_names[1:]):
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

            elif col_name.lower() == 'idusuario':
                input_text = TextInput(text=str(self.id_usuario), multiline=False, readonly=True)
                layout.add_widget(label)
                layout.add_widget(input_text)
                self.input_widgets.append(input_text)

            elif col_name.lower() == 'fechavisualizacion':
                date_input_with_dash = TextInput(multiline=False, readonly=False, text=self.get_current_date_with_dash())
                layout.add_widget(label)
                layout.add_widget(date_input_with_dash)
                self.input_widgets.append(date_input_with_dash)

            else:
                input_text = TextInput(multiline=False)
                layout.add_widget(label)
                layout.add_widget(input_text)
                self.input_widgets.append(input_text)

        save_button = Button(text="Guardar Pelicula", on_press=self.save_song)
        layout.add_widget(save_button)

        self.content = layout


    def get_current_date_with_dash(self):
        return str(date.today())

    def save_song(self, instance):
        # Obtén el valor de la fecha con guiones (date_input_with_dash)
        date_with_dash = self.input_widgets[-1].text

        # Procesa la fecha para quitar los guiones antes de enviarla a la base de datos
        date_without_dash = date_with_dash.replace("-", "")
        new_values = [input_widget.text if isinstance(input_widget, TextInput) else input_widget.text for input_widget in self.input_widgets]

        print("Fecha con guiones:", date_with_dash)
        print("Fecha sin guiones (para la base de datos):", date_without_dash)



        insert_query = f"INSERT INTO cine ({', '.join(self.column_names[1:])}) VALUES ({', '.join(['%s'] * (len(self.column_names) - 1))})"

        print(f"Longitud de new_values: {len(new_values)}")
        print(f"Consulta de inserción: {insert_query}")
        print(f"Valores a insertar: {new_values}")

        try:
            self.cursor.execute(insert_query, tuple(new_values))
            self.connection.commit()
            print("Canción registrada exitosamente.")
        except Exception as e:
            print(f"Error al registrar la canción: {e}")

        self.dismiss()
        self.refresh_callback()  # Llama al callback para actualizar los datos y la interfaz


class Libros(App):
    def __init__(self, id_usuario, **kwargs):
        super(Libros, self).__init__(**kwargs)
        self.id_usuario = id_usuario
        self.resultados = None
        self.filtered_resultados = None
        self.root_layout = None
        self.conexion = None
        self.cursor = None
        self.column_names = None

    def build(self):
        Window.fullscreen = 'auto'
        Window.show_cursor = True

        self.conexion = mysql.connector.connect(
            host="79.116.29.226",
            user="remote",
            password="1234",
            database="bitbliotek",
        )
        self.cursor = self.conexion.cursor()
        consulta = f"SELECT * FROM cine WHERE idusuario = {self.id_usuario}"
        self.cursor.execute(consulta)
        self.resultados = self.cursor.fetchall()
        self.column_names = [i[0] for i in self.cursor.description]

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
                              on_press=self.anadir_press,  # Asegúrate de que esta línea esté correctamente escrita
                              size_hint=(None, None),
                              height=dp(39),
                              pos_hint={'right': 0.92, 'top': 0.75})
        # Establecer el color de fondo a negro
        btn_register.background_color = (0, 0, 0, 1)  # Negro (RGBA)
        # Establecer el color del texto a verde
        btn_register.color = (0.494, 0.851, 0.341, 1)  # Verde (RGBA)
        root_layout.add_widget(btn_register)

        header_scroll_view = CustomScrollView(size_hint=(1, None), do_scroll_x=False, size=(400, 60),
                                              pos_hint={'center_x': 0.52, 'top': 0.72}, scroll_y=0)

        header_layout = BoxLayout(size_hint=(1, None), spacing=35, height=60, padding=(0, 10))
        for col_name in self.column_names[1:]:
            header_label = Label(text=col_name, size_hint=(None, 1), width=175, color=(0, 0, 0, 1))
            header_layout.add_widget(header_label)
        header_scroll_view.add_widget(header_layout)
        root_layout.add_widget(header_scroll_view)

        total_rows = len(self.resultados)
        row_height = 26
        total_rows_height = total_rows * row_height + 10

        self.data_layout = GridLayout(cols=len(self.column_names) + 1, size_hint_y=None, height=total_rows_height,
                                      pos_hint={'top': 0.56})

        # Guarda una copia sin filtrar de los resultados para poder aplicar el filtro más adelante
        self.filtered_resultados = self.resultados.copy()

        for idx, fila in enumerate(self.resultados):
            for col_idx, dato in enumerate(fila):
                if col_idx == 0:
                    continue

                label = Label(text=str(dato), size_hint_y=None, height=row_height, color=(0, 0, 0, 1))
                self.data_layout.add_widget(label)

            image_button1 = ImageButton(source='pabloreal.png', size_hint_y=None, height=row_height, width=50, size=(23, 23))
            image_button2 = ImageButton(source='IMODIFICAR.png', size_hint_y=None, height=row_height, width=50)
            image_button2.bind(on_release=lambda btn, row_id=idx: self.edit_row(row_id))

            image_button1.bind(
                on_release=lambda btn, row_id=idx: self.delete_row(row_id))  # Asociar la función de eliminación al botón

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
        label_layout = RelativeLayout(size_hint=(None, None), size=(dp(180), dp(36)),
                                      pos_hint={'top': 0.93, 'right': 0.96})

        nombre_usuario = obtenerNombre(self.id_usuario)

        label = Label(text=nombre_usuario, size_hint=(None, None), size=(dp(144), dp(36)),
                      pos_hint={'top': 1, 'right': 0.5}, color=(0, 1, 0, 1), font_size='18sp',
                      halign='right', valign='middle', text_size=(dp(144), None))

        with label_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=label.pos, size=label.size)

        label_layout.add_widget(label)

        button = Button(size_hint=(None, None), size=(dp(40), dp(36)), pos_hint={'right': 1, 'top': 1},
                        background_normal='cerral.png')
        button.bind(on_press=self.on_close_press)
        label_layout.add_widget(button)

        root_layout.add_widget(label_layout)

        return root_layout

    def on_close_press(self, instance):
        App.get_running_app().stop()  # Cierra la ventana actual

        print(self.id_usuario)
        # Método para cerrar la ventana actual y volver a la ventana de inicio
        from VentanaInicio import Inicio
        Inicio(id=self.id_usuario).run()


    def close_app(self, instance):
        App.get_running_app().stop()

    def anadir_press(self, instance):
        registro_popup = RegistroPopup(self.conexion, self.cursor, self.refresh_data, id_usuario=self.id_usuario, column_names=self.column_names)
        registro_popup.open()

    def edit_row(self, row_id):
        data = self.filtered_resultados[row_id]
        original_row_index = self.resultados.index(data)
        edit_popup = EditPopup(data, self.conexion, self.cursor, self.refresh_data, self.column_names)
        edit_popup.open()

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
        delete_query = "DELETE FROM cine WHERE idPelicula = %s AND idUsuario = %s"
        try:
            self.cursor.execute(delete_query, (data[0], self.id_usuario))  # data[0] es el id del registro
            self.conexion.commit()  # Confirmar la eliminación
            print("Registro eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar el registro: {e}")

        # Cerrar el popup de confirmación
        confirmation_popup.dismiss()

        # Actualizar la interfaz
        self.refresh_data()

    def refresh_data(self):
        consulta = f"SELECT * FROM cine WHERE idusuario = {self.id_usuario}"
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

        for idx, fila in enumerate(self.filtered_resultados):
            for col_idx, dato in enumerate(fila):
                if col_idx == 0:
                    continue

                label = Label(text=str(dato), size_hint_y=None, height=26, color=(0, 0, 0, 1))
                self.data_layout.add_widget(label)

            image_button1 = ImageButton(source='pabloreal.png', size_hint_y=None, height=26, width=50, size=(23, 23))
            image_button2 = ImageButton(source='IMODIFICAR.png', size_hint_y=None, height=26, width=50)
            image_button2.bind(on_release=lambda btn, row_id=idx: self.edit_row(row_id))

            image_button1.bind(
                on_release=lambda btn, row_id=idx: self.delete_row(row_id))  # Asociar la función de eliminación al botón

            self.data_layout.add_widget(image_button1)
            self.data_layout.add_widget(image_button2)

        self.data_layout.height = len(self.filtered_resultados) * 26 + 10

if __name__ == "__main__":
    Peliculas().run()