import arcade
import os
from variables import *

class GoldCoin(arcade.Sprite):
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.cur_texture = 0
        self.scale = COIN_SCALING

        main_path = "resources/treasures/coin"

        self.coin_animation_texture = []
        for i in range(5):
            texture = arcade.load_texture(f"{main_path}_{i}.png")
            self.coin_animation_texture.append(texture)

        # self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time=1 /60):
        
        if self.change_x == 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture > 4 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.coin_animation_texture[self.cur_texture // UPDATES_PER_FRAME]
            return