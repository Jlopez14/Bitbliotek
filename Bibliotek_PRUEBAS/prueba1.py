import tkinter as tk

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Mi Colección Personal")

        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.master.winfo_screenwidth()
        alto_pantalla = self.master.winfo_screenheight()

        # Definir tamaño de la ventana como cinco sextos de la pantalla
        ancho_ventana = (ancho_pantalla * 5) // 6
        alto_ventana = (alto_pantalla * 5) // 6

        # Calcular posición para centrar la ventana
        x_pos = (ancho_pantalla - ancho_ventana) // 2
        y_pos = (alto_pantalla - alto_ventana) // 2

        # Configurar tamaño y posición
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

        # Colores negro grisáceo y verde oscuro
        color_fondo = "#1C1C1C"  # Negro grisáceo
        color_secundario2 = "#2E7D32"  # Verde oscuro
        color_letra = "black"

        # Configurar estilo para botones
        estilo = {"font": ("Arial", 14), "bg": color_secundario2, "fg": color_letra, "width": 30, "height":  30}
        estilo2 = {"font": ("Arial", 14), "bg": color_secundario2, "fg": color_letra, "width":  3, "height":  1}

        # Configurar fondo de la ventana
        self.master.configure(bg=color_fondo)

        # Contenedor para los botones principales
        contenedor_botones = tk.Frame(master, bg=color_fondo)
        contenedor_botones.pack(side=tk.TOP, pady=alto_ventana // 20)

        # Botones de categorías sin imágenes, centrados en el medio
        tk.Button(contenedor_botones, text="Libros", command=self.mostrar_libros, **estilo).pack(side=tk.LEFT, padx=10)
        tk.Button(contenedor_botones, text="Música", command=self.mostrar_musica, **estilo).pack(side=tk.LEFT, padx=10)
        tk.Button(contenedor_botones, text="Películas", command=self.mostrar_peliculas, **estilo).pack(side=tk.LEFT, padx=10)

        # Botón de salir en la esquina superior derecha
        tk.Button(master, text="Salir", command=master.quit, **estilo2).pack(side=tk.TOP, anchor="ne", pady=10, padx=10)

    def mostrar_libros(self):
        # Lógica para mostrar la ventana de libros
        pass

    def mostrar_musica(self):
        # Lógica para mostrar la ventana de música
        pass

    def mostrar_peliculas(self):
        # Lógica para mostrar la ventana de películas
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()