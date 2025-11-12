from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image

class Tubo(Widget):
    #atributos numericos
    GAP_SIZE = NumericProperty(60)
    CAP_SIZE = NumericProperty(20)
    tubo_center = NumericProperty(0)
    bottom_body_position = NumericProperty(0)
    bottom_cap_position = NumericProperty(0)
    top_body_position = NumericProperty(0)
    top_cap_position = NumericProperty(0)

    # textura
    tubo_body_texture = ObjectProperty(None)
    bottom_tubo_tex_coords = ListProperty((0 ,0, 1, 0, 1, 1, 0, 1))
    top_tubo_tex_coords = ListProperty((0 ,0, 1, 0, 1, 1, 0, 1))

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tubo_body_texture = Image(source = "cuerpo_50x20.png").texture
        self.tubo_body_texture.wrap = 'repeat'

    def on_size(self, *args):
        bottom_body_size = self.bottom_cap_position - self.bottom_body_position

        self.bottom_tubo_tex_coords[5] = bottom_body_size/20.
        self.bottom_tubo_tex_coords[7] = bottom_body_size/20.

        top_body_size = self.top - self.top_body_position

        self.top_tubo_tex_coords[5] = bottom_body_size/20.
        self.top_tubo_tex_coords[7] = bottom_body_size/20.

        