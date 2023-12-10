import pygame, os
from inventory import *
from npc import *
from setting import *
from game_data import game_asset
from func_ex import import_csv,cut_graphics
from Tile import StaticTile,AnimatedTile
from player import Player

class AllSprite(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.zoom_scale = 2
        self.int_surf_size = (1280,1120)
        self.int_surf = pygame.Surface(self.int_surf_size, pygame.SRCALPHA)
        self.int_rect = self.int_surf.get_rect(center=(center))
        self.int_surf_size_vector = pygame.math.Vector2(self.int_surf_size)
        self.int_offset = pygame.math.Vector2()
        self.int_offset.x = self.int_surf_size[0]//2 - center[0]
        self.int_offset.y = self.int_surf_size[1]//2 - center[1]

   
    def center_cam(self,target):
        self.offset.x = target.rect.centerx - center[0] - 155
        self.offset.y = target.rect.centery - center[1]*1.55 - 60

    def custom_draw(self,player):
        self.center_cam(player)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.int_surf.blit(sprite.image,offset_pos)

        scaled_surf = pygame.transform.scale(self.int_surf, self.int_surf_size_vector*self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=center)
        self.display_surf.blit(scaled_surf,scaled_rect)

class Game:
    def __init__(self,game_data,screen):
        self.all_sprite = AllSprite()
        self.screen = screen
        self.dt = 1
        ground_layout = import_csv(game_data['ground'])
        self.ground_sprite = self.tile_group(ground_layout, 'ground', ground)

        water_layout = import_csv(game_data['water'])
        self.water_sprite = self.tile_group(water_layout, 'water', water)

        bridge_layout = import_csv(game_data['bridge'])
        self.bridge_sprite = self.tile_group(bridge_layout, 'bridge', bridge)

        decor_layout = import_csv(game_data['decor'])
        self.decor_sprite = self.tile_group(decor_layout, 'decor', decor)

        self.default_layer = pygame.sprite.LayeredUpdates()
        
        self.npc_sprite = pygame.sprite.LayeredUpdates()
        self.farmer = Farmer(self, self.npc_sprite)
        
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player = Player(self, self.player_sprite, self.water_sprite, self.dt)
        

        self.all_sprite.add(self.ground_sprite,self.bridge_sprite,self.decor_sprite,self.water_sprite,self.player_sprite,self.npc_sprite)

        # inventory
        self.inventory_slot = []
        self.inventory_group = []
        self.farmer_group = []
        self.farmer_button = []
        self.inventory = {}
        
        self.panel = "False"
        self.npc_panel = "False"
        
        if os.path.getsize('inventory_data.txt') != 0:
            with open('inventory_data.txt', 'r') as file:
                self.res = eval(file.readline())
                self.inventory = self.res
                self.res = eval(file.readline())
                self.player.gold_stat.set_amount(self.res)
                file.close()
        
        self.all_inventory_layer = pygame.sprite.LayeredUpdates()
        self.all_farmer_layer = pygame.sprite.LayeredUpdates()
        self.above_text_layer = pygame.sprite.LayeredUpdates()
        
        self.inventory_panel = PageInventory(self, (960-464)/2, (640-314)/2)
        self.inventory_group.append(self.inventory_panel)
        
        self.inventory_button = InventoryButton(self, 32, 32, 77, 76, 'assets/inventory/inventory_button.png', self.default_layer)
        self.button = Button(self, 459, 250, 24, 28, 'assets/stats/button_room.png', self.default_layer)
        
        self.page_farmer = PageFarmer(self, self.player, (960-314)/2, (640-448)/2)
        self.farmer_group.append(self.page_farmer)
        
        self.inventory_group += self.inventory_slot
        self.farmer_group += self.farmer_button

    def tile_group(self,layout, type, layer):
        sprite_group = pygame.sprite.Group()
        tile_list = cut_graphics(game_asset[type])
        for row_index,row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index*TILESIZE
                    y = row_index*TILESIZE
                    if type == 'water':
                        tile_surf = tile_list
                        Sprite = AnimatedTile(TILESIZE,x,y,tile_surf, layer)
                    else:
                        tile_surf = tile_list[int(value)]
                        Sprite = StaticTile(TILESIZE,x,y, tile_surf, layer)
                    sprite_group.add(Sprite)
        return sprite_group

    def run(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pressed = pygame.mouse.get_pressed()

        self.all_sprite.update()
        
        self.all_sprite.custom_draw(self.player)
        
        self.default_layer.draw(self.screen)
        
        self.inventory_panel.draw()
        self.inventory_panel.update()
        
        self.page_farmer.draw()
        self.page_farmer.update()
        
        self.all_farmer_layer.update()
        self.all_inventory_layer.update()
        self.above_text_layer.update()
        self.default_layer.update()
        
        pygame.display.update()