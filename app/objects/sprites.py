'''
Модуль содержит классы описывающие объекты внутри приложения и связанные с ними классы.
'''
from typing import List
import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../..")
from objects.behavior.movement import standartMovement
from tools.math_tools import nextIterible, rectInArea

class Group(pygame.sprite.Group):
    '''
    Станадртный класс `pygame.sprite.Group` с измененными методами:
    - `draw` - в нем реализованны функции `observer` (закрепление камеры за объектом) и `scale` (приближение и отдаление камеры)
    - `update` - в нем реализованна функция передвижения объектов внутри группы

    Атрибуты:
    - стандартные атрибуты `pygame.sprite.Group`
    '''

    def __init__(self, *sprites) -> None:
        '''
        Станадртный класс `pygame.sprite.Group` с измененными методами:
        - `draw` - в нем реализованны функции `observer` (закрепление камеры за объектом) и `scale` (приближение и отдаление камеры)
        - `update` - в нем реализованна функция передвижения объектов внутри группы

        Параметры:
        - стандартные параметры `pygame.sprite.Group` (опциональны)
        '''

        super().__init__(*sprites)


    def draw(self, surface: pygame.surface.Surface, resolution, observer, scale):
        '''
        Отрисовывает объекты группы на переданной поверхности, в пределах области отрисовки (102% разрешения окна)

        Параметры:
        - `surface` - поверхность на которой происходит отрисовка
        - `resolution` - разрешение главного окна
        - `observer` - объект за которым закреплена камера
        - `scale` - коэффициент приближения камеры
        '''

        rendering_area_rect = pygame.Rect(0,0, resolution[0] / (scale * 0.98), resolution[1] / (scale * 0.98))
        rendering_area_rect.center = observer.rect.centerx, observer.rect.centery

        for sprite in self.sprites():

            if sprite.rect.colliderect(rendering_area_rect):

                rect, offset = rectInArea(sprite.rect.copy(), rendering_area_rect)
                image = pygame.transform.scale_by(sprite.image.subsurface((*offset, rect.width + sprite.hitbox_position[0] * 2, rect.height + sprite.hitbox_position[1] * 2)), scale)

                rect.width *= scale
                rect.height *= scale

                rect.x = (rect.x - observer.rect.centerx) * scale + resolution[0] // 2
                rect.y = (rect.y - observer.rect.centery) * scale + resolution[1] // 2

                surface.blit(image, (rect.x - (sprite.hitbox_position[0] * scale), rect.y - (sprite.hitbox_position[1] * scale)))
    
    

    def update(self, moving_entities: pygame.sprite.Group, *args, **kwargs):
        '''
        Обновляет свойства объектов между кадрами в соответсвии с описанным поведением
        в методе `update()` элементов группы и функцией движения.

        Параметры:
        - параметры необходимые методам `update()` объектов группы и функции движения
        '''

        standartMovement(self, moving_entities, *args, **kwargs)

        return super().update(*args, **kwargs)


class Sprite(pygame.sprite.Sprite):
    '''
    Класс описывающий все объекты в главном окне. 

    Атрибуты:
    - `image` - текстура объекта отображаемая на экране
    - `spritesheet` - словарь содержащий все кадры анимации объекта
    - `_animation_frame_index` - индекс кадра анимации
    - `rect` - хитбокс объекта
    - `hitbox_position` - положение хитбокса внутри текстуры объекта
    - `float_position` - позиция объекта на экране не привязанная к сетке пикселей
    - `_clock` - экземпляр класса `pygame.time.Clock` позволяющий импользовать в методах
    время которое прошло с последнего кадра
    '''

    def __init__(self,
                 position: tuple,
                 clock,
                 hitbox: pygame.Rect=None,
                 spritesheet: dict=None,
                 texture: pygame.Surface=None,
                 *groups,
                 **kwargs):
        '''
        Класс описывающий все объекты в главном окне. 

        Параметры:
        - `position` - позиция объекта относительно начала координат
        - `clock` - экземпляр класса `pygame.time.Clock` для работы с временем
        - `hitbox` - экземпляр класса `pygame.Rect` его положение - это положение хитбокса внутри текстуры,
        его размер - размер хитбокса
        - `spritesheet` - словарь содержащий все кадры анимации объекта
        - `texture` - текстура для неанимированных объектов
        - `groups` - группы которым принадлежит объект
        - `kwargs` - key-word параметры которые используются методами класса и групп которым принадлежит объект
        '''

        super().__init__(*groups)

        self.image = spritesheet["default"] if spritesheet else texture
        self.spritesheet = spritesheet
        self._animation_frame_index = -1

        self.rect = hitbox if hitbox else self.image.get_rect()
        self.hitbox_position = self.rect.x, self.rect.y
        self.rect.x, self.rect.y = position
        self.float_position = list(self.rect.center)

        self._clock = clock
        self._lifetime = 0

    def update(self, *args, **kwargs):
        '''
        Обновляет свойства объекта между кадрами.
        '''


