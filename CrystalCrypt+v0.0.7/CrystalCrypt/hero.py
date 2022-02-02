import pygame

class Hero():

    def __init__(self,screen):
        self.screen = screen

        self.image = pygame.image.load('hero/HeroNormal.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.left = 0
        self.rect.top = 0

    def normal(self):
        self.image = pygame.image.load('hero/HeroNormal.bmp')

    def smile(self):
        self.image = pygame.image.load('hero/HeroSurprised.bmp')

    def bleed(self):
        self.image = pygame.image.load('hero/HeroTired.bmp')

    def died(self):
        self.image = pygame.image.load('hero/HeroDead.bmp')

    def update(self):
 	
        self.screen.blit(self.image, self.rect)

