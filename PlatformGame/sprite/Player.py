import pygame, logging, os
from pygame.locals import (
    RLEACCEL,
)

WHITE = (255,255,255)
BLACK = (0,0,0)

log = logging.getLogger(__name__)


class Player(pygame.sprite.Sprite):

    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    fall = pygame.image.load(os.path.join('images', '0.png'))

    def __init__(self, x, y):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.original_y = y
        self._init_slide_list()
        self.jumping = False
        self.jump_index = -1
        self.jumpCount = 0
        # Force (v) up and mass m.
        self.v = 11
        self.m = 1
        self.sliding = False
        self.slide_index = -1
        self.falling = False
        self.run_index = -1
        self.do_run()

    def _init_slide_list(self):
        self.slide = [pygame.image.load(os.path.join('images', 'S1.png'))]
        s2 = pygame.image.load(os.path.join('images', 'S2.png'))
        for i in range(0, 30):
            self.slide.append(s2)
        for i in range(3, 6):
            self.slide.append(pygame.image.load(os.path.join("images", "S{}.png".format(i))))

    def update(self):
        if self.falling:
            self.do_fall()
        elif self.jumping:
            self.do_jump()
        elif self.sliding:
            self.do_slide()
        else:
            self.do_run()

    def do_run(self):
        log.debug("do_run")
        self.image = self.run[self._get_next_run_index()].convert()
        self.handle_new_image()
        self.rect.y = self.original_y

    def do_fall(self):
        log.debug("do_fall")
        self.image = self.fall.convert()
        self.handle_new_image()
        self.rect.y = self.original_y + 30

    def do_jump(self):
        log.debug("do_jump: y={}".format(self.y))
        self.image = self.jump[self._get_next_jump_index()].convert()
        self.handle_new_image()

        # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
        F = (1 / 2) * self.m * (self.v ** 2)
        # change in the y co-ordinate
        self.y -= F
        self.rect.y = self.y
        # decreasing velocity while going up and become negative while coming down
        self.v -= 1
        # object reached its maximum height
        if self.v < 0:
            # negative sign is added to counter negative velocity
            self.m = -1
        # objected reaches its original state
        if self.v <= -10: # or self.rect.y > self.y:
            self.jumping = False
            # setting original values to v and m
            self.v = 11
            self.m = 1
            self.y = self.original_y
            self.do_run()

    def do_slide(self):
        log.debug("do_slide")
        index = self._get_next_slide_index()
        if index == 0:
            self.y += 21
        elif index >= len(self.slide) -1:
            self.y -= 21
            self.sliding = False
        self.image = self.slide[index].convert()
        self.handle_new_image()

    def handle_new_image(self):
        self.image.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def _get_next_run_index(self):
        self.run_index = Player._get_next_index(self.run_index, self.run)
        return self.run_index

    def _get_next_jump_index(self):
        self.jump_index = Player._get_next_index(self.jump_index, self.jump)
        return self.jump_index

    def _get_next_slide_index(self):
        self.slide_index = Player._get_next_index(self.slide_index, self.slide)
        return self.slide_index

    @staticmethod
    def _get_next_index(index, list):
        index += 1
        if index >= len(list):
            index = 0
        return index
