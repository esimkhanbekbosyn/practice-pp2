import pygame
import random

# -------------------- BASIC SETTINGS --------------------
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Racer")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
RED = (220, 40, 40)
BLUE = (50, 120, 255)
GREEN = (40, 200, 80)

font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 16)

# Road lane positions
LANES = [90, 160, 230, 300]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Simple rectangle car, so no image assets are needed
        self.image = pygame.Surface((45, 75))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 90))
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()

        # Move left/right
        if keys[pygame.K_LEFT] and self.rect.left > 45:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 45:
            self.rect.x += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 75))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.reset_position()

    def reset_position(self):
        # Enemy appears in a random lane above the screen
        self.rect.centerx = random.choice(LANES)
        self.rect.y = random.randint(-250, -80)

    def update(self):
        self.rect.y += self.speed

        # If enemy leaves screen, spawn it again
        if self.rect.top > HEIGHT:
            self.reset_position()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Different coin weights: value, radius, color
        self.coin_types = [
            {"value": 1, "radius": 10, "color": YELLOW},
            {"value": 2, "radius": 13, "color": ORANGE},
            {"value": 3, "radius": 16, "color": GREEN},
        ]

        self.value = 1
        self.radius = 10
        self.color = YELLOW
        self.image = None
        self.rect = None
        self.speed = 5
        self.randomize()

    def randomize(self):
        # Choose random weight for coin
        coin_type = random.choice(self.coin_types)
        self.value = coin_type["value"]
        self.radius = coin_type["radius"]
        self.color = coin_type["color"]

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = random.randint(-400, -50)

    def update(self):
        self.rect.y += self.speed

        # If coin leaves screen, create new random coin
        if self.rect.top > HEIGHT:
            self.randomize()


def draw_road():
    screen.fill(GRAY)

    # Road borders
    pygame.draw.line(screen, WHITE, (40, 0), (40, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (360, 0), (360, HEIGHT), 5)

    # Lane dashed lines
    for x in [125, 195, 265]:
        for y in range(0, HEIGHT, 80):
            pygame.draw.line(screen, WHITE, (x, y), (x, y + 40), 3)


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
    player = Player()
    enemy = Enemy()
    coin = Coin()

    all_sprites = pygame.sprite.Group(player, enemy, coin)
    enemies = pygame.sprite.Group(enemy)
    coins = pygame.sprite.Group(coin)

    score = 0
    collected_coins = 0
    speed_level = 0
    N = 5  # Enemy speed increases after every N collected coin points

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        # Check collision with enemy
        if pygame.sprite.spritecollideany(player, enemies):
            game_over(score)
            running = False

        # Check collision with coin
        hit_coin = pygame.sprite.spritecollideany(player, coins)
        if hit_coin:
            score += hit_coin.value
            collected_coins += hit_coin.value
            hit_coin.randomize()

            # Increase enemy speed after player earns N coin points
            new_speed_level = collected_coins // N
            if new_speed_level > speed_level:
                speed_level = new_speed_level
                enemy.speed += 1
                coin.speed += 0.5

        draw_road()
        all_sprites.draw(screen)

        score_text = font.render(f"Coins: {score}", True, WHITE)
        speed_text = small_font.render(f"Enemy speed: {enemy.speed}", True, WHITE)
        screen.blit(score_text, (WIDTH - 140, 10))
        screen.blit(speed_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
