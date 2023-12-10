import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y,layer):
        super().__init__()
        self._layer = layer
        self.image = pygame.Surface((size,size),pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.image.set_colorkey('Black')

    def update(self):
        pass

class StaticTile(Tile):
    def __init__(self,size,x,y,surf,layer):
        super().__init__(size,x,y,layer)
        self.image = surf.convert(pygame.display.get_surface())
        self.rect = self.image.get_rect(topleft=(x,y))

class AnimatedTile(Tile):
    def __init__(self,size,x,y,surf,layer):
        super().__init__(size,x,y,layer)
        self.animation = surf
        self.currentframe = 0
        self.image = self.animation[self.currentframe]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.lastupdate = pygame.time.get_ticks()
        self.animationcd = 75

    def animate(self):
        currenttime = pygame.time.get_ticks()
        if currenttime - self.lastupdate >= self.animationcd:
            self.currentframe+=1
            if self.currentframe>=len(self.animation):
                self.currentframe = 0
            self.lastupdate = currenttime
            self.image = self.animation[self.currentframe]

    def update(self):
        self.animate()

