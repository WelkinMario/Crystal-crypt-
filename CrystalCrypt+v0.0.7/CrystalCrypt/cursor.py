import pygame

class Cursor(object):

    def __init__(self, setting, screen):
        self.screen = screen
        self.setting = setting

        self.image = pygame.image.load('map/maptileChosenBlank.bmp')
        self.rect  = self.image.get_rect()
        self.width = self.rect.width
        self.height= self.rect.height

        self.rect.top = setting.map_top
        self.rect.left = setting.map_left

        self.start = False

        self.health = setting.max_health
        self.stamina = setting.max_stamina
        self.loot = 0

        self.item_get = False
        self.key_get = False
        self.chest_get = False
        self.potion_get = 0

    def update(self):
        self.screen.blit(self.image, self.rect)

    def get_position(self):
        self.x = int((self.rect.left - self.setting.map_left) / 50)
        self.y = int((self.rect.top - self.setting.map_top) / 50)
        position = [self.x, self.y]
        return position

    def stats_limit(self):
        if self.stamina > self.setting.max_stamina:
            self.stamina = self.setting.max_stamina
        if self.health > self.setting.max_health:
            self.health = self.setting.max_health

    def change_image(self, cls):
        self.image = pygame.image.load('map/maptileChosen{}.bmp'.format(cls))

    def respawn(self):
        self.start = False
        self.change_image('Blank')
        self.item_get = False
        self.key_get = False
        self.chest_get = False
        self.potion_get = 0
        self.loot = 0
        self.health = self.setting.max_health
        self.stamina = self.setting.max_stamina
