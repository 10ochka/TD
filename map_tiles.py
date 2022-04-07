import pygame
import os
from abc import abstractmethod


''' Конструктор карты '''


class TileRoot(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.image_dir = ""
        self.get_path(self)
        self.tile_path = [
            'spawn', 'escape', 'forest', 'pathway', 'damage',
            'pointer.right', 'pointer.left', 'pointer.up', 'pointer.down'
        ]
        self.tile_path = [os.path.join(self.image_dir, 'tile.' + i + '.png') for i in self.tile_path]
        self.image = pygame.image.load(os.path.join(self.image_dir, 'tile.stopgap.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect[2] * x
        self.rect.y = self.rect[2] * y
        self.load()

    @abstractmethod
    def load(self):
        """ Загрузка дополнительных параметров """
        pass

    @staticmethod
    def get_path(self):
        if self.image_dir == "":
            self.image_dir = os.path.join(os.path.dirname(__file__), 'img')
        return self.image_dir


class TileSpawn(TileRoot):
    """ Тайл начала пути """

    def load(self):
        self.image = pygame.image.load(self.tile_path[0])


class TileEscape(TileRoot):
    """ Тайл конца пути """

    def load(self):
        self.image = pygame.image.load(self.tile_path[1])


class TileForest(TileRoot):
    """ Тайл фона """

    def load(self):
        self.image = pygame.image.load(self.tile_path[2])


class TilePathway(TileRoot):
    """ Тайл пути """

    def load(self):
        self.image = pygame.image.load(self.tile_path[3])


class TileDamage(TileRoot):
    """ Тайл, наносящий урон """

    def load(self):
        self.image = pygame.image.load(self.tile_path[4])


class TilePointerRight(TileRoot):
    """ Указатель, право """

    def load(self):
        self.image = pygame.image.load(self.tile_path[5])


class TilePointerLeft(TileRoot):
    """ Указатель, лево """

    def load(self):
        self.image = pygame.image.load(self.tile_path[6])


class TilePointerUp(TileRoot):
    """ Указатель, верх """

    def load(self):
        self.image = pygame.image.load(self.tile_path[7])


class TilePointerDown(TileRoot):
    """ Указатель, низ """

    def load(self):
        self.image = pygame.image.load(self.tile_path[8])