import pygame, logging, os
from pygame.locals import (
    RLEACCEL,
)

BLACK = (0,0,0)


class Spike(pygame.sprite.Sprite):

    def __init__(self, x, y, speed):
        super(Spike, self).__init__()
        self.image = pygame.image.load(os.path.join('images', 'spike.png'))
        self.image.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        logging.debug("update: speed = {}".format(self.speed))
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
