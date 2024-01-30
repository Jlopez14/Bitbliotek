from kivy.app import App
from ventana1 import Window1

class MainApp(App):
    def build(self):
        return Window1()

if __name__ == '__main__':
    MainApp().run()
