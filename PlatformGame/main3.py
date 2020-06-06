import pygame
import logging, os # New
from PlatformGame.sprite.Player import Player

############ STEP 3 ############
# LET THE PLAYER JUMP AND SLIDE
################################

logging.basicConfig(level=logging.DEBUG) # New

# Initialize pygame
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

score = 0
running = True
speed = GAME_SPEED

def redraw_window():
    screen.blit(bg, (bgX, 0))
    screen.blit(bg, (bgX2, 0))

    all_sprites.update()
    screen.blit(runner.image, runner.rect)

    score_text = small_font.render('Score: ' + str(score), 1, (255, 255, 255))
    screen.blit(score_text, (700, 10))
    pygame.display.flip()


while running:
    bgX -= speed
    bgX2 -= speed

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()                     # New
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:       # New
        logging.debug("Space or key up!")               # New
        if not runner.jumping: runner.jumping = True    # New
    if keys[pygame.K_DOWN]:                             # New
        logging.debug("Key down!")                      # New
        if not runner.sliding: runner.sliding = True    # New

    redraw_window()

    clock.tick(FRAME_RATE)


pygame.quit()