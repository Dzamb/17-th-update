import arcade
import os
import math
import random
from variables import *
from player import PlayerCharacter
from enemies import Goblin

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.set_file_path()
        self.init_lists_of_interaction_with_player()
        self.init_game_mechanics()
        self.init_sounds()

    def set_file_path(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def init_lists_of_interaction_with_player(self):
        self.player_list = None
        self.player_sprite = None
        self.wall_list = None
        self.enemy_list = None
        self.enemy_sprite = None
        self.background_list = None
        self.vilage_list = None

    def init_game_mechanics(self):
        self.right_pressed = False
        self.left_pressed = False
        self.down_pressed = False
        self.up_pressed = False
        self.jump_need_reset = False
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0

    def init_sounds(self):
        pass

    def setup(self):
        self.setup_game_mechanics()
        my_map = self.read_map()
        self.setup_lists(my_map)
        self.setup_player()
        self.setup_enemies(my_map)


    def setup_game_mechanics(self):
        self.view_bottom = 0
        self.view_left = 0
        self.score = 0



    def setup_lists(self, my_map):
        self.assign_lists()
        self.generate_lists(my_map)

    def assign_lists(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_sprite = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.vilage_list = arcade.SpriteList()
        self.enemy_sprite = Goblin()
        self.player_sprite = PlayerCharacter()

    def setup_player(self):
        self.player_list = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite.scale = PLAYER_SCALING
        self.player_sprite.texture_change_distance = 25
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)
        self.player_sprite.physics_engine = self.physics_engine

    def setup_enemies(self, my_map):
        enemy_sprite = Goblin()
        enemy_layer_name = "enemies"
        e_list = arcade.process_layer(my_map, enemy_layer_name, TILE_SCALING)
        for e in e_list:
            enemy = Goblin()
        enemy.texture_change_distance = 20

        enemy.center_x = e.center_x
        enemy.center_y = e.center_y + 64
        enemy.scale = ENEMY_SCALE
        enemy.change_x = -ENEMY_SPEED

    def generate_lists(self, my_map):
        platform_layer_name = "platforms"
        background_layer_name = "background"
        vilage_layer_name = "vilage"

        self.wall_list = arcade.process_layer(my_map, platform_layer_name, TILE_SCALING)
        self.background_list = arcade.process_layer(my_map, background_layer_name, TILE_SCALING)
        self.vilage_list = arcade.process_layer(my_map, vilage_layer_name, TILE_SCALING)

    def read_map(self):
        platform_layer_name = "platforms"
        map_name = "test4.tmx"
        my_map = arcade.read_tmx(map_name)
        # map_array = my_map.layers_int_data[platform_layer_name]
        # self.end_of_map = (len(map_array[0])-1) * GRID_PIXEL_SIZE
        return my_map


    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        self.player_list.draw()
        self.vilage_list.draw()
        self.enemy_list.draw()
        self.wall_list.draw()

    def process_keychange(self):
        #* Вызывается когда мы надимаем клавиши вверх/вниз или когда мы включаем/ выключаем лестницы

        #* Процесс движения вверх/вниз
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump() and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                # arcade.play_sound(self.jump_sound)
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
            self.player_sprite.is_attacking = True
        
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
            self.player_sprite.is_attacking = False
        
        self.process_keychange()

    def on_update(self, delta_time):
        self.update_player()
        self.update_enemies()
        changed_viewport = self.update_player()
        self.update_viewport(changed_viewport)
        self.physics_engine.update()


    def update_player(self):
        self.player_list.update_animation()
        enemy_player_hitlist = arcade.check_for_collision (self.player_sprite, self.enemy_sprite)
        if enemy_player_hitlist:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            # arcade.play_sound(self.game_over)

        changed_viewport = False

        if self.player_sprite.center_y < 100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_Y = PLAYER_START_Y

            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

    def update_enemies(self):
        self.enemy_list.update_animation()
        for enemy in self.enemy_list:
            enemy.center_x += enemy.change_x
            enemy_flag_hitlist = arcade.check_for_collision_with_list(enemy, self.flag_list)
            if enemy_flag_hitlist:
                enemy.change_x = -enemy.change_x


    def update_viewport(self, changed_viewport):
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



























        self.player_list.update_animation()
        self.enemy_list.update_animation()
        self.wall_list.update()
        self.background_list.update()
        self.vilage_list.update()
        self.physics_engine.update()


        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True
        

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()


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