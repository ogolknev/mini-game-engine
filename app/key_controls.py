import pygame
from __init__ import settings


def keyController(pressed_keys: pygame.key.ScancodeWrapper):
    '''
    Параметры:

    - key_controls - словарь с текущими настройками управления
    - pressed_keys - список состаяния всех кнопок
    
    Возвращает направление в котором должен двигаться управляемый объект
    '''

    key_controls = settings["key_controls"]

    move_direction = [0,0]
    change_resolution = None

    if pressed_keys[key_controls["move_up"]]:
        move_direction[1] -= 1
    if pressed_keys[key_controls["move_left"]]:
        move_direction[0] -= 1
    if pressed_keys[key_controls["move_down"]]:
        move_direction[1] += 1
    if pressed_keys[key_controls["move_right"]]:
        move_direction[0] += 1

    if pressed_keys[key_controls["fullscreen"]]:
        pygame.display.toggle_fullscreen()
        settings["window"]["resolution"] = list(pygame.display.get_window_size())

    return move_direction