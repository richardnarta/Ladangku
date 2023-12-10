import pygame
from item_data import item_id
from timer import Timer

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        return sprite

class PageInventory(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        
        self._layer = 1
        self.groups = self.game.all_inventory_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x 
        self.y = y
        
        self.inventory_page = Spritesheet('assets/inventory/inventory_panel.png')
        self.image = self.inventory_page.get_sprite(0, 0, 464, 314)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.inventory_close_button = InventoryButton(self.game, self.rect.right - 20, self.rect.top - 11,
                                                           35, 35, 'assets/inventory/close_info_button.png', self.game.all_inventory_layer)
        self.game.inventory_group.append(self.inventory_close_button)
        
        padx = 0
        pady = 0
        for j in range (3):
            padx = 0
            for i in range (5):
                self.slot = PageInventorySlots(self.game, self.rect.left + 12 + 64*i + padx, 
                                               self.rect.top + 31 + 64*j + pady)
                self.game.inventory_slot.append(self.slot)
                padx += 20
            pady += 20
        
        i=0
        for item in self.game.inventory:
            if self.game.inventory[item]['amount']!=0 and self.game.inventory[item]['id']!='empty':
                self.game.inventory_slot[i].id = self.game.inventory[item]['id']
                self.game.inventory_slot[i].info_file = self.game.inventory[item][2]
                self.game.inventory_slot[i].item_amount = self.game.inventory[item]['amount']
                i += 1
        
    def edit(self, type, id, amount):
        new_slot = True
        
        for item in self.game.inventory:
            if id == self.game.inventory[item]['id']:
                new_slot = False
                if type == 'add':
                    self.game.inventory[item]['amount'] += amount
                elif type == 'sub' and self.game.inventory[item]['amount'] >= amount:
                    self.game.inventory[item]['amount'] -= amount
                else:
                    print("invalid amount")
                break
        
        if new_slot == True:
            if type == 'add':
                self.game.inventory.update(item_id[id])
                self.game.inventory[id]['amount'] = amount
            else:
                print("anda tidak punya item ini")
                             
        for item in self.game.inventory_slot:
            item.update_slots()
    
    def draw(self):
        if self.game.panel == "True" or self.game.panel == "Paused":
            self.game.all_inventory_layer.draw(self.game.screen)
        
        for text in self.game.inventory_slot:
            text.draw_text(0)
        
        if self.game.panel == "Paused":
            self.game.above_text_layer.draw(self.game.screen)
            for text in self.game.inventory_slot:
                text.draw_text(1)
    
    def update(self):
        if self.inventory_close_button.is_pressed(self.game.mouse_pos, self.game.mouse_pressed) and self.game.panel == "True":
            for sprite in self.game.inventory_group:
                self.game.all_inventory_layer.remove(sprite)
            self.game.panel = "False"
            
        if self.game.inventory_button.is_pressed(self.game.mouse_pos, self.game.mouse_pressed) and self.game.panel == "False":
            for sprite in self.game.inventory_group:
                self.game.all_inventory_layer.add(sprite)
            self.game.panel = "True"

class PageInventorySlots(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.id = 'empty'
        self.game = game
        self.screen = False
        self.timer = Timer(150)
        
        self._layer = 2
        self.groups = self.game.all_inventory_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x + 20
        self.y = y + 20
        
        self.file = self.game.inventory[self.id][1]
        self.empty_slot = Spritesheet(self.game.inventory[self.id][1])
        self.image = self.empty_slot.get_sprite(0, 0, 64, 64)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.temp = None
        self.item_amount = self.game.inventory[self.id]['amount']
        
        self.font = pygame.font.Font('font/arial.ttf', 16)
        self.amount = self.font.render(str(self.game.inventory[self.id]['amount']), False, (0, 0, 0))
        self.amount_rect = self.amount.get_rect()
        
        self.amount_rect.x = self.rect.left + 4
        self.amount_rect.y = self.rect.bottom - 20
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    
    def update(self):
        self.empty_slot = Spritesheet(self.game.inventory[self.id][1])
        self.game.inventory[self.id]['amount'] = self.game.inventory[self.id]['amount']
        self.timer.update()
        
        if self.is_pressed(self.game.mouse_pos, self.game.mouse_pressed) and self.game.inventory[self.id][1] != 'assets/inventory/empty_slot.png' and self.game.panel == "True":
            
            self.item_info = InfoItem(self.game, self, (960-252)/2, (640-282)/2, self.game.inventory[self.id][2])
            self.item_info_closebutton = InventoryButton(self, self.item_info.rect.right - 25, self.item_info.rect.top - 12, 35, 35,
                                                         'assets/inventory/close_info_button.png', self.game.above_text_layer)
            self.item_info_removebutton = InventoryButton(self, self.item_info.rect.right - 153, self.item_info.rect.top + 83, 126, 18,
                                                      'assets/inventory/remove_item_button.png', self.game.above_text_layer)
            self.item_addbutton = InventoryButton(self, self.item_info.rect.right - 55, self.item_info.rect.top + 50, 28, 28,
                                                  'assets/inventory/add_item.png', self.game.above_text_layer)
            self.item_subbutton = InventoryButton(self, self.item_info.rect.right - 153, self.item_info.rect.top + 50,  28, 28,
                                                  'assets/inventory/sub_item.png', self.game.above_text_layer)
            self.timer.activate()
            self.screen = True
            self.image = self.empty_slot.get_sprite(64, 0, 70, 70)
            
            self.rect.x = self.x-3
            self.rect.y = self.y-3
            
            self.game.panel = "Paused"
            self.temp = self.game.inventory[self.id]['amount']
            
        elif self.game.panel != "Paused":
            self.image = self.empty_slot.get_sprite(0, 0, 64, 64)
            
            self.rect.x = self.x
            self.rect.y = self.y
        
        if self.screen == True:
            if not self.timer.active:
                if self.item_subbutton.is_pressed(self.game.mouse_pos, self.game.mouse_pressed):
                    if self.item_amount > 0:
                        self.item_amount -= 1
                        self.timer.activate()
                    else:
                        self.game.inventory[self.id]['amount'] = 0
                    self.timer.activate()
                elif self.item_addbutton.is_pressed(self.game.mouse_pos, self.game.mouse_pressed):
                    if self.item_amount < self.temp:
                        self.item_amount += 1
                        self.timer.activate()
                    else:
                        self.game.inventory[self.id]['amount'] = self.temp    
                    
                if self.item_info_removebutton.is_pressed(self.game.mouse_pos, self.game.mouse_pressed):
                    self.temp = self.item_amount
                    self.game.inventory[self.id]['amount'] = self.temp
                    self.timer.activate()
            
                if self.item_info_closebutton.is_pressed(self.game.mouse_pos, self.game.mouse_pressed):
                    self.item_amount = self.temp
                    self.game.panel = "True"
                    self.screen = False
                    for sprite in self.game.above_text_layer:
                        self.game.above_text_layer.remove(sprite)
                    self.timer.activate()
                    self.update_slots()
                
        if self.game.panel == "True" and self.game.inventory[self.id][1] != 'assets/inventory/empty_slot.png':
            self.amount = self.font.render(str(self.item_amount), False, (0, 0, 0))
            self.game.screen.blit(self.amount, self.amount_rect)
            
    def update_slots(self):
        if self.game.inventory[self.id]['amount'] == 0 and self.id != 'empty':
            del(self.game.inventory[self.id])
            self.id = 'empty'
            
        for i in self.game.inventory_slot:
            i.id = 'empty'
        
        
        i=0
        for item in self.game.inventory:
            if self.game.inventory[item]['id']!='empty':
                self.game.inventory_slot[i].id = self.game.inventory[item]['id']
                self.game.inventory_slot[i].info_file = self.game.inventory[item][2]
                self.game.inventory_slot[i].item_amount = self.game.inventory[item]['amount']
                i += 1
    
    def draw_text(self, code):
        if (self.game.panel == "True" or self.game.panel == "Paused") and self.game.inventory[self.id][1] != 'assets/inventory/empty_slot.png' and code == 0:
            self.game.screen.blit(self.amount, self.amount_rect)
            
        elif self.screen == True and code == 1:
            self.game.screen.blit(self.item_info.amount_remove, self.item_info.amount_remove_rect)
            
class InfoItem(pygame.sprite.Sprite):
    def __init__(self, game, inventory, x, y, file):
        self.game = game
        self.inventory = inventory
        
        self._layer = 1
        self.groups = self.game.above_text_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.file = file
        
        self.x = x 
        self.y = y
        
        self.inventory_page = Spritesheet(self.file)
        self.image = self.inventory_page.get_sprite(0, 0, 252, 282)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y

        self.font = pygame.font.Font('font/courier.ttf', 20)
    
    def update(self):
        self.amount_remove = self.font.render(str(self.inventory.item_amount), True, (0, 0, 0))
        self.amount_remove_rect = self.amount_remove.get_rect()
        
        self.amount_remove_rect.centerx = 516
        self.amount_remove_rect.centery = 243
        self.game.screen.blit(self.amount_remove, self.amount_remove_rect)
            
class InventoryButton(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, file, group):
        self.game = game
        
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