import arcade
import math
from variables import *

class Fireball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += 20


class Goblin(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.state = FACE_RIGHT
        self.stand_right_textures = None
        self.stand_left_textures = None
        self.run_left_textures = None
        self.run_right_textures = None
        self.attack_right_textures = None
        self.attack_left_textures = None
        self.die_right_textures = None
        self.die_left_textures = None
        self.takehit_right_textures = None
        self.takehit_left_textures = None
        self.cur_texture_index = 0
        self.texture_change_distance = 20
        self.last_texture_change_center_x = 0
        self.last_texture_change_center_y = 0
        self.health = 100

#* Указывает путь к спрайтам персонажа и загружаем их в списки
        main_path = "resources/enemies/Goblin/goblin"
        
    #* Для состояния простоя. Лицо смотрит направо.
        self.stand_right_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}_idle_{i}.png")
            self.stand_right_textures.append(texture)

    #* Для состояния простоя. Лицо смотрит налево.
        self.stand_left_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}_idle_{i}.png", mirrored=True)
            self.stand_left_textures.append(texture)

    #* Для состояния бега. Лицо смотрит направо.
        self.run_right_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_run_{i}.png")
            self.run_right_textures.append(texture)

    #* Для состояния бега. Лицо смотрит налево.
        self.run_left_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_run_{i}.png", mirrored=True)
            self.run_left_textures.append(texture)

    #* Для состояния атаки. Лицо смотрит направо.
        self.attack_right_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_attack_{i}.png")
            self.attack_right_textures.append(texture)

    #* Для состояния атаки. Лицо смотрит налево.
        self.attack_left_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_attack_{i}.png", mirrored=True)
            self.attack_left_textures.append(texture)

    #* Для состояния смерти. Лицо смотрит направо.
        self.die_right_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}_death_{i}.png")
            self.die_right_textures.append(texture)

    #* Для состояния смерти. Лицо смотрит налево.
        self.die_left_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}_death_{i}.png", mirrored=True)
            self.die_left_textures.append(texture)

    #* Для состояния получения урона. Лицо смотрит направо.
        self.takehit_right_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}_takehit_{i}.png")
            self.takehit_right_textures.append(texture)

    #* Для состояния получения урона. Лицо смотрит налево.
        self.takehit_left_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}_takehit_{i}.png", mirrored=True)
            self.takehit_left_textures.append(texture)

        #* Инициализируем начальную текстуру
        self.texture = self.stand_right_textures[0]

        #? Что такое хит-боксы я пока не разобрался, но вроде нужно
        self.set_hit_box(self.texture.hit_box_points)



    def update_animation(self):
        x1 = self.center_x
        x2 = self.last_texture_change_center_x
        y1 = self.center_y
        y2 = self.last_texture_change_center_y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        texture_list = []

        change_direction = False
        if self.change_x > 0 \
                and self.change_y == 0 \
                and self.state != FACE_RIGHT \
                and self.walk_right_textures \
                and len(self.walk_right_textures) > 0:
            self.state = FACE_RIGHT
            change_direction = True
        elif self.change_x < 0 and self.change_y == 0 and self.state != FACE_LEFT \
                and self.walk_left_textures and len(self.walk_left_textures) > 0:
            self.state = FACE_LEFT
            change_direction = True


        if self.change_x == 0 and self.change_y == 0:
            if self.state == FACE_LEFT:
                self.texture = self.stand_left_textures[0]
            elif self.state == FACE_RIGHT:
                self.texture = self.stand_right_textures[0]


        elif change_direction or distance >= self.texture_change_distance:
            self.last_texture_change_center_x = self.center_x
            self.last_texture_change_center_y = self.center_y

            if self.state == FACE_LEFT:
                texture_list = self.walk_left_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a "
                                       "list of walk left textures.")
            elif self.state == FACE_RIGHT:
                texture_list = self.walk_right_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a list of "
                                       "walk right textures.")

            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0

            self.texture = texture_list[self.cur_texture_index]

        if self._texture is None:
            print("Error, no texture set")
        else:
            self.width = self._texture.width * self.scale
            self.height = self._texture.height * self.scale
