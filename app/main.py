import pygame
from __init__ import window, run, sprites, settings, clock, font, SCALE, observer
from key_controls import keyController

# главный цикл
while run:

    clock.tick() # подсчет времени между кадрами

    # обработка событий
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    window.fill((0,0,0)) # цвет основной поверхности

    move_direction = keyController(pygame.key.get_pressed())

    sprites.update(settings=settings,
                   window=window,
                   move_direction=move_direction) # обновление всех спрайтов

    sprites.draw(settings=settings,
                 surface=window,
                 observer=observer) # рендер всех спрайтов


    window.blit(font.render(str(int(clock.get_fps())) + " fps", True, (0,0,0), (200,200,200)), (0, 0))

    pygame.display.flip() # смена кадра

pygame.quit() # завершение программы