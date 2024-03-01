'''
Основной исполняемый файл.
'''
import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../..")
from app import window, run, sprites, settings, clock, font, scale, scale_timer, observer, appKeyController

# главный цикл
while run:

    clock.tick(60) # подсчет времени между кадрами

    # обработка событий
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    window.fill((0,0,0)) # цвет основной поверхности

    pressed_keys = pygame.key.get_pressed()

    settings, scale, scale_timer = appKeyController(settings=settings,
                                                    pressed_keys=pressed_keys,
                                                    scale=scale,
                                                    scale_timer=scale_timer,
                                                    tick_time=clock.get_time())

    sprites.update(settings=settings,
                   window=window,
                   pressed_keys=pressed_keys) # обновление всех спрайтов

    sprites.draw(settings=settings,
                 surface=window,
                 observer=observer,
                 scale=scale) # рендер всех спрайтов


    window.blit(font.render(str(int(clock.get_fps())) + " fps", True, (0,0,0), (200,200,200)), (0, 0))

    pygame.display.flip() # смена кадра

pygame.quit() # завершение программы