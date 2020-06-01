import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
WHITE = (255,255,255)
BLACK = (0,0,0)
SKY_BLUE = (135, 206, 250)

eggs_catched = 0
eggs_broken = 0

class Bunny(pygame.sprite.Sprite):
    HEIGHT = SCREEN_HEIGHT - 165
    def __init__(self):
        super(Bunny, self).__init__()
        self.surface = pygame.image.load("media/bunny.png").convert()
        self.surface = pygame.transform.scale(self.surface, (218, 330))
        self.surface.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.surface.get_rect(center=(SCREEN_WIDTH / 2, self.HEIGHT))
        # Stores if player is jumping or not
        self.isjump = False
        # Force (v) up and mass m.
        self.v = 10
        self.m = 1

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        speedboost = 0
        if self.isjump:
            self.jumping()
        elif pressed_keys[K_SPACE]:
                            self.isjump = True
        if pressed_keys[K_DOWN]:
            speedboost = 100
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-20-speedboost, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(20+speedboost, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def jumping(self):
        # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
        F = (1 / 2) * self.m * (self.v ** 2)
        # change in the y co-ordinate
        self.rect.y -= F
        # decreasing velocity while going up and become negative while coming down
        self.v = self.v - 1
        # object reached its maximum height
        if self.v < 0:
            # negative sign is added to counter negative velocity
            self.m = -1
        # objected reaches its original state
        if self.v <= -10:
            # making isjump equal to false
            self.isjump = False
            # setting original values to v and m
            self.v = 10
            self.m = 1
            self.rect.bottom=SCREEN_HEIGHT


class Egg(pygame.sprite.Sprite):
    def __init__(self):
        super(Egg, self).__init__()
        self.surface = pygame.image.load("media/easter-egg.png").convert()
        self.surface = pygame.transform.scale(self.surface, (131, 180))
        self.surface.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.surface.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), 0))
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the bottom edge of the screen
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= SCREEN_HEIGHT:
            global eggs_broken
            eggs_broken += 1
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surface = pygame.image.load("media/cloud.png").convert()
        self.surface = pygame.transform.scale(self.surface, (75, 75))
        self.surface.set_colorkey(BLACK, RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surface.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT / 3),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()


# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont('mono', 24, bold=True)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

ADD_EGG = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_EGG, 1000)

ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 2000)

eggs = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

bunny = Bunny()
all_sprites.add(bunny)

# Variable to keep the main loop running
running = True

def paint_grass():
    surface = pygame.image.load("media/grass.png").convert()
    surface = pygame.transform.scale(surface, (125, 75))
    surface.set_colorkey(BLACK, RLEACCEL)
    for i in range(0, 16):
        screen.blit(surface, (i*125, SCREEN_HEIGHT-75))

def show_score():
    score_text = "Score: {} ({} eieren gevangen, {} eieren gebroken)".format(eggs_catched-eggs_broken, eggs_catched, eggs_broken)
    fw, fh = font.size(score_text)
    surface = font.render(score_text, True, (0, 0, 0))
    screen.blit(surface, (50, 20))

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        # Add a new egg?
        elif event.type == ADD_EGG:
            # Create the new egg and add it to sprite groups
            new_egg = Egg()
            eggs.add(new_egg)
            all_sprites.add(new_egg)
        # Add a new cloud?
        elif event.type == ADD_CLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    bunny.update(pressed_keys)

    screen.fill(SKY_BLUE)
    paint_grass()

    # Update the position of our eggs and clouds
    eggs.update()
    clouds.update()

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surface, entity.rect)

    # Check if any eggs have collided with the bunny
    if pygame.sprite.spritecollide(bunny, eggs, True):
        eggs_catched += 1
        print("Ei gevangen!")

    show_score()

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()
