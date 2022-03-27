from abc import abstractmethod

import pygame
import random
import os

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
wave = True

# Создаём игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()
sprites_units = pygame.sprite.Group()
sprites_map = pygame.sprite.Group()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')


class UnitWave:
    def __init__(self):
        # [[точка_спавна], [порядок_выхода_юнитов], интервал_между_появлением]
        self.wave_storage = {
            '1': [get_random_spawn(), ['Soldier', 'Skeleton', 'Soldier'], 0.6, 2]
        }
        self.__wave_length = 0

        self.__spawn_interval = 0

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

                    if self.wave_storage[__wave_index][1][current_unit_spawn] == 'Soldier':
                        __creating_unit = Soldier(__wave_spawnpoint)
                        sprites_units.add(__creating_unit)
                        tick = 0
                        current_unit_spawn += 1

                    elif self.wave_storage[__wave_index][1][current_unit_spawn] == 'Skeleton':
                        __creating_unit = Skeleton(__wave_spawnpoint)
                        sprites_units.add(__creating_unit)
                        tick = 0
                        current_unit_spawn += 1

                    else:
                        pass

            else:
                wave = False

        else:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                wave = True
                current_unit_spawn = 0
                tick = 0




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


''' Конструктор карты '''


class TileRoot(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.stopgap.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = 50 * x
        self.rect.y = 50 * y
        self.load()

    @abstractmethod
    def load(self):
        """ Загрузка дополнительных параметров """
        pass


class TileSpawn(TileRoot):
    """ Тайл начала пути """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.spawn.png')).convert()


class TileEscape(TileRoot):
    """ Тайл конца пути """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.escape.png')).convert()


class TileForest(TileRoot):
    """ Тайл фона """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.forest.png')).convert()


class TilePathway(TileRoot):
    """ Тайл пути """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pathway.png')).convert()


class TileDamage(TileRoot):
    """ Тайл, наносящий урон """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.damage.png')).convert()


class TilePointerRight(TileRoot):
    """ Указатель, право """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.right.png')).convert()


class TilePointerLeft(TileRoot):
    """ Указатель, лево """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.left.png')).convert()


class TilePointerUp(TileRoot):
    """ Указатель, верх """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.up.png')).convert()


class TilePointerDown(TileRoot):
    """ Указатель, низ """
    def load(self):
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.down.png')).convert()


''' Конструктор юнитов '''


class UnitRoot(pygame.sprite.Sprite):

    def __init__(self, __coordinates: list):
        pygame.sprite.Sprite.__init__(self)
        self.__bar_width = 50
        self.__bar_height = 8
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.stopgap.png')).convert()
        self.rect = self.image.get_rect()
        self.speed = [1, 0, 2]
        self.rect.x = __coordinates[0]
        self.rect.y = __coordinates[1]
        self.__hp_max = 2
        self.__hp_current = self.__hp_max
        self.__max_hp_bar = HpBar()
        sprites_units.add(self.__max_hp_bar)
        self.__current_hp_bar = CurrentHpBar()
        sprites_units.add(self.__current_hp_bar)
        self.load()

    def update(self):
        """ Обновление состояния спрайта """
        self.speed = move_dir(self.speed, self.rect.x, self.rect.y)
        self.rect.x += self.speed[0] * self.speed[2]
        self.rect.y += self.speed[1] * self.speed[2]

        if tile_index(self.rect.x, self.rect.y) == 4:
            self.__hp_current -= 1

        self.__max_hp_bar.set_values(self.rect.x, self.rect.y, self.__bar_width, self.__bar_height)
        self.__current_hp_bar.set_values(self.rect.x, self.rect.y, self.__bar_height, self.__hp_current, self.__hp_max)
        # Умерли/ пошли весь путь
        if tile_index(self.rect.x, self.rect.y) == 2 or self.__hp_current == 0:
            sprites_units.remove(self.__max_hp_bar, self.__current_hp_bar)
            self.kill()

    @abstractmethod
    def load(self):
        pass


class Soldier(pygame.sprite.Sprite):
    """ Солдат """

    def __init__(self, __coordinates: list):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'sprite.soldier.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        # Х; Y; скорость, должна быть множителем 50 для корректной работы
        self.speed = [1, 0, 2]
        self.width = 50
        self.height = 8
        self.rect.x = __coordinates[0]
        self.rect.y = __coordinates[1]
        self.hp_max = 2
        self.hp_current = self.hp_max

        # Создание полоски здоровья
        self.hp_bar = HpBar()
        sprites_units.add(self.hp_bar)
        self.current_hp_bar = CurrentHpBar()
        sprites_units.add(self.current_hp_bar)

    def update(self):
        """ Обновление состояния спрайта """
        self.speed = move_dir(self.speed, self.rect.x, self.rect.y)
        self.rect.x += self.speed[0] * self.speed[2]
        self.rect.y += self.speed[1] * self.speed[2]

        if tile_index(self.rect.x, self.rect.y) == 4:
            self.hp_current -= 1

        self.hp_bar.set_values(self.rect.x, self.rect.y, self.width, self.height)
        self.current_hp_bar.set_values(self.rect.x, self.rect.y, self.height, self.hp_current, self.hp_max)
        # Умерли/ пошли весь путь
        if tile_index(self.rect.x, self.rect.y) == 2 or self.hp_current == 0:
            sprites_units.remove(self.hp_bar, self.current_hp_bar)
            self.kill()


class Skeleton(pygame.sprite.Sprite):
    """ Скелет """

    def __init__(self, __coordinates: list):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'sprite.skeleton.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        # Х; Y; скорость, должна быть множителем 50 для корректной работы
        self.speed = [1, 0, 2]
        self.width = 50
        self.height = 8
        self.rect.x = __coordinates[0]
        self.rect.y = __coordinates[1]
        self.hp_max = 2
        self.hp_current = self.hp_max

        # Создание полоски здоровья
        self.hp_bar = HpBar()
        sprites_units.add(self.hp_bar)
        self.current_hp_bar = CurrentHpBar()
        sprites_units.add(self.current_hp_bar)

    def update(self):
        """ Обновление состояния спрайта """
        self.speed = move_dir(self.speed, self.rect.x, self.rect.y)
        self.rect.x += self.speed[0] * self.speed[2]
        self.rect.y += self.speed[1] * self.speed[2]

        if tile_index(self.rect.x, self.rect.y) == 4:
            self.hp_current -= 1

        self.hp_bar.set_values(self.rect.x, self.rect.y, self.width, self.height)
        self.current_hp_bar.set_values(self.rect.x, self.rect.y, self.height, self.hp_current, self.hp_max)
        # Умерли/ пошли весь путь
        if tile_index(self.rect.x, self.rect.y) == 2 or self.hp_current == 0:
            sprites_units.remove(self.hp_bar, self.current_hp_bar)
            self.kill()


class HpBar(pygame.sprite.Sprite):
    """ Полоска здоровья 1-я часть """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def set_values(self, x: int, y: int, width: int, height: int):
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 1


class CurrentHpBar(pygame.sprite.Sprite):
    """ Полоска здоровья 2-я часть """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def set_values(self, x: int, y: int, height: int, hp_current: int, hp_max: int):
        self.image = pygame.Surface(((hp_current / hp_max) * 50, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 1


class Map:
    """ Создание карты """
    def map_creator(self):
        for __y in range(len(track)):
            for __x in range(len(track[0])):
                tmp_tile = track[__y][__x]
                sprites_map.add(TileForest(__x, __y)) if tmp_tile == 0 else None
                sprites_map.add(TileSpawn(__x, __y)) if tmp_tile == 1 else None
                sprites_map.add(TileEscape(__x, __y)) if tmp_tile == 2 else None
                sprites_map.add(TilePathway(__x, __y)) if tmp_tile == 3 else None
                sprites_map.add(TileDamage(__x, __y)) if tmp_tile == 4 else None
                sprites_map.add(TilePointerRight(__x, __y)) if tmp_tile == 5 else None
                sprites_map.add(TilePointerLeft(__x, __y)) if tmp_tile == 6 else None
                sprites_map.add(TilePointerUp(__x, __y)) if tmp_tile == 7 else None
                sprites_map.add(TilePointerDown(__x, __y)) if tmp_tile == 8 else None


class Game:
    """ Основной цикл игры"""
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

            # После отрисовки всего, переворачиваем экран
            pygame.display.flip()
        pygame.quit()


Game().run()
