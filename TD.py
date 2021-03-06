import os
import random
from abc import abstractmethod
from map_tiles import *
import pygame

WIDTH = 1000
HEIGHT = 700
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

'''
0 - клетка фона
1 - тайл начала пути / спавн
2 - тайл конца пути
3 - тайл пути
4 - тайл, наносящий урон
5 - тайл указателя, право
6 - тайл указателя, лево
7 - тайл указателя, верх
8 - тайл указателя, низ
'''

track = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 3, 3, 3, 3, 3, 0],
    [0, 0, 3, 0, 3, 0, 0, 0, 3, 0],
    [0, 0, 5, 3, 4, 0, 3, 3, 8, 0],
    [0, 0, 3, 0, 0, 0, 3, 0, 3, 0],
    [0, 1, 3, 3, 3, 3, 4, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

tick = 0
current_unit_spawn = 0
wave = False
bar_width = 50
bar_height = 8

# Создаём игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()
sprites_units = pygame.sprite.Group()
sprites_map = pygame.sprite.Group()
sprites_buttons = pygame.sprite.Group()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')


class UnitWave:
    def __init__(self):
        # [[точка_спавна], [порядок_выхода_юнитов], интервал_между_появлением]
        self.wave_storage = {
            '1': [get_random_spawn(), [Soldier, Skeleton, Soldier], 0.6, 2]
        }
        self.__wave_length = 0
        self.__spawn_interval = 0

        self.button = Button(None, 'Wave', RED, [600, 400])

    def wave_creator(self, __wave_index: int):
        global tick
        global current_unit_spawn

        __wave_index = str(__wave_index)
        __wave_spawnpoint = self.wave_storage[__wave_index][0]
        self.__wave_length = len(self.wave_storage[__wave_index][1])
        global wave
        if wave:

            if current_unit_spawn < self.__wave_length:

                if (tick / FPS) == self.wave_storage[__wave_index][2]:
                    tmp_unit_type = self.wave_storage[__wave_index][1][current_unit_spawn]
                    sprites_units.add(tmp_unit_type(__wave_spawnpoint))
                    tick = 0
                    current_unit_spawn += 1

            else:
                wave = False

        else:
            if self.button.get_pressed():
                wave = True
                current_unit_spawn = 0
                tick = 0

    def load(self):
        pass


class Text(pygame.sprite.Sprite):
    def __init__(self, font, text, color, coordinates):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(font, 50)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[0]

    def set_coordinates(self, coordinates):
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]


class Button(pygame.sprite.Sprite):
    def __init__(self, font, text, color, coordinates):
        pygame.sprite.Sprite.__init__(self)
        self.text = Text(font, text, color, (0, 0))
        self.text_rect = pygame.font.Font.size(self.text.font, text)
        self.image = pygame.Surface(self.text_rect)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.__button_position = {
            'top-left': [0, 0],
            'top-right': [WIDTH - self.text_rect[0], 0],
            'bottom-left': [0, HEIGHT - self.text_rect[1]],
            'bottom-right': [WIDTH - self.text_rect[0], HEIGHT - self.text_rect[1]],
        }
        if type(coordinates) is str:
            self.text.set_coordinates(self.__button_position[coordinates])
            self.rect.x = self.__button_position[coordinates][0]
            self.rect.y = self.__button_position[coordinates][1]
        else:
            self.text.set_coordinates(coordinates)
            self.rect.x = coordinates[0]
            self.rect.y = coordinates[1]
        sprites_buttons.add(self)
        sprites_buttons.add(self.text)

    def get_pressed(self):
        __right_mouse_bottom_pressed = pygame.mouse.get_pressed()[0]
        __cursor_position = pygame.mouse.get_pos()
        __on_button = True if (self.rect.x <= __cursor_position[0] <= self.rect.x + self.rect[0] and
                               self.rect.y <= __cursor_position[1] <= self.rect.y + self.rect[1]) else False
        if __right_mouse_bottom_pressed and __on_button:
            return True
        else:
            return False


def tile_index(tmp_x: int, tmp_y: int):
    if tmp_x % 50 == 0 and tmp_y % 50 == 0:
        tmp_x //= 50
        tmp_y //= 50
        current_tile = track[tmp_y][tmp_x]
        return current_tile
    else:
        return False


def move_dir(speed: list, tmp_x: int, tmp_y: int):
    """ "Глаза" всех передвигающихся спрайтов """

    if tmp_x % 50 == 0 and tmp_y % 50 == 0:

        # Встретили указатель, право
        if tile_index(tmp_x, tmp_y) == 5:
            return [1, 0, speed[2]]

        # Встретили указатель, лево
        elif tile_index(tmp_x, tmp_y) == 6:
            return [-1, 0, speed[2]]

        # Встретили указатель, верх
        elif tile_index(tmp_x, tmp_y) == 7:
            return [0, -1, speed[2]]

        # Встретили указатель, низ
        elif tile_index(tmp_x, tmp_y) == 8:
            return [0, 1, speed[2]]

        else:
            speed = [-50 * speed[0], -50 * speed[1], speed[2]]
            dir_list = [
                [0, -50],
                [0, 50],
                [-50, 0],
                [50, 0]
            ]
            tmp_dir_list = []

            opposite_dir = [speed[0], speed[1]]
            dir_list.remove(opposite_dir)
            for direction in dir_list:
                if tile_index(tmp_x + direction[0], tmp_y + direction[1]) > 1:
                    tmp_dir_list.append(direction)
            random_dir = random.choice(tmp_dir_list)
            random_dir = [random_dir[0] / 50, random_dir[1] / 50, speed[2]]
            return random_dir
    else:
        return speed


