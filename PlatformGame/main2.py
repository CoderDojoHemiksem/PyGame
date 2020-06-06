import pygame
import os
from PlatformGame.sprite.Player import Player # New

########### STEP 2 ###########
# ADD PLAYER
##############################

# Initialize pygame
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 437
FRAME_RATE = 30
GAME_SPEED = 8 # New

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platform game')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

small_font = pygame.font.SysFont('comicsans', 30)

clock = pygame.time.Clock()

runner = Player(200, 313) # New
all_sprites = pygame.sprite.Group() #New
all_sprites.add(runner) # New

score = 0
running = True
speed = GAME_SPEED # New

def redraw_window():
    screen.blit(bg, (bgX, 0))
    screen.blit(bg, (bgX2, 0))

    all_sprites.update() # New
    screen.blit(runner.image, runner.rect) # New

    score_text = small_font.render('Score: ' + str(score), 1, (255, 255, 255))
    screen.blit(score_text, (700, 10))
    pygame.display.flip()


while running:
    bgX -= speed # New
    bgX2 -= speed # New

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    redraw_window()

    clock.tick(FRAME_RATE)


pygame.quit()