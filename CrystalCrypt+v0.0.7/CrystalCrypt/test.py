import pygame

def test_map(maps, cursor):
    for maptile in maps:
        maptile.chosen()
        maptile.change_image()
        if maptile.code == cursor.get_position():
            cursor.change_image(maptile.cls)

def add_new_item(items, cls, type_treasure, args):
    new_item = Item_UI(args, cls)
    new_item.rect.right = setting.map_right - len(items) * new_item.width
    items.add(new_item)
    #key
    if type_treasure == 1:
        args.cursor.key_get = True
    #chest
    elif type_treasure == 2:
        args.cursor.chest_get = True
    #potion
    elif type_treasure == 3:
        args.cursor.potion_get += 1
    #compass
    elif type_treasure == 4:
        if not args.cursor.key_get:
            for key in args.maps:
                if key.type_treasure == 1:
                    key.reveal_item()
                    break
        elif not args.cursor.chest_get:
            for chest in args.maps:
                if chest.type_treasure == 2:
                    chest.reveal_item()
                    break
