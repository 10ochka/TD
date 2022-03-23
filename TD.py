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


# Создаём игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
sprites_map = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')


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


class TileSpawn(pygame.sprite.Sprite):
    """ Тайл начала пути """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.spawn.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


class TileEscape(pygame.sprite.Sprite):
    """ Тайл конца пути """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.escape.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


class TileForest(pygame.sprite.Sprite):
    """ Тайл фона """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.forest.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


class TilePathway(pygame.sprite.Sprite):
    """ Тайл пути """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pathway.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


class TileDamage(pygame.sprite.Sprite):
    """ Тайл, наносящий урон """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.damage.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


class TilePointerRight(pygame.sprite.Sprite):
    """ Указатель, право """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.right.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


class TilePointerLeft(pygame.sprite.Sprite):
    """ Указатель, лево """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.left.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


class TilePointerUp(pygame.sprite.Sprite):
    """ Указатель, верх """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.up.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


class TilePointerDown(pygame.sprite.Sprite):
    """ Указатель, низ """

    def __init__(self, x: int, y: int):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.down.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * x
        self.rect.y = 50 * y


''' Конструктор юнитов '''


class SpriteSoldier(pygame.sprite.Sprite):
    """ Солдат """

    def __init__(self):
        # Создание спрайта
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'sprite.soldier.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        # Х; Y; скорость, должна быть множителем 50 для корректной работы
        self.speed = [1, 0, 2]
        self.rect.x = get_random_spawn()[0]
        self.rect.y = get_random_spawn()[1]
        self.hp_max = 2
        self.hp_current = self.hp_max
        self.width = 50
        self.height = 8

        # Создание полоски здоровья
        self.hp_bar = HpBar()
        all_sprites.add(self.hp_bar)
        self.current_hp_bar = CurrentHpBar()
        all_sprites.add(self.current_hp_bar)

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
            all_sprites.remove(self.hp_bar, self.current_hp_bar)
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
    @staticmethod
    def map_creator():
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


class GameLoop:
    """ Основной цикл игры"""
    @staticmethod
    def run():
        Map().map_creator()
        all_sprites.add(SpriteSoldier())
        running = True
        while running:
            # Держим цикл на правильной скорости
            clock.tick(FPS)

            # Ввод процесса (события)
            for event in pygame.event.get():
                # проверка для закрытия окна
                if event.type == pygame.QUIT:
                    running = False
            # Обновление
            all_sprites.update()

            ''' Рендеринг '''
            # Чтобы не выглядело вырвиглазно
            screen.fill(WHITE)
            sprites_map.draw(screen)
            all_sprites.draw(screen)

            # После отрисовки всего, переворачиваем экран
            pygame.display.flip()
        pygame.quit()


GameLoop().run()
