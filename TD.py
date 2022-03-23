import pygame
import random
import os

WIDTH = 1000
HEIGHT = 700
FPS = 60

# Задаем цвета
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
            for n in range(3):
                if tile_index(tmp_x + dir_list[n][0], tmp_y + dir_list[n][1]) > 1:
                    tmp_dir_list.append(dir_list[n])
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


# Создаём игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("!")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

''' Конструктор карты '''


class TileSpawn(pygame.sprite.Sprite):
    """ Тайл начала пути """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.spawn.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


class TileEscape(pygame.sprite.Sprite):
    """ Тайл конца пути """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.escape.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


class TileForest(pygame.sprite.Sprite):
    """ Тайл фона """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.forest.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


class TilePathway(pygame.sprite.Sprite):
    """ Тайл пути """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pathway.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


class TileDamage(pygame.sprite.Sprite):
    """ Тайл, наносящий урон """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.damage.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


class TilePointerRight(pygame.sprite.Sprite):
    """ Указатель, право """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.right.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


class TilePointerLeft(pygame.sprite.Sprite):
    """ Указатель, лево """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.left.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


class TilePointerUp(pygame.sprite.Sprite):
    """ Указатель, верх """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.up.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


class TilePointerDown(pygame.sprite.Sprite):
    """ Указатель, низ """

    def __init__(self):
        # Создаем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'tile.pointer.down.png')).convert()
        self.rect = self.image.get_rect()
        # Помещаем в нужное место
        self.rect.x = 50 * track_x
        self.rect.y = 50 * track_y


''' Конструктор юнитов '''


class SpriteSoldier(pygame.sprite.Sprite):
    """ Солдат """

    def __init__(self):
        # Создаем спрайт
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

        self.hp_bar.set_values(self.rect.x, self.rect.y, self.hp_max)
        self.current_hp_bar.set_values(self.rect.x, self.rect.y, 8, self.hp_current, self.hp_max)
        # Умерли/ пошли весь путь
        if tile_index(self.rect.x, self.rect.y) == 2 or self.hp_current == 0:
            self.kill()


class HpBar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 50
        self.height = 8
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.hp = 0

    def set_values(self, x: int, y: int, hp_max: int):
        self.rect.x = x
        self.rect.y = y + 2


class CurrentHpBar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = 10, 10
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

    def set_values(self, x: int, y: int, height: int, hp_current: int, hp_max: int):
        self.height = height
        self.width = (hp_current / hp_max) * 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 2


# Создание карты
for track_y in range(len(track)):
    for track_x in range(len(track[0])):
        tmp_tile = track[track_y][track_x]
        if tmp_tile == 0:
            all_sprites.add(TileForest())
        if tmp_tile == 1:
            all_sprites.add(TileSpawn())
        if tmp_tile == 2:
            all_sprites.add(TileEscape())
        if tmp_tile == 3:
            all_sprites.add(TilePathway())
        if tmp_tile == 4:
            all_sprites.add(TileDamage())
        if tmp_tile == 5:
            all_sprites.add(TilePointerRight())
        if tmp_tile == 6:
            all_sprites.add(TilePointerLeft())
        if tmp_tile == 7:
            all_sprites.add(TilePointerUp())
        if tmp_tile == 8:
            all_sprites.add(TilePointerDown())
all_sprites.add(SpriteSoldier())


# Цикл игры
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

    # Рендеринг
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
#ggfgffggf
