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

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

runner = Player(200, 313)
all_sprites.add(runner)

ADD_OBSTACLE = USEREVENT + 1
INCREASE_SPEED = USEREVENT + 2

pygame.time.set_timer(ADD_OBSTACLE, 2000)
pygame.time.set_timer(INCREASE_SPEED, 8000)

running = True
frame_rate = FRAME_RATE
speed = GAME_SPEED
counter = 0
score = 0
pause = 0


def init_game():
    global running, frame_rate, speed, counter, score, pause
    running = True
    frame_rate = FRAME_RATE
    speed = GAME_SPEED
    counter = 0
    score = 0
    pause = 0
    runner.falling = False
    runner.sliding = False
    runner.jumping = False
    for obstacle in obstacles:
        obstacle.kill()
        obstacles.remove(obstacle)


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

    # Update the display
    #pygame.display.update()
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


def end_screen():
    end_run = True
    while end_run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                end_run = False
                init_game()

        screen.blit(bg, (0, 0))
        large_font = pygame.font.SysFont('comicsans', 80)
        last_score = large_font.render("Best Score: " + str(update_score()), 1, (255, 255, 255))
        current_score = large_font.render("Score: " + str(score), 1, (255, 255, 255))
        screen.blit(last_score, (int(SCREEN_WIDTH / 2 - last_score.get_width() / 2), 150))
        screen.blit(current_score, (int(SCREEN_WIDTH / 2 - current_score.get_width() / 2), 240))
        pygame.display.update()


def update_score():
    last = 0
    with open("scores.txt", "r+") as f:
        file = f.readlines()
        if len(file) > 0:
            last = int(file[0])
    if last < int(score):
        with open("scores.txt", "w+") as f:
            f.write(str(score))
        return score
    return last


while running:

    if pause > 0:
        pause += 1
        if pause > 20:
            end_screen()
    else:
        counter += 1
        score = counter // 100

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
        elif event.type == INCREASE_SPEED:
            speed += 1
            logging.info("Increase speed to {}".format(speed))

    keys = pygame.key.get_pressed()
    if keys[K_SPACE] or keys[K_UP]:
        logging.debug("Space or key up!")
        if not runner.jumping: runner.jumping = True
    if keys[K_DOWN]:
        logging.debug("Key down!")
        if not runner.sliding: runner.sliding = True

    redraw_window()

    # Check if any obstacles have collided with the runner
    if pygame.sprite.spritecollideany(runner, obstacles):
        # If so, then remove the player and stop the loop
        runner.falling = True
        pause = 1

    clock.tick(frame_rate)


pygame.quit()