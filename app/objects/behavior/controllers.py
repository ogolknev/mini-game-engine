import pygame
from random import randint
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../../../..")


def appKeyController(pressed_keys: pygame.key.ScancodeWrapper, **kwargs):
    '''
    '''
    settings = kwargs["settings"]
    key_controls = settings["key_controls"]
    scale = kwargs["scale"]
    scale_timer = kwargs["scale_timer"]
    scale_timer += kwargs["tick_time"]

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

    return settings, scale, scale_timer


def gameKeyController(**kwargs):

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

    sprite = kwargs["sprite"]

    if "rand_move_timer" in sprite.kwattrs:
        sprite.kwattrs["rand_move_timer"] += sprite._clock.get_time()
        if sprite.kwattrs["rand_move_timer"] > randint(200, 3000):
            print("direction changed")
            sprite.kwattrs["direction"] = [randint(-1, 1), randint(-1, 1)]
            sprite.kwattrs["rand_move_timer"] = 0
        else:
            return sprite.kwattrs["direction"]
    else:
        sprite.kwattrs.update({"rand_move_timer": 0})
        sprite.kwattrs.update({"direction": [0,0]})

    return sprite.kwattrs["direction"]
