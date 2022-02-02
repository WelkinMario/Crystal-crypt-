import pygame

class Setting():

    def __init__(self):
        #screen_character
        self.bg_color = (150, 150, 150)
        self.caption = "Crystal Crypt v0.0.7"

        #ui_settings
        self.ui_height = 100
        self.unit_size = 50
        self.margin_width = 5
        self.margin_double = 10
        
        #map_width_index
        self.width_num = 15 #map's number in a row
        self.height_num= 10 #in a colunm
        self.map_width = self.width_num * self.unit_size #map's number * one map's width
        self.map_height = self.height_num * self.unit_size
        self.map_left = self.margin_width
        self.map_top  = self.ui_height + self.margin_width
        self.map_right = self.map_left + self.map_width
        self.map_bottom= self.map_top + self.map_height
        
        #screen_size
        self.screen_width = self.map_width + 2*self.margin_width
        self.screen_height= self.map_height+ 2*self.margin_width + self.ui_height
        
        #crystals
        self.crystals_num = 20
        
        #cursor_character
        self.max_stamina = 10
        self.restore_stamina = 6

        self.max_health = 6
        self.restore_health = 3

        #game_data
        self.number = 0
        self.key_code = []
        self.chest_code = []
        self.blank_maps = []
        self.last_code = []
        
        #margin_character
        self.margin_color = (255, 255, 255)
        
        self.h_width = self.map_width + 2*self.margin_width
        self.h_height = self.map_top - self.ui_height
        self.v_width = self.margin_width
        self.v_height = self.map_height

        self.rect_top = pygame.Rect(0, self.ui_height,
                                     self.h_width, self.h_height)
        self.rect_bottom = pygame.Rect(0, self.map_bottom,
                                     self.h_width, self.h_height)
        self.rect_left = pygame.Rect(0, self.map_top,
                                     self.v_width, self.v_height)
        self.rect_right = pygame.Rect(self.map_right, self.map_top,
                                     self.v_width, self.v_height)

    def retry(self):
        self.number = 0
        self.key_code = []
        self.chest_code = []
        self.blank_maps = []
        self.last_code = []
        
