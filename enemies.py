import arcade
import math
from variables import *

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

class Fireball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += 20


class Goblin(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.goblin_face_direction = FACE_RIGHT
        self.scale = GOBLIN_SCALE
        self.cur_texture = 0

        self.texture_change_distance = 20
        self.last_texture_change_center_x = 0
        self.last_texture_change_center_y = 0
        self.health = 100

        self.is_attacking = False
        self.is_dyeing = False
        self.is_takehit = False

#* Указывает путь к спрайтам персонажа и загружаем их в списки
        main_path = "resources/enemies/Goblin/goblin"
        
    #* Для состояния простоя.
        self.stand_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}_idle_{i}.png")
            self.stand_texture_pair.append(texture)

    #* Для состояния бега.
        self.run_texture_pair = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_run_{i}.png")
            self.run_texture_pair.append(texture)

    #* Для состояния атаки.
        self.attack_texture_pair = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_attack_{i}.png")
            self.attack_texture_pair.append(texture)

    #* Для состояния смерти.
        self.die_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}_death_{i}.png")
            self.die_texture_pair.append(texture)

    #* Для состояния получения урона.
        self.takehit_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}_takehit_{i}.png")
            self.takehit_texture_pair.append(texture)

        #* Инициализируем начальную текстуру
        self.texture = self.stand_texture_pair[0][0]

        #? Что такое хит-боксы я пока не разобрался, но вроде нужно
        self.set_hit_box(self.texture.hit_box_points)



    def update_animation(self, deltatime=1/60):

        # #* анимация атаки
        # if self.is_attacking:
        #     self.cur_texture += 1
        #     if self.cur_texture > 7 * UPDATES_PER_FRAME:
        #         self.cur_texture = 0
        #     self.texture = self.attack_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.goblin_face_direction]
        #     return


        # #* Указание в какую сторону смотрит персонаж
        # if self.change_x < 0 and self.goblin_face_direction == FACE_RIGHT:
        #     self.goblin_face_direction = FACE_LEFT
        # elif self.change_x > 0 and self.goblin_face_direction == FACE_LEFT:
        #     self.goblin_face_direction = FACE_RIGHT

        # #* анимация простоя
        # if self.change_x == 0 and self.change_y == 0:
        #     self.cur_texture += 1
        #     if self.cur_texture > 3 * UPDATES_PER_FRAME:
        #         self.cur_texture = 0
        #     self.texture = self.stand_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.goblin_face_direction]
        #     return

        #* анимация бега
        self.cur_texture += 1 and self.change_y == 0
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.run_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.goblin_face_direction]
        return

        # #* анимация смерти
        # if self.is_dyeing and self.health <= 0:
        #     self.cur_texture += 1
        #     if self.cur_texture > 3 * UPDATES_PER_FRAME:
        #         self.cur_texture = 0
        #     self.texture = self.die_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.goblin_face_direction]
        #     return

        # #* Анимация  получения урона
        # if self.is_takehit:
        #     self.cur_texture += 1
        #     if self.cur_texture >3 * UPDATES_PER_FRAME:
        #         self.cur_texture = 0
        #     self.texture = self.takehit_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.goblin_face_direction]





        # x1 = self.center_x
        # x2 = self.last_texture_change_center_x
        # y1 = self.center_y
        # y2 = self.last_texture_change_center_y
        # distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # texture_list = []

        # change_direction = False
        # if self.change_x > 0 \
        #         and self.change_y == 0 \
        #         and self.state != FACE_RIGHT \
        #         and self.walk_right_textures \
        #         and len(self.walk_right_textures) > 0:
        #     self.state = FACE_RIGHT
        #     change_direction = True
        # elif self.change_x < 0 and self.change_y == 0 and self.state != FACE_LEFT \
        #         and self.walk_left_textures and len(self.walk_left_textures) > 0:
        #     self.state = FACE_LEFT
        #     change_direction = True


        # if self.change_x == 0 and self.change_y == 0:
        #     if self.state == FACE_LEFT:
        #         self.texture = self.stand_left_textures[0]
        #     elif self.state == FACE_RIGHT:
        #         self.texture = self.stand_right_textures[0]


        # elif change_direction or distance >= self.texture_change_distance:
        #     self.last_texture_change_center_x = self.center_x
        #     self.last_texture_change_center_y = self.center_y

        #     if self.state == FACE_LEFT:
        #         texture_list = self.walk_left_textures
        #         if texture_list is None or len(texture_list) == 0:
        #             raise RuntimeError("update_animation was called on a sprite that doesn't have a "
        #                                "list of walk left textures.")
        #     elif self.state == FACE_RIGHT:
        #         texture_list = self.walk_right_textures
        #         if texture_list is None or len(texture_list) == 0:
        #             raise RuntimeError("update_animation was called on a sprite that doesn't have a list of "
        #                                "walk right textures.")

        #     self.cur_texture_index += 1
        #     if self.cur_texture_index >= len(texture_list):
        #         self.cur_texture_index = 0

        #     self.texture = texture_list[self.cur_texture_index]

        # if self._texture is None:
        #     print("Error, no texture set")
        # else:
        #     self.width = self._texture.width * self.scale
        #     self.height = self._texture.height * self.scale
