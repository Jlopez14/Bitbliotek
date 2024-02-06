import mysql.connector
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        # Conexión a la base de datos MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='pablo2',
            database='bitbliotek'
        )
        cursor = conn.cursor()

        # Ejemplo de consulta SQL
        cursor.execute('SELECT Titulo, Genero, Artista, Album, Rating FROM musica')
        data = cursor.fetchall()

        # Crear la interfaz gráfica con GridLayout
        layout = GridLayout(cols=5, spacing=1)

        # Encabezados de la tabla
        headers = ['Título', 'Género', 'Artista', 'Álbum', 'Rating']
        for header in headers:
            header_label = Label(text=header, bold=True, size_hint_y=None, height=40, halign='center', valign='middle', canvas_before=header_label.canvas.before, canvas_after=header_label.canvas.after)
            header_label.canvas.before.add(Color(1, 1, 1, 1))  # Color blanco
            header_label.canvas.before.add(Rectangle(pos=header_label.pos, size=header_label.size))
            layout.add_widget(header_label)

        # Datos de la tabla
        for item in data:
            for value in item:
                cell_label = Label(text=str(value), size_hint_y=None, height=30, halign='center', valign='middle', canvas_before=cell_label.canvas.before, canvas_after=cell_label.canvas.after)
                cell_label.canvas.before.add(Color(1, 1, 1, 1))  # Color blanco
                cell_label.canvas.before.add(Rectangle(pos=cell_label.pos, size=cell_label.size))
                layout.add_widget(cell_label)

        return layout

    def on_start(self):
        # Método llamado después de que la aplicación ha sido iniciada
        # Establecer el fondo verde
        with self.root.canvas.before:
            Color(0, 1, 0, 1)  # Color verde
            self.rect = Rectangle(size=(self.root.width, self.root.height), pos=self.root.pos)

if __name__ == '__main__':
    MyApp().run()
