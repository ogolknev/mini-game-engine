import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../../../..")
from app import settings


def keyController(pressed_keys: pygame.key.ScancodeWrapper, **kwargs):
    '''
    Параметры:

    - key_controls - словарь с текущими настройками управления
    - pressed_keys - список состаяния всех кнопок
    
    Возвращает направление в котором должен двигаться управляемый объект
    '''

    key_controls = settings["key_controls"]

    move_direction = [0,0]
    scale = kwargs["scale"]
    scale_timer = kwargs["scale_timer"]
    scale_timer += kwargs["tick_time"]

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

    if pressed_keys[key_controls["scale_up"]]:
        if scale < 2 and scale_timer > 30:
            scale += 0.02
            scale_timer = 0
    if pressed_keys[key_controls["scale_down"]]:
        if scale > 0.2 and scale_timer > 30: 
            scale -= 0.02
            scale_timer = 0

    return move_direction, scale, scale_timer