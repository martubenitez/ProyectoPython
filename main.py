from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from tubo import Tubo

class Background(Widget):
    textura_nube = ObjectProperty(None)
    textura_sopi = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #crear texturas
        self.textura_nube = Image(source="nube.png").texture
        self.textura_nube.wrap = 'repeat'
        self.textura_nube.uvsize = (Window.width / 250, -1)

        self.textura_sopi = Image(source="sopi.png").texture
        self.textura_sopi.wrap = 'repeat'
        self.textura_sopi.uvsize = (Window.width / self.textura_sopi.width, -1)

    def scroll_textures(self, time_passed):
        #actualizar uvpos
        self.textura_nube.uvpos = ((self.textura_nube.uvpos[0] + time_passed/3.0)%Window.width, self.textura_nube.uvpos[1])
        self.textura_sopi.uvpos = ((self.textura_sopi.uvpos[0] + time_passed/2.0)%Window.width, self.textura_sopi.uvpos[1])
        #redibujar textura
        texture = self.property("textura_nube")
        texture.dispatch(self)


        texture = self.property("textura_sopi")
        texture.dispatch(self)

    pass

from random import randint
from kivy.properties import NumericProperty

class Bird(Image):
    velocidad = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "bird2.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "bird1.png"
        super().on_touch_up(touch)


class MainApp(App):
    tubos = []
    GRAVITY = 300
    was_colliding = False

    # def on_start(self):
    #     Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60)

    def move_bird(self, time_passed):
        bird = self.root.ids.bird
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed
        self.check_collision()

    def check_collision(self):
        bird = self.root.ids.bird
        # Voy por cada tubo y chequear si choca con el pajaro
        is_colliding = False
        for tubo in self.tubos:
            if tubo.collide_widget(bird):
                is_colliding = True
                # Chequeo si el pajaro paso por el medio de los dos tubos
                if bird.y < (tubo.tubo_center - tubo.GAP_SIZE/2.0):
                    self.game_over()
                if bird.top > (tubo.tubo_center + tubo.GAP_SIZE/2.0):
                    self.game_over()
        if bird.y < 100:
            self.game_over()
        if bird.top > Window.height:
            self.game_over()
        
        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text)+1)
        self.was_colliding = is_colliding

    def game_over(self):
        self.root.ids.bird.pos = (20, (self.root.height - 100) / 2.0)
        for tubo in self.tubos:
            self.root.remove_widget(tubo)
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1
        
    def next_frame(self, time_passed):
        self.move_bird(time_passed)
        self.mover_tubos(time_passed)
        self.root.ids.background.scroll_textures(time_passed)

    def start_game(self):
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.tubos = []
        max_diferencia_espacios = 100
        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)
        # Crear tubos
        num_tubos = 5
        distancia_entre_tubos = Window.width / (num_tubos - 1)
        centro_anterior_tubo = randint(100 + 100, self.root.height - 100)
        for i in range(num_tubos):
            tubo = Tubo()
            if centro_anterior_tubo > 199 + max_diferencia_espacios and centro_anterior_tubo < Window.height - (99 + max_diferencia_espacios):
                tubo.tubo_center = randint(centro_anterior_tubo - max_diferencia_espacios, centro_anterior_tubo + max_diferencia_espacios)
            if centro_anterior_tubo < 200 + max_diferencia_espacios:
                tubo.tubo_center = randint(centro_anterior_tubo - (centro_anterior_tubo - 200), centro_anterior_tubo + max_diferencia_espacios)
            if centro_anterior_tubo > Window.height - (100 + max_diferencia_espacios):
                tubo.tubo_center = randint(centro_anterior_tubo - max_diferencia_espacios, centro_anterior_tubo + (Window.height - 100 - centro_anterior_tubo))
            
            tubo.size_hint = (None, None)
            tubo.pos = (Window.width + i*distancia_entre_tubos, 100)
            tubo.size = (70, self.root.height - 100)
            centro_anterior_tubo = tubo.tubo_center

            self.tubos.append(tubo)
            self.root.add_widget(tubo)

    def mover_tubos(self, time_passed):
        for tubo in self.tubos:
            tubo.x -= time_passed * 100

        # Chequeo si tengo que reposicionar el tubo al lado derecho
        num_tubos = 5
        distancia_entre_tubos = Window.width / (num_tubos - 1)
        tubo_xs = list(map(lambda tubo: tubo.x, self.tubos))
        ultimo_tubo_x = max(tubo_xs)
        if ultimo_tubo_x <= Window.width - distancia_entre_tubos:
            primer_tubo = self.tubos[tubo_xs.index(min(tubo_xs))]
            primer_tubo.x = Window.width
        
    pass

if __name__ == "__main__":
    MainApp().run()