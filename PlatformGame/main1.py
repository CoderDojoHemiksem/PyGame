import pygame
import os

########### STEP 1 ###########
# MOVING BACKGROUND
##############################

# Initialize pygame
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 437
FRAME_RATE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platform game')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

small_font = pygame.font.SysFont('comicsans', 30)

clock = pygame.time.Clock()

score = 0
running = True


def redraw_window():
    screen.blit(bg, (bgX, 0))
    screen.blit(bg, (bgX2, 0))
    score_text = small_font.render('Score: ' + str(score), 1, (255, 255, 255))

    screen.blit(score_text, (700, 10))
    pygame.display.flip()


while running:
    bgX -= 2
    bgX2 -= 2

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