import pygame
import random

# -------------------- BASIC SETTINGS --------------------
pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 16)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (230, 50, 50)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
BLUE = (60, 160, 255)


class Food:
    def __init__(self, snake_body):
        # Food types have different weights and life time
        self.types = [
            {"weight": 1, "color": RED, "lifetime": 6000},
            {"weight": 2, "color": YELLOW, "lifetime": 4500},
            {"weight": 3, "color": ORANGE, "lifetime": 3000},
        ]
        self.spawn(snake_body)

    def spawn(self, snake_body):
        food_type = random.choice(self.types)
        self.weight = food_type["weight"]
        self.color = food_type["color"]
        self.lifetime = food_type["lifetime"]
        self.spawn_time = pygame.time.get_ticks()

        # Generate food not on snake body
        while True:
            self.position = [random.randint(0, COLS - 1), random.randint(0, ROWS - 1)]
            if self.position not in snake_body:
                break

    def is_expired(self):
        # Food disappears after lifetime milliseconds
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.lifetime

    def draw(self):
        x = self.position[0] * CELL
        y = self.position[1] * CELL
        pygame.draw.rect(screen, self.color, (x, y, CELL, CELL))

        # Show food weight number inside food
        text = small_font.render(str(self.weight), True, BLACK)
        screen.blit(text, text.get_rect(center=(x + CELL // 2, y + CELL // 2)))


def draw_snake(snake):
    for index, part in enumerate(snake):
        x = part[0] * CELL
        y = part[1] * CELL
        color = GREEN if index == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (x, y, CELL, CELL))


def game_over(score):
    screen.fill(BLACK)
    text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    info = small_font.render("Press ESC to quit", True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False


def main():
    # Snake is stored in cell coordinates: [col, row]
    snake = [[5, 5], [4, 5], [3, 5]]
    direction = [1, 0]
    next_direction = [1, 0]

    food = Food(snake)
    score = 0
    speed = 8

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Prevent reverse movement into itself
                if event.key == pygame.K_UP and direction != [0, 1]:
                    next_direction = [0, -1]
                elif event.key == pygame.K_DOWN and direction != [0, -1]:
                    next_direction = [0, 1]
                elif event.key == pygame.K_LEFT and direction != [1, 0]:
                    next_direction = [-1, 0]
                elif event.key == pygame.K_RIGHT and direction != [-1, 0]:
                    next_direction = [1, 0]

        direction = next_direction

        # New head position
        head = snake[0]
        new_head = [head[0] + direction[0], head[1] + direction[1]]

        # Wall collision
        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
            game_over(score)
            running = False
            continue

        # Self collision
        if new_head in snake:
            game_over(score)
            running = False
            continue

        snake.insert(0, new_head)

        # Eating food
        if new_head == food.position:
            score += food.weight

            # Grow according to food weight
            for _ in range(food.weight - 1):
                snake.append(list(snake[-1]))

            food.spawn(snake)

            # Increase speed slowly when score grows
            speed = 8 + score // 5
        else:
            # Remove tail if food is not eaten
            snake.pop()

        # If food time ended, create new food
        if food.is_expired():
            food.spawn(snake)

        screen.fill(BLACK)
        draw_snake(snake)
        food.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        speed_text = small_font.render(f"Speed: {speed}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (10, 40))

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()


if __name__ == "__main__":
    main()
