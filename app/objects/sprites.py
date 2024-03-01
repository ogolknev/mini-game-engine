'''
Модуль содержит классы описывающие объекты внутри приложения и связанные с ними классы.
'''
import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../..")
from objects.behavior.movement import standartMovement


class Group(pygame.sprite.Group):
    '''
    Станадртный класс `pygame.sprite.Group` с измененным методом `draw` - в нем реализованны `observer` и `scale`.
    '''

    def __init__(self, *sprites) -> None:

        super().__init__(*sprites)


    def _setObserver(self, rect: pygame.Rect, image: pygame.surface.Surface, observer, resolution, scale):

        if observer.rect == rect:

            rect.centerx = resolution[0] // 2
            rect.centery = resolution[1] // 2


        else:

            rect.x *= scale
            rect.y *= scale

            rect.x -= observer.rect.centerx * scale - resolution[0] // 2
            rect.y -= observer.rect.centery * scale - resolution[1] // 2

        return rect.centerx - image.get_width() / 2 * scale, rect.centery - image.get_height() / 2 * scale
    

    def _setScale(self, image, scale):

        size = image.get_size()
        image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))

        return image


    def draw(self, surface, bgsurf=None, special_flags=0, **kwargs):

        observer = kwargs["observer"]
        resolution = kwargs["settings"]["window"]["resolution"]
        scale = kwargs["scale"]

        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(
                        (self._setScale(spr.image, scale), self._setObserver(spr.rect.copy(), spr.image, observer, resolution, scale), None, special_flags) for spr in sprites
                    ),
                )
            )
        else:
            for spr in sprites:
                
                self.spritedict[spr] = surface.blit(
                    self._setScale(spr.image, scale), self._setObserver(spr.rect.copy(), spr.image, observer, resolution, scale), None, special_flags
                )

        self.lostsprites = []
        dirty = self.lostsprites

        return dirty

class Sprite(pygame.sprite.Sprite):

    def __init__(self, texture: pygame.Surface, position: tuple, clock, hitbox: pygame.Rect=None, *groups, **kwargs) -> None:

        super().__init__(*groups)

        self.image = texture
        self.rect = hitbox if hitbox else self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.float_position = list(self.rect.center)

        self._clock = clock
        self._lifetime = 0


    def update(self, *args, **kwargs):
        pass

    # def __eq__(self, other: object) -> bool:
    #     return id(self) == id(other)

class Entity(Sprite):

    def __init__(self, texture: pygame.Surface, position: tuple, clock, controller, hitbox: pygame.Rect=None, *groups, **kwargs) -> None:

        super().__init__(texture, position, clock, hitbox, *groups, **kwargs)

        self.controller = controller

        self.speed = [0,0]
        self.move_block = [0,0]

        self.kwattrs = kwargs

    def update(self, *args, **kwargs):

        self._lifetime += self._clock.get_time()

        standartMovement(self, **kwargs)






        
