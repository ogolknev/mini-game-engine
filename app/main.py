'''
Основной исполняемый файл.
'''
import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../..")
from init import (window, run, entities, moving_entities, settings, clock,
                 fps, font, scale, observer, appKeyController)

# главный цикл
while run:

    clock.tick(fps) # подсчет времени между кадрами и применение задержки для ограничения fps

    # обработка событий
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    window.fill((0,0,0)) # заливка основной поверхности (окна) цветом

    pressed_keys = pygame.key.get_pressed() # получение зажатых клавиш

    settings, run, scale = appKeyController(pressed_keys=pressed_keys,
                                            settings=settings,
                                            run=run,
                                            scale=scale,
                                            clock=clock,
                                            ) # управление настройками с помощью кнопок

    entities.update(moving_entities=moving_entities,
                    settings=settings,
                    pressed_keys=pressed_keys) # обновление всех спрайтов

    entities.draw(surface=window,
                  resolution=settings["window"]["resolution"],
                  observer=observer,
                  scale=scale
                  ) # рендер всех спрайтов
    

    window.blit(font.render(str(int(clock.get_fps())) + " fps", True, (0,0,0), (200,200,200)), (0, 0)) # отображение debug панели

    pygame.display.flip() # смена кадра

pygame.quit() # завершение программы