import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600

CELL_SIZE = 20

COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 130, 0)
RED = (220, 0, 0)
GRAY = (180, 180, 180)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 50)

snake = [(5, 5), (4, 5), (3, 5)]

direction = (1, 0)
next_direction = direction


score = 0
level = 1
speed = 8


walls = set()


for y in range(8, 20):
    walls.add((15, y))

for x in range(20, 27):
    walls.add((x, 10))


def draw_cell(position, color):
    
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def draw_snake():

    draw_cell(snake[0], GREEN)

    for part in snake[1:]:
        draw_cell(part, DARK_GREEN)


def draw_food():
   
    draw_cell(food, RED)


def draw_walls():
    
    for wall in walls:
        draw_cell(wall, GRAY)


def generate_food():
    
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake and pos not in walls:
            return pos


def move_snake():
    global score, food, level, speed

    
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    
    if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
        game_over()

    
    if new_head in walls:
        game_over()

    
    if new_head in snake:
        game_over()

    
    snake.insert(0, new_head)

   
    if new_head == food:
        score += 1
        food = generate_food()

     
        level = score // 4 + 1

        
        speed = 8 + (level - 1) * 2
    else:
        
        snake.pop()


def draw_info():
    
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(level_text, (WIDTH - 100, 10))


def game_over():
    
    screen.fill(WHITE)

    
    text = big_font.render("Game Over", True, RED)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()



food = generate_food()

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                next_direction = (1, 0)

    
    direction = next_direction

    
    move_snake()

    
    screen.fill(WHITE)

    
    draw_walls()
    draw_food()
    draw_snake()
    draw_info()

   
    pygame.display.update()

    clock.tick(speed)