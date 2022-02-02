import pygame
from pygame.sprite import Sprite
from random import *

class Maptile(Sprite):
    def __init__(self, args):
        super(Maptile, self).__init__()
        self.screen = args.screen
        self.image = pygame.image.load('map/mapclear0.bmp')
        self.rect = self.image.get_rect()
        
        self.code = [0,0]#position/coordinates
        self.type = False #"False" means it's not a crystal/"True" means a crystal
        self.event = False
        self.num = 0 #the number of crystals around it.
        
        self.state = False #"False" means it's unchosen/"True" means it's been chosen
        self.cls = 'Blank'
        self.type_treasure = -1
        self.cls_type = ['Crystal',#0
                         'Key',#1
                         'Chest',#2
                         'Potion',#3
                         'Compass',#4
                         'Exit',#5
                         ]
        self.event_type = []#pass

    def chosen(self):

        self.state = True

    def change_image(self):
        if self.type_treasure == -1:
            self.cls = 'Num{}'.format(self.num)
        else:
            self.cls = self.cls_type[self.type_treasure]
        if self.state == False:
            self.image = pygame.image.load('map/mapclear0.bmp')
        else:
            self.image = pygame.image.load('map/maptile{}.bmp'.format(self.cls))

    def reveal_item(self):
        self.image = pygame.image.load('map/maptileItem.bmp')

    def cal_distance(self, code):
        d_x = abs(self.code[0] - code[0])
        d_y = abs(self.code[1] - code[1])
        d = d_x + d_y
        return d

    def update(self):
        self.screen.blit(self.image, self.rect)