def get_random_spawn():
    """выбор случайного тайла """
    random_spawn_list = []
    for y in range(len(track)):
        for x in range(len(track[0])):
            if track[y][x] == 1:
                random_spawn_list.append([x, y])
    random_spawn = random.choice(random_spawn_list)
    return [random_spawn[0] * 50, random_spawn[1] * 50]


''' Конструктор юнитов '''


class UnitRoot(pygame.sprite.Sprite):

    def __init__(self, coordinates: list):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.stopgap.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]

        self.speed = [1, 0, 2]

        self.bar_width = bar_width
        self.bar_height = bar_height
        self.hp_max = 2
        self.hp_current = self.hp_max
        self.max_hp_bar = None
        self.current_hp_bar = None

        self.load()

    @abstractmethod
    def load(self):
        """ Загрузка дополнительных параметров """
        pass

    def update(self):
        """ Обновление состояния спрайта """
        self.speed = move_dir(self.speed, self.rect.x, self.rect.y)
        self.rect.x += self.speed[0] * self.speed[2]
        self.rect.y += self.speed[1] * self.speed[2]

        if tile_index(self.rect.x, self.rect.y) == 4:
            self.hp_current -= 1

        sprites_units.remove(self.max_hp_bar)
        self.max_hp_bar = HpBar(self.rect.x, self.rect.y, self.bar_width, self.bar_height)
        sprites_units.add(self.max_hp_bar)

        sprites_units.remove(self.current_hp_bar)
        self.current_hp_bar = CurrentHpBar(self.rect.x, self.rect.y, self.bar_height, self.hp_current, self.hp_max)
        sprites_units.add(self.current_hp_bar)
        # Умерли/ пошли весь путь
        if tile_index(self.rect.x, self.rect.y) == 2 or self.hp_current == 0:
            sprites_units.remove(self.max_hp_bar, self.current_hp_bar)
            self.kill()


class Soldier(UnitRoot):
    """ Солдат """

    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'sprite.soldier.png')).convert()
        self.image.set_colorkey(WHITE)
        # Х; Y; скорость, должна быть множителем 50 для корректной работы
        self.speed = [1, 0, 2]
        self.hp_max = 3
        self.hp_current = self.hp_max


class Skeleton(UnitRoot):
    """ Скелет """

    def load(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'sprite.skeleton.png')).convert()
        self.image.set_colorkey(WHITE)
        # Х; Y; скорость, должна быть множителем 50 для корректной работы
        self.speed = [1, 0, 2]
        self.hp_max = 2
        self.hp_current = self.hp_max


class HpBar(pygame.sprite.Sprite):
    """ Полоска здоровья 1-я часть """

    def __init__(self, x: int, y: int, width: int, height: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 1


class CurrentHpBar(pygame.sprite.Sprite):
    """ Полоска здоровья 2-я часть """

    def __init__(self, x: int, y: int, height: int, hp_current: int, hp_max: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(((hp_current / hp_max) * 50, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 1


class Map:
    """ Создание карты """

    def __init__(self):
        self.tiles = {
            0: TileForest,
            1: TileSpawn,
            2: TileEscape,
            3: TilePathway,
            4: TileDamage,
            5: TilePointerRight,
            6: TilePointerLeft,
            7: TilePointerUp,
            8: TilePointerDown
        }

    def map_creator(self):
        for __y in range(len(track)):
            for __x in range(len(track[0])):
                tmp_tile = track[__y][__x]
                sprites_map.add(self.tiles[tmp_tile](__x, __y))


class Game:
    """ Основной цикл игры"""
    def __init__(self):
        self.a = 0

    def run(self):
        Map().map_creator()

        running = True
        while running:
            # Держим цикл на правильной скорости
            clock.tick(FPS)
            UnitWave().wave_creator(1)
            # Ввод процесса (события)
            for event in pygame.event.get():
                # проверка для закрытия окна
                if event.type == pygame.QUIT:
                    running = False
            # Обновление
            sprites_units.update()

            global tick
            tick += 1
            print(tick)
            ''' Рендеринг '''
            # Чтобы не выглядело вырвиглазно
            screen.fill(WHITE)
            sprites_map.draw(screen)
            sprites_units.draw(screen)
            sprites_buttons.draw(screen)

            # После отрисовки всего, переворачиваем экран
            pygame.display.flip()
        pygame.quit()


Game().run()
