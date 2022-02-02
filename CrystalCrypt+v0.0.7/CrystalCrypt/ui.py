import pygame
from pygame.sprite import Sprite

class Stats_UI(object):

    def __init__(self, setting, screen, cls, order):
        self.screen = screen

        self.image = pygame.image.load('ui/{}.bmp'.format(cls))
        self.rect  = self.image.get_rect()

        self.rect.top = order * self.rect.height
        self.rect.left= 100

    def change_image(self, cls):
        self.image = pygame.image.load('ui/{}.bmp'.format(cls))

    def update(self):
        self.screen.blit(self.image, self.rect)

class Item_UI(Sprite):

    def __init__(self, args, item_cls):
        super(Item_UI, self).__init__()
        self.screen = args.screen

        self.image = pygame.image.load('ui/{}.bmp'.format(item_cls))
        self.rect  = self.image.get_rect()
        self.width = self.rect.width

        self.rect.right = 0
        self.rect.top = 0

        self.cls = item_cls

    def change_image(self):
        self.image = pygame.image.load('ui/{}.bmp'.format(self.cls))

    def update(self):
        self.screen.blit(self.image, self.rect)
