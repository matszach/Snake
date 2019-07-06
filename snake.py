import pygame
from random import randint


# =================== COLORS =====================
COL_BACKGROUND = (0, 0, 0)
COL_GRID = (100, 100, 100)
COL_FRUIT = (255, 0, 0)
COL_SNAKE_BODY = (0, 255, 0)
COL_SNAKE_HEAD = (0, 140, 0)


# =================== VIEW VARS =====================
UNIT = 30
WIDTH = 20
HEIGHT = 20


# =================== GAME DATA =====================
score = [0]

snake = [(WIDTH/2, HEIGHT/2)]
direction = [0]  # 0 - up, 1 - right, 2 - down, 3 - left / list used for immutability

MAX_FRUITS = 1
fruits = []


# =================== DRAW FUNCTIONS =====================
def clear():
    surface.fill(COL_BACKGROUND)


def draw_grid():
    for i in range(WIDTH):
        pygame.draw.line(surface, COL_GRID, (UNIT * i, 0), (UNIT * i, UNIT * HEIGHT))
    for i in range(HEIGHT):
        pygame.draw.line(surface, COL_GRID, (0, UNIT * i), (UNIT * WIDTH, UNIT * i))


def draw_fruit():
    for f in fruits:
        pygame.draw.rect(surface, COL_FRUIT, (f[0] * UNIT, f[1] * UNIT, UNIT, UNIT))


def draw_snake():

    for seg in snake:
        pygame.draw.rect(surface, COL_SNAKE_BODY, (seg[0] * UNIT, seg[1] * UNIT, UNIT, UNIT))

    head = snake_get_head()
    pygame.draw.rect(surface, COL_SNAKE_HEAD, (head[0] * UNIT + 5, head[1] * UNIT + 5, UNIT - 10, UNIT - 10))


# =================== GAME LOGIC FUNCTIONS =====================
def handle_fruit_spawn():
    while len(fruits) < MAX_FRUITS:
        x = randint(0, WIDTH - 1)
        y = randint(0, HEIGHT - 1)
        if (x, y) not in snake + fruits:
            fruits.append((x, y))


def snake_get_head():
    return snake[-1]


def snake_pop_tail():
    del snake[0]


def snake_check_fruit():

    head = snake_get_head()

    if head in fruits:
        fruits.remove(head)
        score[0] += 1
        return True

    else:
        return False


def snake_check_dead():
    return snake_get_head() in snake[:-1]


def handle_snake_move():

    curr_hx, curr_hy = snake_get_head()

    if direction[0] == 0:
        next_hx, next_hy = curr_hx, curr_hy - 1
        if next_hy < 0:
            next_hy += HEIGHT
    elif direction[0] == 1:
        next_hx, next_hy = curr_hx + 1, curr_hy
        if next_hx >= WIDTH:
            next_hx -= WIDTH
    elif direction[0] == 2:
        next_hx, next_hy = curr_hx, curr_hy + 1
        if next_hy >= HEIGHT:
            next_hy -= HEIGHT
    else:  # 3
        next_hx, next_hy = curr_hx - 1, curr_hy
        if next_hx < 0:
            next_hx += WIDTH

    if not snake_check_fruit():
        snake_pop_tail()

    snake.append((next_hx, next_hy))


# =================== USER INPUT =====================
def handle_user_input():
    
    d = direction[0]
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        if d is not 2:
            d = 0

    if keys[pygame.K_d]:
        if d is not 3:
            d = 1

    if keys[pygame.K_s]:
        if d is not 0:
            d = 2

    if keys[pygame.K_a]:
        if d is not 1:
            d = 3

    direction[0] = d


# =================== PYGAME INIT =====================
surface = pygame.display.set_mode((UNIT*WIDTH, UNIT*HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

# =================== MAIN LOOP =====================
while True:

    clock.tick(8)  # 5 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    clear()
    draw_grid()

    handle_fruit_spawn()
    draw_fruit()

    handle_user_input()
    handle_snake_move()
    draw_snake()

    if snake_check_dead():
        print(f'* GAME OVER! * \nYOUR SCORE WAS: {score[0]}!')
        exit()

    # draws current game state on display
    pygame.display.update()



