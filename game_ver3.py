import arcade
import os
import time


TILE_SCALING = 1
PLAYER_SCALING = 0.5
PLAYER_START_X = 196
PLAYER_START_Y = 200
PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 25

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "17-th Update"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN_TOP = 90
VIEWPORT_MARGIN_BOTTOM = 90
VIEWPORT_RIGHT_MARGIN = 300
VIEWPORT_LEFT_MARGIN = 300

# Physics
MOVEMENT_SPEED = 6
JUMP_SPEED = 6
GRAVITY = 1.1
UPDATES_PER_FRAME = 7
CHARACTER_SCALING = 1
COIN_SCALE = 1

RIGHT_FACING = 0
LEFT_FACING = 1

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
        self.character_face_direction = RIGHT_FACING

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

#!        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

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
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

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
        if self.is_death:
            self.cur_texture += 1
            if self.cur_texture > 6 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.die_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return




class MyGame(arcade.Window):
    """ Main application class. """

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
        #TODO: self.game_over = False
        #TODO: self.last_time = None
        #TODO: self.frame_count = 0
        #TODO: self.fps_message = None

        #* Загрузка свуковых эффектов
        #TODO: self.collect_coin_sound = arcade.load_sound("указываем расположение файла")
        #TODO: self.jump_sound = arcade.load_sound("указываем расположение файла")
        #TODO: self.game_over = arcade.load_sound("указываем расположение файла")


    def setup(self):

        self.view_bottom = 0
        self.view_left = 0
        #TODO: self. view_score = 0

        #* Создаём спрайт листы
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        #* Ссылаемся что список игрока равен классу что мы уже описали
        self.player_sprite = PlayerCharacter()

        #* Задаём начальные координаты старта персонажа, его размеры.
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite.scale = PLAYER_SCALING
        self.player_list.append(self.player_sprite)

        #* Задаём какую карту загружать и где она расположена
        map_name = "test4.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)
        # my_map = arcade.read_tiled_map(map_name)

        #* Вычисляем правый конец карты в пикселях
        # self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        #* --- Слой земли ---
        self.background_list = arcade.process_layer(my_map, "background", TILE_SCALING)
        self.vilage_list = arcade.process_layer(my_map, "vilage", TILE_SCALING)
        self.wall_list = arcade.process_layer(my_map, "platforms", TILE_SCALING)

        #* --- Слой монеток (пока не реализовано) ---
        coin_layer_name = "coins"
        self.coin_list = arcade.process_layer(my_map, coin_layer_name, COIN_SCALE)

        enemy_layer_name = "enemies"
        self.enemy_list = arcade.process_layer(my_map, enemy_layer_name, TILE_SCALING)


        #* Объекты заднего фона
        #TODO: self.background_list = arcade.tilemap.process_layer(my_map, "Background", TILE_SCALING)

        #* Лестницы
        #TODO: self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders", TILE_SCALING)

        
        # --- Other stuff
        # Set the background color
        # if my_map.background_color:
        #     arcade.set_background_color(my_map.background_color)

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
        
        #TODO: self.background_list.draw()
        #TODO: self.ladder_list.draw()
        #TODO: self.coin_list.draw()

        #* Отрисовка очков на экране, прокрутка по области просмотра
        # score_text = f"Score: {self.score}"
        # arcade.draw_text(score_text, 10 + self.view_left, 10 + view_bottom, arcade.scccolor.BLACK, 18)


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
        self.player_list.update_animation()
        self.wall_list.update()
        #* Процесс обновления спрайтов и игровой логики.

        #* Движение игрока с физическим движком
        self.physics_engine.update()
        self.coin_list.update_animation()
        self.enemy_list.update_animation()

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