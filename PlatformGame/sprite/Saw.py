import pygame, logging, os
from pygame.locals import (
    RLEACCEL,
)

BLACK = (0,0,0)


class Saw(pygame.sprite.Sprite):

    rotate = [pygame.image.load(os.path.join('images', 'SAW0.png')),
              pygame.image.load(os.path.join('images', 'SAW1.png')),
              pygame.image.load(os.path.join('images', 'SAW2.png')),
              pygame.image.load(os.path.join('images', 'SAW3.png'))]

    def __init__(self, x, y, speed):
        super(Saw, self).__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.rotate_index = -1
        self.do_rotate()

    def update(self):
        #self.do_rotate()
        logging.debug("update")
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def do_rotate(self):
        logging.debug("do_rotate")
        self.image = self.rotate[self._get_next_rotate_index()].convert()
        self._handle_new_image()

    def _get_next_rotate_index(self):
        self.rotate_index += 1
        if self.rotate_index >= len(self.rotate):
            self.rotate_index = 0
        logging.debug("rotate_index: {}".format(self.rotate_index))
        return self.rotate_index

    def _handle_new_image(self):
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
