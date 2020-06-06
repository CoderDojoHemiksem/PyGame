import pygame, logging, os, random
from PlatformGame.sprite.Player import Player
from PlatformGame.sprite.Saw import Saw
from PlatformGame.sprite.Spike import Spike
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    USEREVENT,
    QUIT,
)

############ STEP 5 ############
# INCREASE SPEED
################################

logging.basicConfig(level=logging.INFO)

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 437
FRAME_RATE = 30
GAME_SPEED = 8

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platform game')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

small_font = pygame.font.SysFont('comicsans', 30)

clock = pygame.time.Clock()

runner = Player(200, 313)
all_sprites = pygame.sprite.Group()
all_sprites.add(runner)

obstacles = pygame.sprite.Group()
ADD_OBSTACLE = USEREVENT + 1
pygame.time.set_timer(ADD_OBSTACLE, 2000)

INCREASE_SPEED = USEREVENT + 2                  # New
pygame.time.set_timer(INCREASE_SPEED, 8000)     # New

score = 0
running = True
speed = GAME_SPEED


def redraw_window():
    # Draw the background
    screen.blit(bg, (bgX, 0))
    screen.blit(bg, (bgX2, 0))

    # Draw all sprites
    all_sprites.update()
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    # Draw the score
    score_text = small_font.render('Score: ' + str(score), 1, (255, 255, 255))
    screen.blit(score_text, (700, 10))
    pygame.display.flip()


def add_obstacle():
    r = random.randrange(0, 2)
    obstacle = None
    if r == 0:
        obstacle = Saw(810, 313, speed)
        logging.info("Add saw obstacle")
    elif r == 1:
        obstacle = Spike(810, 0, speed)
        logging.info("Add spike obstacle")

    obstacles.add(obstacle)
    all_sprites.add(obstacle)


while running:
    bgX -= speed
    bgX2 -= speed

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == ADD_OBSTACLE:
            add_obstacle()
        elif event.type == INCREASE_SPEED:                          # New
            speed += 1                                              # New
            logging.info("Increase speed to {}".format(speed))      # New

    keys = pygame.key.get_pressed()
    if keys[K_SPACE] or keys[K_UP]:
        logging.debug("Space or key up!")
        if not runner.jumping: runner.jumping = True
    if keys[K_DOWN]:
        logging.debug("Key down!")
        if not runner.sliding: runner.sliding = True

    redraw_window()

    clock.tick(FRAME_RATE)


pygame.quit()