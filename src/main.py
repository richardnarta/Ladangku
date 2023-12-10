import pygame, sys, time
from setting import *
from game import Game
from game_data import game_data
from debug import debug

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
clock = pygame.time.Clock()
gamerun = Game(game_data,screen)
running = True

prev_time = time.time()
while running:
    dt = time.time()-prev_time
    prev_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('inventory_data.txt', 'w') as file:
                file.writelines(str(gamerun.inventory))
                file.writelines(f'\n{str(gamerun.player.gold_stat.get_amount())}')
                file.close()
            running = False
        if event.type == pygame.MOUSEWHEEL and (gamerun.panel == "False" and gamerun.npc_panel == "False"):
            if gamerun.all_sprite.zoom_scale + event.y * 0.09 >= 1.15 and gamerun.all_sprite.zoom_scale + event.y * 0.09<= 2.5:
                gamerun.all_sprite.zoom_scale+= event.y * 0.09
                
    gamerun.dt = dt
    gamerun.run()
    # debug(clock)
    # debug(dt, y=40)
    clock.tick(FPS)
    pygame.display.update()