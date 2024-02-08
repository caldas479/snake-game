import pygame
import random
import os
from time import sleep

pygame.init()

# Screen Initializing
WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Pixel
PIXEL_LENGTH = 50
MAX_PIXEL_WIDTH = (WIDTH-PIXEL_LENGTH)/PIXEL_LENGTH
MAX_PIXEL_HEIGHT = (HEIGHT-PIXEL_LENGTH)/PIXEL_LENGTH

# Screen limits coordinates
TOP_SIDE_LIMIT = [[x, -PIXEL_LENGTH] for x in range(0, WIDTH, PIXEL_LENGTH)]
BOTTOM_SIDE_LIMIT = [[x, HEIGHT] for x in range(0, WIDTH, PIXEL_LENGTH)]
LEFT_SIDE_LIMIT = [[-PIXEL_LENGTH, y] for y in range(0, HEIGHT, PIXEL_LENGTH)]
RIGHT_SIDE_LIMIT = [[WIDTH, y] for y in range(0, HEIGHT, PIXEL_LENGTH)]
LIMITS = TOP_SIDE_LIMIT + BOTTOM_SIDE_LIMIT + LEFT_SIDE_LIMIT + RIGHT_SIDE_LIMIT

# FPS
FPS = 10

# Colors
GREY = (25, 25, 23)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Score text font
SCORE_FONT = pygame.font.SysFont('comicsans', 30)

# Game Over font
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)

# Snake head coordinates
SNAKE_HEAD = [450, 350]

# Snake body coordinates
SNAKE_BODY = [[450, 350], [400, 350], [350, 350]]

# Snake Images
SNAKE_HEAD_IMAGE2SCALE = pygame.image.load(
    os.path.join('Assets', 'snake_head.png'))
SNAKE_HEAD_IMAGE_SCALED = pygame.transform.scale(
    SNAKE_HEAD_IMAGE2SCALE, (PIXEL_LENGTH, PIXEL_LENGTH))

SNAKE_HEAD_UP = pygame.transform.rotate(SNAKE_HEAD_IMAGE_SCALED, 180)
SNAKE_HEAD_DOWN = SNAKE_HEAD_IMAGE_SCALED
SNAKE_HEAD_LEFT = pygame.transform.rotate(SNAKE_HEAD_IMAGE_SCALED, 270)
SNAKE_HEAD_RIGHT = pygame.transform.rotate(SNAKE_HEAD_IMAGE_SCALED, 90)

SNAKE_HEAD_IMAGES = {'UP': SNAKE_HEAD_UP,
                     'DOWN': SNAKE_HEAD_DOWN,
                     'LEFT': SNAKE_HEAD_LEFT,
                     'RIGHT': SNAKE_HEAD_RIGHT}

SNAKE_BODY_IMAGE2SCALE = pygame.image.load(
    os.path.join('Assets', 'snake_body.png'))
SNAKE_BODY_IMAGE = pygame.transform.scale(
    SNAKE_BODY_IMAGE2SCALE, (PIXEL_LENGTH, PIXEL_LENGTH))

# Food has a list with coordinates and a state
FOOD = {'pos': [], 'exists': False}

# Event when food is eaten
FOOD_EATEN = pygame.USEREVENT

# Apple Image
APPLE_IMAGE2SCALE = pygame.image.load(os.path.join('Assets', 'apple.png'))
APPLE_IMAGE = pygame.transform.scale(
    APPLE_IMAGE2SCALE, (PIXEL_LENGTH, PIXEL_LENGTH))

# Sounds
pygame.mixer.init() 
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'game_over.wav'))
BITE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bite.wav'))


def set_food_pos():
    pos = [PIXEL_LENGTH*random.randint(1, MAX_PIXEL_WIDTH),
           PIXEL_LENGTH*random.randint(1, MAX_PIXEL_HEIGHT)]
    if pos not in SNAKE_BODY:
        FOOD['pos'] = pos
        FOOD['exists'] = True


def draw_screen(snake_direction, score):
    SCREEN.fill(GREY)
    score_text = SCORE_FONT.render('Score: ' + str(score), 1, WHITE)
    SCREEN.blit(score_text, (10, 10))
    draw_snake(snake_direction)
    draw_food()


def draw_game_over_screen(score):
    SCREEN.fill(GREY)
    game_over_text = GAME_OVER_FONT.render('GAME OVER', 1, RED)
    SCREEN.blit(game_over_text, (100, 300))
    score_text = SCORE_FONT.render('Your score was ' + str(score), 1, WHITE)
    SCREEN.blit(score_text, (300, 500))


def draw_snake(snake_direction):
    SCREEN.blit(SNAKE_HEAD_IMAGES[snake_direction], SNAKE_HEAD)
    for i in range(1, len(SNAKE_BODY)):
        pos = SNAKE_BODY[i]
        SCREEN.blit(SNAKE_BODY_IMAGE, pos)


def draw_food():
    if FOOD['exists']:
        SCREEN.blit(APPLE_IMAGE, FOOD['pos'])


def move_snake(snake_direction):

    if snake_direction == 'UP':
        SNAKE_HEAD[1] -= PIXEL_LENGTH
    if snake_direction == 'DOWN':
        SNAKE_HEAD[1] += PIXEL_LENGTH
    if snake_direction == 'LEFT':
        SNAKE_HEAD[0] -= PIXEL_LENGTH
    if snake_direction == 'RIGHT':
        SNAKE_HEAD[0] += PIXEL_LENGTH

    if SNAKE_BODY[0] not in SNAKE_BODY[1:] and SNAKE_BODY[0] not in LIMITS:
        SNAKE_BODY.insert(0, list(SNAKE_HEAD))
        if SNAKE_BODY[0][0] == FOOD['pos'][0] and SNAKE_BODY[0][1] == FOOD['pos'][1]:
            FOOD['exists'] = False
            pygame.event.post(pygame.event.Event(FOOD_EATEN))
            BITE_SOUND.play()
        else:
            SNAKE_BODY.pop()
        return True

    return False


def main():
    clock = pygame.time.Clock()
    game_on = True
    snake_direction = 'RIGHT'
    direction = snake_direction
    score = 0
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                if event.key == pygame.K_UP:
                    direction = 'UP'
                if event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'

            # Score updates when snake eats the food
            if event.type == FOOD_EATEN:
                score += 1

        # Changes snake direction when key pressed is valid
        if direction == 'UP' and snake_direction != 'DOWN':
            snake_direction = 'UP'
        if direction == 'DOWN' and snake_direction != 'UP':
            snake_direction = 'DOWN'
        if direction == 'LEFT' and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        if direction == 'RIGHT' and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'

        # Generates random food position
        while not(FOOD['exists']):
            set_food_pos()

        draw_screen(snake_direction, score)

        if not(move_snake(snake_direction)):
            game_on = False
            GAME_OVER_SOUND.play()
            draw_game_over_screen(score)

        pygame.display.update()
        clock.tick(FPS)

    sleep(5)


if __name__ == '__main__':
    main()
