from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock

from tubo import Tubo

class Background(Widget):
    nube_textura = ObjectProperty(None)
    sopi_textura = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #crear texturas
        self.nube_textura = Image(source="nube.png").texture
        self.nube_textura.wrap = 'repeat'
        self.nube_textura.uvsize = (Window.width / 250, -1)

        self.sopi_textura = Image(source="sopi.png").texture
        self.sopi_textura.wrap = 'repeat'
        self.sopi_textura.uvsize = (Window.width / self.sopi_textura.width, -1)

    def scroll_textures(self, time_passed):
        #actualizar uvpos
        self.nube_textura.uvpos = ((self.nube_textura.uvpos[0] + time_passed/3.0)%Window.width, self.nube_textura.uvpos[1])
        self.sopi_textura.uvpos = ((self.sopi_textura.uvpos[0] + time_passed/2.0)%Window.width, self.sopi_textura.uvpos[1])
        #redibujar textura
        texture = self.property("nube_textura")
        texture.dispatch(self)


        texture = self.property("sopi_textura")
        texture.dispatch(self)

    pass



class MainApp(App):
    def on_start(self):
        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60)

    pass

if __name__ == "__main__":
    MainApp().run()
