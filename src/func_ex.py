from csv import reader
import pygame
from setting import *

def import_csv(path):
    ground_map = []
    with open(path) as map:
        ground = reader(map, delimiter=',')
        for row in ground:
            ground_map.append(list(row))
        return ground_map
    
def cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_x = int(surface.get_size()[0] / TILESIZE)
    tile_y = int(surface.get_size()[1] / TILESIZE)

    tiles = []
    for row in range(tile_y):
        for column in range(tile_x):
            x = column *TILESIZE
            y = row * TILESIZE
            new_surf = pygame.Surface((TILESIZE,TILESIZE))
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,TILESIZE,TILESIZE))
            new_surf.set_colorkey((0,0,0))
            tiles.append(new_surf)
    
    return tiles

def get_animation_player(path, width, height):
    surface = pygame.image.load(path).convert_alpha()
    tile_x = int(surface.get_size()[0]/ width)
    tile_y = int(surface.get_size()[1]/ height)

    animation = []
    for row in range (tile_y):
        temp = []
        for col in range (tile_x):
            x = col * width
            y = row * height
            new_surf = pygame.Surface((width,height))
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,width,height))
            new_surf.set_colorkey((0,0,0))
            temp.append(new_surf)
        animation.append(temp)

    return animation


