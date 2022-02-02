import pygame
from pygame.sprite import Group

import function as f
from settings import Setting
from text import Text
from cursor import Cursor
from ui import Stats_UI
from hero import Hero

def run_game():
    pygame.init()
    setting = Setting()
    screen = pygame.display.set_mode(
        (setting.screen_width, setting.screen_height))
    pygame.display.set_caption(setting.caption)
    text = Text(setting, screen)
    print(text.instruction)
    
    maps = Group()
    items= Group()
    cursor = Cursor(setting, screen)
    health_ui = Stats_UI(setting, screen, 'health{}'.format(setting.max_health), 0)
    stamina_ui = Stats_UI(setting, screen, 'stamina{}'.format(setting.max_stamina), 1)
    hero = Hero(screen)

    args = f.Arguments(setting, screen, health_ui, stamina_ui,
                       hero, maps, items, cursor, text)

    f.generate_map(setting, maps, args)
       
    while True:
        
        f.check_events(maps, items, cursor, args)
        
        f.update_screen(maps, items, cursor, args)

run_game()
