import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../../..")
from tools.math_tools import sign, blockFilter

def standartMovement(sprite: pygame.sprite.Sprite, **kwargs):

    '''
    Реализует перемещение данного объекта

    Парметры
    - sprite - Объект для которого реализуется перемещение
    - maxacceleration - Ускорение/замедление
    '''

    maxacceleration = sprite.kwattrs["maxacceleration"]
    maxspeed = sprite.kwattrs["maxspeed"]
    move_direction = sprite.controller(**(kwargs | {"sprite": sprite}))

    # if "func" in sprite.kwattrs:
    #     print(move_direction)

    time = sprite._clock.get_time() * 0.001

    acceleration = [maxacceleration * move_direction[0],
                    maxacceleration * move_direction[1]]
    
    
    sprite.speed[0] += acceleration[0] * 2 * time
    sprite.speed[1] += acceleration[1] * 2 * time

    sprite.speed[0] -= maxacceleration * sign(sprite.speed[0]) * time
    sprite.speed[1] -= maxacceleration * sign(sprite.speed[1]) * time


    if (sprite.speed[0]**2 + sprite.speed[1]**2)**(1/2) > maxspeed:
        sprite.speed[0] = move_direction[0] * maxspeed if not acceleration[1] else move_direction[0] * maxspeed / 2
        sprite.speed[1] = move_direction[1] * maxspeed if not acceleration[0] else move_direction[1] * maxspeed / 2


    sprite.move_block = [0,0]

    pathInterpole(sprite, sprite.speed[0] * time, sprite.speed[1] * time)

def pathInterpole(sprite: pygame.sprite.Sprite, pathx, pathy):

    steps_num = int(max(abs(pathx), abs(pathy))) + 1
    stepx = pathx / steps_num
    stepy = pathy / steps_num

    group = sprite.groups()[0]
    sprite.remove(group)

    for _ in range(steps_num):

        collisions = pygame.sprite.spritecollide(sprite, group, False)

        if collisions:
            collideHandle(sprite, collisions)

        stepx = blockFilter(stepx, sprite.move_block[0])
        stepy = blockFilter(stepy, sprite.move_block[1])

        if stepx or stepy:

            sprite.float_position[0] += stepx
            sprite.float_position[1] += stepy

            sprite.rect.centerx = int(sprite.float_position[0])
            sprite.rect.centery = int(sprite.float_position[1])

        else:
            break

    
    sprite.add(group)

def collideHandle(sprite: pygame.sprite.Sprite, collisions):

    for collided in collisions:

        diffx = (sprite.rect.centerx - collided.rect.centerx) / (sprite.rect.width + collided.rect.width)
        diffy = (sprite.rect.centery - collided.rect.centery) / (sprite.rect.height + collided.rect.height)

        if abs(diffx) > abs(diffy):
            if diffx < 0: 
                sprite.move_block[0] += 2
            else:
                sprite.move_block[0] += 1
        elif abs(diffy) > abs(diffx):
            if diffy < 0: 
                sprite.move_block[1] += 2
            else:
                sprite.move_block[1] += 1
        else:
            if diffx > 0:
                sprite.move_block[0] += 1
                if diffy > 0:
                    sprite.move_block[1] += 1
                else:
                    sprite.move_block[1] += 2
            else:
                sprite.move_block[0] += 2
                if diffy > 0:
                    sprite.move_block[1] += 1
                else:
                    sprite.move_block[1] += 2
