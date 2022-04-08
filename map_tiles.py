import pygame
import os
from abc import abstractmethod


''' Конструктор карты '''


class TileRoot(pygame.sprite.Sprite):

    _IMAGE_DIR = ""

    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.load_path()
        self.image = pygame.image.load(os.path.join(self._IMAGE_DIR, 'tile.stopgap.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect[2] * x
        self.rect.y = self.rect[2] * y
        self.load()

    @abstractmethod
    def load(self):
        """ Загрузка дополнительных параметров """
        pass

    def load_path(self):
        if TileRoot._IMAGE_DIR == "":
            TileRoot._IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'img')


class TileSpawn(TileRoot):
    """ Тайл начала пути """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.spawn.png'))


class TileEscape(TileRoot):
    """ Тайл конца пути """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.escape.png'))


class TileForest(TileRoot):
    """ Тайл фона """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.forest.png'))


class TilePathway(TileRoot):
    """ Тайл пути """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.pathway.png'))


class TileDamage(TileRoot):
    """ Тайл, наносящий урон """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.damage.png'))


class TilePointerRight(TileRoot):
    """ Указатель, право """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.pointer.right.png'))


class TilePointerLeft(TileRoot):
    """ Указатель, лево """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.pointer.left.png'))


class TilePointerUp(TileRoot):
    """ Указатель, верх """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.pointer.up.png'))


class TilePointerDown(TileRoot):
    """ Указатель, низ """

    def load(self):
        self.image = pygame.image.load(os.path.join(TileRoot._IMAGE_DIR, 'tile.pointer.down.png'))