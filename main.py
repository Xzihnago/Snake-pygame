from collections import deque
from typing import Deque
from random import randint

import pygame

# Constants
TPS = 3
GRID_WIDTH = 20
GRID_HEIGHT = 20
GRID_SIZE = 30

FPS = 60
COLOR_BACKGROUND = (220, 220, 220)
COLOR_HIGHLIGHT_TEXT = (255, 0, 0)
COLOR_FRUIT = (0, 255, 0)
COLOR_SNAKE_HEAD = (255, 0, 0)
COLOR_SNAKE_BODY = (127, 127, 127)


class Vector2(pygame.Vector2):
    zero = pygame.Vector2(0, 0)
    down = pygame.Vector2(0, 1)
    up = pygame.Vector2(0, -1)
    left = pygame.Vector2(-1, 0)
    right = pygame.Vector2(1, 0)


class Fruit(pygame.Vector2):
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = randint(0, GRID_WIDTH - 1)
        self.y = randint(0, GRID_HEIGHT - 1)

    def draw(self):
        rect = pygame.Rect(GRID_SIZE * self.x, GRID_SIZE * self.y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, COLOR_FRUIT, rect)


class Snake():
    def __init__(self):
        self.head = pygame.Vector2(GRID_WIDTH >> 1, GRID_HEIGHT >> 1)
        self.body: Deque[pygame.Vector2] = deque()
        self.length = 0
        self.direction = Vector2.zero

    def update(self):
        self.body.append(self.head)
        self.head = self.head + self.direction

        if len(self.body) > self.length:
            self.body.popleft()

    def draw(self):
        # Head
        rect = pygame.Rect(GRID_SIZE * self.head.x, GRID_SIZE * self.head.y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, COLOR_SNAKE_HEAD, rect)

        # Body
        for part in canva.snake.body:
            rect = pygame.Rect(GRID_SIZE * part.x, GRID_SIZE * part.y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, COLOR_SNAKE_BODY, rect)


class Canva():
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = True
        self.fruit = Fruit()
        self.snake = Snake()

    def update(self):
        # Check gameover
        nexthead = self.snake.head + self.snake.direction
        if nexthead in self.snake.body or nexthead.x > GRID_WIDTH - 1 or nexthead.x < 0 or nexthead.y > GRID_HEIGHT - 1 or nexthead.y < 0:
            self.game = False
            return

        self.snake.update()

        # Check eat
        if self.snake.head == self.fruit:
            self.fruit.reset()
            self.snake.length += 1

    def draw(self):
        surface.fill(COLOR_BACKGROUND)

        self.fruit.draw()
        self.snake.draw()

        if self.game:
            text = font.render(f'Score: {self.snake.length}', True, 0)
            surface.blit(text, (10, 10))

            text = font.render('Press P to pause', True, 0)
            surface.blit(text, (CANVA_WIDTH - text.get_width() - 10, 10))

        else:
            text = font.render('GameOver', True, 0)
            surface.blit(text, (CANVA_WIDTH - text.get_width() >> 1, (CANVA_HEIGHT - text.get_height() >> 1) - 40))

            text = font.render(f'Score: {self.snake.length}', True, COLOR_HIGHLIGHT_TEXT)
            surface.blit(text, (CANVA_WIDTH - text.get_width() >> 1, CANVA_HEIGHT - text.get_height() >> 1))

            text = font.render('Press R to restart', True, 0)
            surface.blit(text, (CANVA_WIDTH - text.get_width() >> 1, (CANVA_HEIGHT - text.get_height() >> 1) + 40))


# Init
CANVA_WIDTH = GRID_SIZE * GRID_WIDTH
CANVA_HEIGHT = GRID_SIZE * GRID_HEIGHT

pygame.init()
pygame.display.set_caption('Snake')
surface = pygame.display.set_mode((CANVA_WIDTH, CANVA_HEIGHT))
font = pygame.font.SysFont('Verdana', 20)
clock = pygame.time.Clock()

# Main loop
canva = Canva()
is_running = True
is_pause = False
cnt_tick = 0

while is_running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                is_pause = not is_pause

            elif event.key == pygame.K_r and not canva.game:
                canva.reset()

            if canva.snake.direction != Vector2.down and canva.snake.direction != Vector2.up:
                if event.key == pygame.K_DOWN:
                    canva.snake.direction = Vector2.down

                elif event.key == pygame.K_UP:
                    canva.snake.direction = Vector2.up

            if canva.snake.direction != Vector2.left and canva.snake.direction != Vector2.right:
                if event.key == pygame.K_LEFT:
                    canva.snake.direction = Vector2.left

                elif event.key == pygame.K_RIGHT:
                    canva.snake.direction = Vector2.right

    # Draw
    if not is_pause:
        cnt_tick += 1
        if cnt_tick % (FPS // TPS) == 0 and canva.game:
            canva.update()

        canva.draw()

    else:
        text = font.render('Pause', True, 0)
        surface.blit(text, (CANVA_WIDTH - text.get_width() >> 1, CANVA_HEIGHT - text.get_height() >> 1))

    # Update
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()