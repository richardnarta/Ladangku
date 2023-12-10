import pygame
from timer import *
from inventory import Spritesheet
from func_ex import get_animation_player
from game_data import game_asset
from item_data import *
from setting import *

class Farmer(pygame.sprite.Sprite):
    def __init__(self,game, group):
        self.game = game
        self.groups = group
        self._layer = npc
        super().__init__(group)
        self.animation = get_animation_player(game_asset['farmer'], FARMER_ANIMATION_WIDTH, FARMER_ANIMATION_HEIGHT)
        self.current_frame = 0
        self.image = self.animation[0][self.current_frame]
        self.rect = self.image.get_rect(center = (500,600))
        self.animationcd = 750
        self.lastupdate = pygame.time.get_ticks()
        
    def animate(self):
        currenttime = pygame.time.get_ticks()
        
        if self.current_frame == 1:
            self.current_frame = -1
        
        if currenttime - self.lastupdate >= self.animationcd:
            self.current_frame+=1
            self.lastupdate = currenttime
            
        self.image = self.animation[0][self.current_frame]
    
    def update(self):
        self.animate()
        
class PageFarmer(pygame.sprite.Sprite):
    def __init__(self, game, player, x, y):
        self.game = game
        self.player = player
        self.timer = Timer(300)
        
        self._layer = 1
        self.groups = self.game.all_farmer_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x 
        self.y = y
        
        self.farmer_page = Spritesheet('assets/npc/farmer/panel.png')
        self.image = self.farmer_page.get_sprite(0, 0, 314, 448)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.farmer_page_close_button = Button(self.game, self.rect.right - 20, self.rect.top - 11,
                                                           35, 35, 'assets/npc/farmer/close_button.png', self.game.npc_sprite)
        self.game.farmer_group.append(self.farmer_page_close_button)

        self.game.default_layer.remove(self.game.button)
        
        pady = 0
        for i in range(5):
            if i<3 :
                self.button = Button(self.game, self.rect.right - 105, self.rect.top + 51 + pady, 61, 26,
                                     'assets/npc/farmer/sell_button.png', self.game.npc_sprite)
                self.button.type = 'sell'
            else :
                self.button = Button(self.game, self.rect.right - 105, self.rect.top + 51 + pady, 61, 26,
                                     'assets/npc/farmer/buy_button.png', self.game.npc_sprite)
                self.button.type = 'buy'
                
            self.game.farmer_button.append(self.button)
            self.button.id = npc_id_item[i]
            pady += 80
        
    def draw(self):
        pass
        if self.game.npc_panel == "True":
            self.game.all_farmer_layer.draw(self.game.screen)
        
    def update(self):
        self.timer.update()
        
        if self.game.npc_panel == "True":
            for button in self.game.farmer_button:
                if not self.timer.active:
                    if button.is_pressed(self.game.mouse_pos, self.game.mouse_pressed):
                        if button.type == 'sell':
                            if button.id in self.game.inventory:
                                if self.game.inventory[button.id]['amount'] > 1:
                                    self.game.inventory_panel.edit('sub', button.id, 1)
                                    self.game.player.gold_stat.set_amount(self.game.player.gold_stat.get_amount() + self.game.inventory[button.id]['price'])          
                        elif button.type == 'buy':
                            if self.game.player.gold_stat.get_amount() > item_id[button.id][button.id]['price']:
                                self.game.inventory_panel.edit('add', button.id, 1)
                                self.game.player.gold_stat.set_amount(self.game.player.gold_stat.get_amount() - self.game.inventory[button.id]['price'])
                        self.timer.activate()
        
        if self.farmer_page_close_button.is_pressed(self.game.mouse_pos, self.game.mouse_pressed) and self.game.npc_panel == "True":
            for sprite in self.game.farmer_group:
                self.game.all_farmer_layer.remove(sprite)
            self.game.npc_panel = "False"

        if self.game.player.approach_farmer():
            self.game.default_layer.add(self.game.button)
            if self.game.button.is_pressed(self.game.mouse_pos, self.game.mouse_pressed) and self.game.npc_panel == "False":
                for sprite in self.game.farmer_group:
                    self.game.all_farmer_layer.add(sprite)
                self.game.npc_panel = "True"
        else:
            self.game.default_layer.remove(self.game.button)
        
class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, file, group):
        self.game = game
        
        self.type = None
        self.id = None
        self._layer = 2
        self.groups = group
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x 
        self.y = y
        
        self.close_button = Spritesheet(file)
        self.image = self.close_button.get_sprite(0, 0, width, height)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False