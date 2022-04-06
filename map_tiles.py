import pygame
import os
from abc import abstractmethod

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

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