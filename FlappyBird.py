import pygame, random, time
from pygame.locals import *

SCREEN_W = 300
SCREEN_H = 600
SPEED = 10
GRAVITY = 1
GAME_SPEED = 5

GROUND_W = 2 * SCREEN_W
GROUND_H = 100

PIPE_W = 80
PIPE_H = 400

PIPE_GAP = 150

black = (0, 0, 0)


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('assets/yellowbird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/yellowbird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()]
        self.current = 0
        self.speed = SPEED

        self.image = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_W / 2 - 12
        self.rect[1] = SCREEN_H / 2 - 17

    def update(self):
        self.current = (self.current + 1) % 3
        self.image = self.images[self.current]

        self.speed += GRAVITY
        # Update height
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED


class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, x_position, y_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_W, PIPE_H))
        self.rect = self.image.get_rect()
        self.rect[0] = x_position

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - y_size)
        else:
            self.rect[1] = SCREEN_H - y_size

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):
    def __init__(self, x_position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_W, GROUND_H))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = x_position
        self.rect[1] = SCREEN_H - GROUND_H

    def update(self):
        self.rect[0] -= GAME_SPEED


def if_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(x_position):
    size = random.randint(140, 400)
    pipe = Pipe(False, x_position, size)
    pipe_inverted = Pipe(True, x_position, SCREEN_H - size - PIPE_GAP)
    return (pipe, pipe_inverted)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def score_count(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(count), True, black)
    screen.blit(text, (10, SCREEN_H - 30))

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 40)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((SCREEN_W / 2), (SCREEN_H / 2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)
    game_loop()

def game_loop():
    score = 0;
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(i * SCREEN_W)
        ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
    for i in range(2):
        print(i)
        pipes = get_random_pipes(SCREEN_W * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.bump()

        screen.blit(BACKGROUND, (0, 0))

        if if_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_W - 310)
            ground_group.add(new_ground)

        if if_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(SCREEN_W * 2)

            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        # print(bird_group.sprites())
        # print(pipe_group.sprites())
        bird_group.update()
        pipe_group.update()
        ground_group.update()

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)

        if (pipe_group.sprites()[0].rect[0] == SCREEN_W / 2 or
            pipe_group.sprites()[1].rect[0] == SCREEN_W / 2):
            score += 1
        score_count(score)

        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            # Game over
            message_display('Game over')
            input()

        pygame.display.update()


pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

BACKGROUND = pygame.image.load('assets/background-day.png').convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_W, SCREEN_H))

game_loop()
pygame.quit()
quit()
