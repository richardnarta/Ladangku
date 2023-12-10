import pygame
from npc import Button
from inventory import Spritesheet
from func_ex import get_animation_player
from game_data import game_asset
from setting import *

class GoldStatistic(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = 2
        self.groups = self.game.default_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.__amount = 1000
        
        self.x = x 
        self.y = y
        
        self.gold_stat = Spritesheet('assets/stats/gold_stat.png')
        self.image = self.gold_stat.get_sprite(0, 0, 222, 51)
        self.rect = self.image.get_rect()
        
        self.rect.right = self.x
        self.rect.top = self.y
        
        self.font = pygame.font.Font('font/courier.ttf', 24, bold = True)
        
    def set_amount(self, new_amount):
        self.__amount = new_amount
        
    def get_amount(self):
        return self.__amount
        
    def update(self):
        self.gold_amount = self.font.render(str(self.__amount), True, (247, 132, 0))
        self.gold_amount_rect = self.gold_amount.get_rect(right = self.x - 20, top = self.y + 13)
        
        self.game.screen.blit(self.gold_amount, self.gold_amount_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self,game,group,group2,dt):
        self.game = game
        super().__init__(group)
        self.groups = group
        self._layer = player
        self.animation = get_animation_player(game_asset['player'], PLAYER_ANIMATION_WIDTH, PLAYER_ANIMATION_HEIGHT)
        self.current_act = 0
        self.current_frame = 0
        self.image = self.animation[self.current_act][self.current_frame]
        self.rect = self.image.get_rect(center = (600,600))
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2()
        self.animationcd = 75
        self.lastupdate = pygame.time.get_ticks()
        self.moving = False
        self.temp = group2
        self.deltatime = dt
        
        self.x_change = 0
        self.y_change = 0
        
        self.gold_stat = GoldStatistic(self.game, WIN_WIDTH-24, 26)

    def move(self):
        key = pygame.key.get_pressed()    
        if key[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.current_act = 1   
            self.moving = True
        if key[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.current_act = 0   
            self.moving = True 
        if key[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.current_act = 2
            self.moving = True
        if key[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.current_act = 3
            self.moving = True
        
    def animate(self):
        currenttime = pygame.time.get_ticks()
        if self.moving:
            if currenttime-self.lastupdate>= self.animationcd:
                self.current_frame+=1
                if self.current_frame>= len(self.animation):
                    self.current_frame = 0
                self.lastupdate = currenttime
        else:
            self.current_frame = 0
        self.image = self.animation[self.current_act][self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.moving = False

    def collide(self, group, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, group, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                        
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
            
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, group, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                        
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    
    def approach_farmer(self):
        if self.rect.top - self.game.farmer.rect.bottom < 10:
            if self.rect.left - self.game.farmer.rect.right < 10:
                if self.game.farmer.rect.top - self.rect.bottom < 10:
                    if self.game.farmer.rect.left - self.rect.right < 10:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
                
    def update(self):
        self.move()
        
        self.rect.x += self.x_change * self.deltatime * FPS
        self.collide(self.temp, 'x')
        self.rect.y += self.y_change * self.deltatime * FPS
        self.collide(self.temp, 'y')
        
        self.animate()
        
        self.x_change = 0
        self.y_change = 0