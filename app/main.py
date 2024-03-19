'''
Основной исполняемый файл.
'''
import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../..")
from app import (window, run, entities, moving_entities, settings, clock,
                 fps, font, scale, observer, main_surface, appKeyController)

# главный цикл
while run:

    clock.tick(fps) # подсчет времени между кадрами и применение задержки для ограничения fps

    # обработка событий
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    window.fill((0,0,0)) # цвет основной поверхности
    # main_surface.sprite.image.fill((100,100,100))

    pressed_keys = pygame.key.get_pressed() # получение зажатых клавиш

    settings, scale, run = appKeyController(settings=settings,
                                            pressed_keys=pressed_keys,
                                            scale=scale,
                                            clock=clock,
                                            run = run) # управление настройками с помощью кнопок

    entities.update(settings=settings,
                    pressed_keys=pressed_keys,
                    moving_entities=moving_entities) # обновление всех спрайтов

    entities.draw(surface=window,
                  resolution=settings["window"]["resolution"],
                  observer=observer,
                  scale=scale
                  ) # рендер всех спрайтов
    

    # window.blit(main_surface, (0,0))
    window.blit(font.render(str(int(clock.get_fps())) + " fps", True, (0,0,0), (200,200,200)), (0, 0)) # отображение debug панели

    pygame.display.flip() # смена кадра

pygame.quit() # завершение программы