'''
Модуль описывающий контроллеры - функции управляющие другими объектами.
'''
import pygame
from random import randint
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../../../..")


def appKeyController(pressed_keys: pygame.key.ScancodeWrapper,
                     settings: dict,
                     run: bool,
                     scale: float,
                     clock: pygame.time.Clock):
    '''
    Контроллер управляющий основными настройками приложения с помощью клавиатуры.

    Принимает:
    - `pressed_keys` - объект pygame (pygame.key.ScancodeWrapper), содержащий состояние всех клавиш
    - `settings` - словарь содержащий настройки приложения
    - `run` - переключатель отвечающий за работу приложения
    - `scale` - коэффициент приближения камеры
    - `clock` - объект pygame для отслеживания времени

    Возвращает:
    - `settings` - обработанный словарь содержащий настройки приложения
    - `run` - обработанный переключатель отвечающий за работу приложения
    - `scale` - обработанный коэффициент приближения камеры
    '''
    key_controls = settings["key_controls"]
    

    if pressed_keys[key_controls["fullscreen"]]:
        pygame.display.toggle_fullscreen()
        settings["window"]["resolution"] = list(pygame.display.get_window_size())

    if pressed_keys[key_controls["exit"]]:
        run = False and run

    if pressed_keys[key_controls["scale_up"]]:
        scale += 2 * 0.001 * clock.get_time()
        if scale > 5: scale = 5.0
    if pressed_keys[key_controls["scale_down"]]:
        scale -= 2 * 0.001 * clock.get_time()
        if scale < 0.2: scale = 0.2


    return settings, run, scale


def gameKeyController(**kwargs):
    '''
    Контроллер управляющий движением сущностей внутри приложения с помощью клавиатуры.
    Определяет направление движения сущности, в соответсвии нажатым клавишам.

    Принимает:
    - `kwargs` - кей-ворд параметры:
        - `settings` - словарь содержащий настройки приложения
        - `pressed_keys` - объект pygame (pygame.key.ScancodeWrapper), содержащий состояние всех клавиш

    Возвращает:
    - `move_direction` - список из двух направлений [по горизонтали, по вертикали]
    (`1` - в сторону увеличения координаты, `-1` - наоборот, 0 - нет движения)
    '''

    settings = kwargs["settings"]
    pressed_keys = kwargs["pressed_keys"]
    key_controls = settings["key_controls"]
    move_direction = [0,0]

    if pressed_keys[key_controls["move_up"]]:
        move_direction[1] -= 1
    if pressed_keys[key_controls["move_left"]]:
        move_direction[0] -= 1
    if pressed_keys[key_controls["move_down"]]:
        move_direction[1] += 1
    if pressed_keys[key_controls["move_right"]]:
        move_direction[0] += 1

    return move_direction


def gameRandController(**kwargs):
    '''
    Контроллер управляющий движением сущностей внутри приложения.
    Случайно определяет направление движения сущности.

    Принимает:
    - `kwargs` - кей-ворд параметры:
        - `sprite` - сущность для которой определяется направление движения

    Возвращает:
    - `move_direction` - список из двух направлений [по горизонтали, по вертикали]
    (`1` - в сторону увеличения координаты, `-1` - наоборот, 0 - нет движения)
    '''

    sprite = kwargs["sprite"]

    if "rand_move_timer" in sprite.kwattrs:
        sprite.kwattrs["rand_move_timer"] += sprite._clock.get_time()
        if sprite.kwattrs["rand_move_timer"] > randint(200, 3000):
            sprite.kwattrs["direction"] = [randint(-1, 1), randint(-1, 1)]
            sprite.kwattrs["rand_move_timer"] = 0
        else:
            return sprite.kwattrs["direction"]
    else:
        sprite.kwattrs.update({"rand_move_timer": 0})
        sprite.kwattrs.update({"direction": [0,0]})

    return sprite.kwattrs["direction"]

