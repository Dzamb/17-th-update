
import arcade
import os
import time
import math
from variables import *
from player import PlayerCharacter
from enemies import Goblin
import math


class MyGame(arcade.Window):

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        #* отслеживаем текущее состояние нажатой клавиши
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.cast_pressed = False
        self.sword_attack_pressed = False

        #* Это списки которые отслеживают наши спрайты. Каждый спрайт должен войти в список.
        self.coin_list = None
        self.wall_list = None
        self.background_list = None
        self.player_list = None
        self.vilage_list = None
        self.dont_touch_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.enemy_list = None
        self.goblin_sprite = None
        self.fireball_list = None

        #* Используем для отслеживания нашего скролинга
        self.view_bottom = 0
        self.view_left = 0
        #TODO: self.view_right = 0
        #TODO: self.view_top = 0

        #* Настраиваем конец карты
        self.end_of_map = 0

        #* Отслеживание очков
        self.score = 0

        #* Ещё несколько параметров для реализации
        self.game_over = False
        #TODO: self.last_time = None
        #TODO: self.frame_count = 0
        #TODO: self.fps_message = None

        #* Загрузка свуковых эффектов
        self.collect_coin_sound = arcade.load_sound("resources/SFX/coins.wav")
        self.jump_sound = arcade.load_sound("resources/SFX/jumping.wav")
        self.game_over = arcade.load_sound("resources/SFX/game-over.wav")
        self.cast_sound = arcade.load_sound("resources/SFX/fireball.wav")
        self.enemy_damage_sound = arcade.load_sound("resources/SFX/monster-damage.wav")


    def setup(self):

        self.view_bottom = 0
        self.view_left = 0
        #TODO: self. view_score = 0

        #* Создаём спрайт листы
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.goblin_sprite = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()

        #* Ссылаемся что список игрока равен классу что мы уже описали
        self.player_sprite = PlayerCharacter()
        # self.goblin_sprite = Goblin()

        #* Задаём начальные координаты старта персонажа, его размеры.
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite.scale = PLAYER_SCALING
        self.player_list.append(self.player_sprite)

        #* Задаём какую карту загружать и где она расположена
        map_name = "test4.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)

        #* Вычисляем правый конец карты в пикселях
        # self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        #* --- Слой земли и декораций---
        self.background_list = arcade.process_layer(my_map, "background", TILE_SCALING)
        self.vilage_list = arcade.process_layer(my_map, "vilage", TILE_SCALING)
        self.wall_list = arcade.process_layer(my_map, "platforms", TILE_SCALING)

        #* --- Слой монеток ---
        coin_layer_name = "coins"
        self.coin_list = arcade.process_layer(my_map, coin_layer_name, COIN_SCALE)

        #* --- Слой врагов ---
        enemy_layer_name = "enemies"
        e_list = arcade.process_layer(my_map, enemy_layer_name, TILE_SCALING)
        for e in e_list:
            enemy = Goblin()
            enemy.center_x = e.center_x
            enemy.center_y = e.center_y + 64
            enemy.scale = 1
            enemy.change_x = -ENEMY_SPEED
            self.enemy_list.append(enemy)
        self.goblin_physics_engine = arcade.PhysicsEnginePlatformer(self.goblin_sprite, self.wall_list, gravity_constant=GRAVITY)

        #* --- Лестницы ---
        #TODO: self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders", TILE_SCALING)

        #* Создаём физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)   #TODO: ещё нужно будет добавить ladder=self.ladder_list


    def on_draw(self):

        arcade.start_render()

        #* Рисуем наши спрайты.
        self.background_list.draw()
        self.vilage_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.goblin_sprite.draw()
        self.fireball_list.draw()

        #TODO: self.ladder_list.draw()
        #TODO: self.coin_list.draw()

        #* Отрисовка очков на экране, прокрутка по области просмотра
        # score_text = f"Score: {self.score}"
        # arcade.draw_text(score_text, 10 + self.view_left, 10 + view_bottom, arcade.scccolor.BLACK, 18)

    def on_mouse_press(self, x, y, button, modifiers):
        arcade.play_sound(self.cast_sound)
        fireball = arcade.Sprite("resources/effects/FireBall_64x64.gif", FIREBALL_SCALE)
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        fireball.center_x = start_x
        fireball.center_y = start_y
        dest_x = x
        dest_y = y
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
        fireball.angle = math.degrees(angle)
        fireball.change_x = math.cos(angle) * FIREBALL_SPEED
        fireball.change_y = math.sin(angle) * FIREBALL_SPEED
        self.fireball_list.append(fireball)


        # arcade.play_sound(self.cast_sound)
        # fireball = arcade.Sprite("resources/effects/FireBall_64x64.gif", FIREBALL_SCALE)
        # if self.player_sprite.character_face_direction == FACE_LEFT:
        #     fireball.angle = 90
        #     fireball.change_x = -FIREBALL_SPEED
        #     fireball.center_x = self.center_x
        #     fireball.center_y = self.center_y
        #     fireball.right = self.left
        # elif self.player_sprite.character_face_direction == FACE_RIGHT:
        #     fireball.angle = -90
        #     fireball.change_x = FIREBALL_SPEED
        #     fireball.center_x = self.center_x
        #     fireball.center_y = self.center_y
        #     fireball.left = self.right

        # self.fireball_list.append(fireball)








    def process_keychange(self):
        #* Вызывается когда мы надимаем клавиши вверх/вниз или когда мы включаем/ выключаем лестницы

        #* Процесс движения вверх/вниз
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump() and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True

        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        #* Процесс движения вверх/вниз когда мы на лестнице и не двигаемся
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0
        
        #* Процесс движения влево/вправо
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0
        


    def on_key_press(self, key, modifiers):
        #* Вызывается когда мы клавиша нажата.
        if key ==arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.C:
            self.cast_pressed = True

        self.process_keychange()


    def on_key_release(self, key, modifiers):
        #* Вызывается когда пользователь отпускает клавишу.

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.C:
            self.cast_pressed = False
        
        self.process_keychange()


    def on_update(self, delta_time):
        self.player_list.update_animation()
        self.wall_list.update()

        #* Движение игрока с физическим движком
        self.physics_engine.update()
        self.coin_list.update_animation()
        self.enemy_list.update_animation()
        self.fireball_list.update()
        for fireball in self.fireball_list:
            enemy_fireball_hitlist = arcade.check_for_collision_with_list(fireball, self.enemy_list)
            if len(enemy_fireball_hitlist) > 0:
                fireball.kill()
            
            for enemy in enemy_fireball_hitlist:
                enemy.kill()
                arcade.play_sound(self.enemy_damage_sound)


        #* Обновление анимации
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True
        
        #? Дальше мне немного не понятен процесс того что я описываю
        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)
        for coin in coin_hit_list:

            # Figure out how many points this coin is worth
            if 'Points' not in coin.properties:
                print("Warning, collected a coin without a Points property.")
            else:
                points = int(coin.properties['Points'])
                self.score += points

            # Remove the coin
            coin.remove_from_sprite_lists()

        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        for enemy in enemy_hit_list:
            if "points" not in enemy.properties:
                print("Warning, collected a coin without a Points property.")
            else:
                points = int(enemy.properties['Points'])
                self.score += points
            enemy.remove_from_sprite_lists()

        #* Логика отображающая не наткнулась ли движущаяся платформа
        #* на преграду и не надо ли повернуть движение.
        for wall in self.wall_list:

            if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
                wall.change_x *= -1
            if wall.boundary_left and wall.left < wall.boundary_left and wall.change_y < 0:
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
                wall.change_y *= -1


        #* Отслеживание нужно ли нам поменять обзор(viewport)
        changed_viewport = False

            #* ===Скролинг===

            #* Скролинг влево
        left_boundary = self.view_left + VIEWPORT_LEFT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        #* Скролинг вправо
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        #* Скролинг вверх
        top_boundary = self.view_bottom + SCREEN_WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - right_boundary
            changed_viewport = True

        #* Скролинг вниз
        bottom_boundary = self.view_bottom + VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            #* Прокрутка только до целых чисел. Иначе мы получим пиксели 
            #* которые не выстраиваются в линию на экране.
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            #* Скролинг
            arcade.set_viewport(self.view_left, 
                                SCREEN_WIDTH + self.view_left, 
                                self.view_bottom, 
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()