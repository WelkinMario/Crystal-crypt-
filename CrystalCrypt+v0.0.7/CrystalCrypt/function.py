import sys
import pygame
import math
from maps import Maptile
from ui import Item_UI
from random import *
import test as t

class Arguments():
    '''arguments summary'''
    def __init__(self, setting, screen, health_ui, stamina_ui,
                 hero, maps, items, cursor, text):
        self.setting = setting
        self.screen = screen
        self.health_ui = health_ui
        self.stamina_ui = stamina_ui
        self.hero = hero
        self.maps = maps
        self.items = items
        self.cursor = cursor
        self.text = text

def update_screen(maps, items, cursor, args):
    args.screen.fill(args.setting.bg_color)

    maps.update()
    items.update()
    cursor.update()
    args.hero.update()
    
    #change UI's image
    cursor.stats_limit()
    args.stamina_ui.change_image('stamina{}'.format(cursor.stamina))
    args.health_ui.change_image('health{}'.format(cursor.health))
    args.health_ui.update()
    args.stamina_ui.update()
    
    draw_rec(args)
    pygame.display.flip()

def check_events(maps, items, cursor, args):
    '''game_function'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            KEYDOWN_manipulation(event, maps, items, cursor, args)
            
def KEYDOWN_manipulation(event, maps, items, cursor, args):
    '''Game manipulation:'''
    setting = args.setting
    #move
    if cursor.health > 0:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            if cursor.rect.right < setting.map_right:
                cursor.rect.left += cursor.width
                delta_image(setting, maps, items, cursor, args)
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            if cursor.rect.left > setting.map_left:
                cursor.rect.left -= cursor.width
                delta_image(setting, maps, items, cursor, args)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if cursor.rect.bottom < setting.map_bottom:
                cursor.rect.top += cursor.height
                delta_image(setting, maps, items, cursor, args)
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            if cursor.rect.top > setting.map_top:
                cursor.rect.top -= cursor.height
                delta_image(setting, maps, items, cursor, args)
        #use potion
        elif event.key == pygame.K_c:
            use_potion(items, cursor, args)
    #choose the initial position
    if event.key == pygame.K_SPACE:
        game_start(setting, maps, items, cursor, args)
    #restart the game
    elif event.key == pygame.K_r:
        game_retry(setting, maps, items, cursor, args)
        restore_full(cursor, args)
    #exit the game        
    elif event.key == pygame.K_q:
        sys.exit()
    #refill
    elif event.key == pygame.K_x:
        restore_full(cursor, args)
    #for test
    elif event.key == pygame.K_z:
        t.test_map(maps, cursor)

def game_start(setting, maps, items, cursor, args):
    if cursor.start == False:
        #choose position at the beginning
        cursor.start = True
        for maptile in maps:
            if maptile.code == cursor.get_position():
                explore(setting, maptile, maps, items, cursor, args)
                break

def game_retry(setting, maps, items, cursor, args):   
    maps.empty()
    items.empty()
    cursor.respawn()
    setting.retry()
    generate_map(setting, maps, args)
    args.hero.normal()

def restore_full(cursor, args):
    cursor.health = args.setting.max_health
    cursor.stamina = args.setting.max_stamina
    args.hero.normal()

def use_potion(items, cursor, args):
    if cursor.potion_get > 0:
        cursor.health += args.setting.restore_health
        cursor.potion_get -= 1
        use_one = 1
        for item in items:
            if item.cls == 'Potion':
                if use_one > 0:
                    item.cls = 'EmptyPotion'
                    item.change_image()
                    use_one -= 1
                break

def delta_image(setting, maps, items, cursor, args):
    #change maps/cursor/hero's image
    for maptile in maps:
        if maptile.code == cursor.get_position():
            explore(setting, maptile, maps, items, cursor, args)
            break
    #action consumption
    if cursor.start == True:
        if cursor.stamina > 0:
            cursor.stamina -= 1
        else:
            cursor.health -= 1
    if cursor.stamina == 0 and cursor.health > 0 and not cursor.item_get:
        args.hero.bleed()
    elif cursor.stamina > 0 and not cursor.item_get:
        args.hero.normal()
    elif cursor.health == 0:
        args.hero.died()
        print(args.text.dead_massage)

def explore(setting, maptile, maps, items, cursor, args):
    cursor.change_image(maptile.cls)
    cursor.item_get = False
    #explore the maptile(change maptile/cursor's image)
    if cursor.start:
        if maptile.state == False:
            maptile.chosen()
            maptile.change_image()
            cursor.change_image(maptile.cls)
            #find a crystal
            if maptile.type == True:
                cursor.stamina += setting.restore_stamina
                args.hero.smile()
            if maptile.type_treasure >= 0:
                cursor.item_get = True
            #find an item
            if maptile.type_treasure > 0:
                new_item = Item_UI(args, maptile.cls)
                new_item.rect.right = setting.map_right - len(items) * new_item.width
                items.add(new_item)
                args.hero.smile()
                #find key
                if maptile.type_treasure == 1:
                    cursor.key_get = True
                #find chest
                elif maptile.type_treasure == 2:
                    cursor.chest_get = True
                #find a potion
                elif maptile.type_treasure == 3:
                    cursor.potion_get += 1
                #find a compass
                elif maptile.type_treasure == 4:
                    if not cursor.key_get:
                        for key in maps:
                            if key.type_treasure == 1:
                                key.reveal_item()
                                break
                    elif not cursor.chest_get:
                        for chest in maps:
                            if chest.type_treasure == 2:
                                chest.reveal_item()
                                break
        #find the exit
        if maptile.type_treasure == 5:
            game_retry(setting, maps, items, cursor, args)
        #find both key and chest, reveal the exit
        if cursor.key_get and cursor.chest_get:
            delta_type_extra(maps, setting.blank_maps, -1, args)
            cursor.key_get = False
            cursor.chest_get = False

def generate_map(setting, maps, args):
    '''For initialization:'''
    #create a map
    maptile = Maptile(args)
    width = height = maptile.rect.width
    #create maps
    for y in range(setting.height_num):
        for x in range(setting.width_num):
            new_map = Maptile(args)
            new_map.code = [x, y]
            new_map.rect.top = setting.map_top + y * height
            new_map.rect.left= setting.map_left+ x * width
            maps.add(new_map)
    #place crystals, key and chest
    for num in range(setting.crystals_num):
        delta_type(setting, maps, num)
    #place exit, potion and any other events
    for maptile in maps:
        if maptile.type == False and maptile.num == 0:
            setting.blank_maps.append(maptile.code)
    events_num = math.ceil(len(setting.blank_maps)/10)
    for num in range(events_num):
        delta_type_extra(maps, setting.blank_maps, num, args)
            
def delta_type(setting, maps, num):
    #generate crystals
    x = randrange(setting.width_num)
    y = randrange(setting.height_num)#generate a random position
    for maptile in maps:
        if maptile.code == [x, y]:#find the map according to that position
            if maptile.type == False:
                #yes, find it and it is not a crystal
                maptile.type = True
                if num == 0:#make 1st crystal become 'key'
                    maptile.type_treasure = 1
                    setting.key_code = maptile.code
                elif num == 1:#make 2nd crystal become 'chest'
                    if maptile.cal_distance(setting.key_code) > 5:
                        maptile.type_treasure = 2
                    else:#make key and chest far enough
                        maptile.type = False
                        delta_type(setting, maps, num)
                else:#make rest of crystals become 'crystal'
                    maptile.type_treasure = 0
                delta_num(setting, maps, x, y)
                break
            else:
                #it's already a crystal, go back to find another one
                delta_type(setting, maps, num)

def delta_type_extra(maps, blank_maps, num, args):
    '''
    note:
        this function has potential problem
        when there are not enough maptiles in blank_maps
    '''
    position = choice(blank_maps)
    position_cheak = False
    for maptile in maps:
        if maptile.code == position:
            if maptile.event == False:
                maptile.event = True
                if num == -1:
                    maptile.type_treasure = 5#exit
                    maptile.image = pygame.image.load('map/maptileExit.bmp')
                elif num == 0: 
                    maptile.type_treasure = 4#compass
                elif num == 1:
                    maptile.type_treasure = 3#potion
                    args.setting.last_code.append(maptile.code)
                else:
                    for code in args.setting.last_code:
                        if maptile.cal_distance(code) > 2:
                            position_cheak = True
                        else:
                            position_cheak = False
                            break
                    if position_cheak:
                        maptile.type_treasure = 3#potion
                        args.setting.last_code.append(maptile.code)
                    else:
                        maptile.event = False
                        delta_type_extra(maps, blank_maps, num, args)
                break
            else:
                delta_type_extra(maps, blank_maps, num, args)

def delta_num(setting, maps, x, y):
    max_x = setting.width_num - 1
    max_y = setting.height_num - 1
    #change the number around crystals/items
    for map_around in maps:
        if x != 0:
            if map_around.code == [x-1, y]:
                map_around.num += 1
        if x != max_x:
            if map_around.code == [x+1, y]:
                map_around.num += 1
        if y != 0:
            if map_around.code == [x, y-1]:
                map_around.num += 1
        if y != max_y:
            if map_around.code == [x, y+1]:
                map_around.num += 1
        if x != 0 and y != 0:
            if map_around.code == [x-1, y-1]:
                map_around.num += 1
        if x != max_x and y != max_y:
            if map_around.code == [x+1, y+1]:
                map_around.num += 1
        if x != 0 and y != max_y:
            if map_around.code == [x-1, y+1]:
                map_around.num += 1
        if x != max_x and y != 0:
            if map_around.code == [x+1, y-1]:
                map_around.num += 1

def draw_rec(args):
    setting = args.setting
    margins = [setting.rect_top, setting.rect_bottom,
               setting.rect_left, setting.rect_right]
    for margin in margins:
        pygame.draw.rect(args.screen, setting.margin_color, margin)