class Entity(Sprite):
    '''
    Класс описывающий объекты внутри игры.

    Атрибуты:
    - `image` - текстура объекта отображаемая на экране
    - `spritesheet` - словарь содержащий все кадры анимации объекта
    - `_animation_frame_index` - индекс кадра анимации
    - `rect` - хитбокс объекта
    - `hitbox_position` - положение хитбокса внутри текстуры объекта
    - `float_position` - позиция объекта на экране не привязанная к сетке пикселей
    - `_clock` - экземпляр класса `pygame.time.Clock` позволяющий импользовать в методах
    время которое прошло с последнего кадра
    - `controller` - функция определяющая направление движения объекта
    - `speed` - текущая скорость объекта в виде списка из двух значений: скрость по горизонтали и скрость по вертикали
    - `path` - путь объекта за текущий кадр в виде списка из двух значений: путь по горизонтали и путь по вертикали
    - `move_block` - блокировки направлений движения объекта в виде списка из двух значений:
    блокировки по горизонтали и блокировки по вертикали 
    - `kwattrs` - key-word атрибуты которые используются методами класса и группами которым принадлежит объект
    '''

    def __init__(self, 
                 position: tuple, 
                 clock, 
                 controller, 
                 hitbox: pygame.Rect=None, 
                 spritesheet: dict=None,
                 texture: pygame.Surface=None, 
                 *groups, 
                 **kwargs) -> None:
        '''
        Класс описывающий объекты внутри игры.

        Параметры:
        - `position` - позиция объекта относительно начала координат
        - `clock` - экземпляр класса `pygame.time.Clock` для работы с временем
        - `controller` - функция определяющая направление движения объекта
        - `hitbox` - экземпляр класса `pygame.Rect` его положение - это положение хитбокса внутри текстуры,
        его размер - размер хитбокса
        - `spritesheet` - словарь содержащий все кадры анимации объекта
        - `texture` - текстура для неанимированных объектов
        - `groups` - группы которым принадлежит объект
        - `kwargs` - key-word параметры которые используются методами класса и группами которым принадлежит объект
        '''

        super().__init__(position, clock, hitbox, spritesheet, texture, *groups, **kwargs)

        self.controller = controller

        self.speed = [0,0]
        self.path = [0,0]
        self.move_block = [0,0]

        self.kwattrs = kwargs

    def update(self, *args, **kwargs):
        '''
        Обновляет свойства объекта между кадрами.
        '''

    def animation(self, speed, mode=None, *args):

        '''
        Сменяет кадры в анимации сущности.

        Параметры:
        - `mode` - название типа анимации в `self.spritesheet`
        - `args` - ключи по которым определяется конкретный набор кадров в `self.spritesheet`
        - `speed` - скорость (кадры/секунду) анимации
        '''

        if mode:
            self.image = self.spritesheet[mode]
            for arg in args:
                self.image = self.image[arg]
        else:
            self.image = self.spritesheet["default"]
            
        self.image, self._animation_frame_index = nextIterible(self.image, self._animation_frame_index, self._clock.get_time(), speed)
        


        
        
