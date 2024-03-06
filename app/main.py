'''
Основной исполняемый файл.
'''
import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../..")
from app import (window, run, entities, moving_entities, settings, clock,
                 fps, font, scale, observer, appKeyController)

# главный цикл
while run:

    clock.tick(fps) # подсчет времени между кадрами

    # обработка событий
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    window.fill((0,0,0)) # цвет основной поверхности

    pressed_keys = pygame.key.get_pressed()

    settings, scale, run = appKeyController(settings=settings,
                                            pressed_keys=pressed_keys,
                                            scale=scale,
                                            scale_clock=clock)

    entities.update(settings=settings,
                   window=window,
                   pressed_keys=pressed_keys,
                   moving_entities=moving_entities) # обновление всех спрайтов

    entities.draw(settings=settings,
                 surface=window,
                 observer=observer,
                 scale=scale) # рендер всех спрайтов


    window.blit(font.render(str(int(clock.get_fps())) + " fps", True, (0,0,0), (200,200,200)), (200, 200))

    pygame.display.flip() # смена кадра

pygame.quit() # завершение программы