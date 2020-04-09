import arcade
import os
from variables import *

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        #* устанавливаем куда смотрит лицо по-умолчанию
        self.character_face_direction = FACE_RIGHT

        #* Переключение между последовательностями изображений
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        #* Отслеживание наших состояний
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.is_death = False
        self.is_attacking = False
        self.is_casting = False


#*   ===Загрузка текстур===
        #* Указываем папку содержащую все изображения
        main_path = "resources/player/adventurer"

        #* Загрузка текстур стояния для левого и правого состояния
        self.idle_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}-idle-{i}.png")
            self.idle_texture_pair.append(texture)

        #* Загрузка текстур бега для левого и правого состояния
        self.run_texture_pair = []
        for i in range(6):
            texture = load_texture_pair(f"{main_path}-run-{i}.png")
            self.run_texture_pair.append(texture)

        #* Загрузка текстур прыжка для левого и правого состояния
        self.jump_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}-jump-{i}.png")
            self.jump_texture_pair.append(texture)

        #* Загрузка текстур падения для левого и правого состояния
        self.fall_texture_pair = []
        for i in range(2):
            texture = load_texture_pair(f"{main_path}-fall-{i}.png")
            self.fall_texture_pair.append(texture)

        #* Загрузка текстур каста заклинания для левого и правого состояния
        self.cast_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}-cast-{i}.png")
            self.cast_texture_pair.append(texture)

        #* Загрузка текстур атаки мечём для левого и правого состояния
        self.attack_texture_pair = []
        for i in range(5):
            texture = load_texture_pair(f"{main_path}-swordAttack-{i}.png")
            self.attack_texture_pair.append(texture)

        #* Загрузка текстур смерти персонажа для левого и правого состояния
        self.die_texture_pair = []
        for i in range(7):
            texture = load_texture_pair(f"{main_path}-die-{i}.png")
            self.die_texture_pair.append(texture)

        #* Инициализируем начальную текстуру
        self.texture = self.idle_texture_pair[0][0]

        #? Что такое хит-боксы я пока не разобрался, но вроде нужно
        self.set_hit_box(self.texture.hit_box_points)


    def update_animation(self, delta_time=1 /60):

        #* анимация атаки мечём
        if self.is_attacking:
            self.cur_texture += 1
            if self.cur_texture > 4 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.attack_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return

        #* анимация каста заклинания
        if self.is_casting:
            self.cur_texture += 1
            if self.cur_texture > 3 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.cast_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return


        #* Указание в какую сторону смотрит персонаж
        if self.change_x < 0 and self.character_face_direction == FACE_RIGHT:
            self.character_face_direction = FACE_LEFT
        elif self.change_x > 0 and self.character_face_direction == FACE_LEFT:
            self.character_face_direction = FACE_RIGHT

        #* анимация простоя
        if self.change_x == 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture > 3 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.idle_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return

        #* анимация прыжка и падения
        if self.change_y > 0 and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture > 3 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.jump_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.fall_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return

        #* анимация бега
        self.cur_texture += 1 and self.change_y == 0
        if self.cur_texture > 5 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.run_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
        return

        #* анимация смерти
        if self.health <=0:
            self.cur_texture += 1
            if self.cur_texture > 6 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.die_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return
