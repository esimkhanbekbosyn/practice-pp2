import pygame
import math

# -------------------- BASIC SETTINGS --------------------
pygame.init()

WIDTH, HEIGHT = 900, 650
TOOLBAR_HEIGHT = 80
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 16)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
RED = (220, 40, 40)
GREEN = (0, 170, 70)
BLUE = (40, 100, 230)
YELLOW = (255, 220, 0)
PURPLE = (150, 60, 200)

colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE]
current_color = BLACK

# Tools: square, right triangle, equilateral triangle, rhombus
current_tool = "square"

# Canvas surface keeps all finished drawings
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

start_pos = None
is_drawing = False


def get_canvas_pos(mouse_pos):
    # Convert screen coordinates to canvas coordinates
    return mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    text = font.render(
        "Tools: 1 Square | 2 Right Triangle | 3 Equilateral Triangle | 4 Rhombus | C Clear | Colors: click boxes",
        True,
        BLACK,
    )
    screen.blit(text, (10, 8))

    tool_text = font.render(f"Current tool: {current_tool}    Current color:", True, BLACK)
    screen.blit(tool_text, (10, 35))
    pygame.draw.rect(screen, current_color, (290, 35, 35, 25))
    pygame.draw.rect(screen, BLACK, (290, 35, 35, 25), 2)

    # Draw color boxes
    x = 350
    for color in colors:
        pygame.draw.rect(screen, color, (x, 35, 35, 25))
        pygame.draw.rect(screen, BLACK, (x, 35, 35, 25), 2)
        x += 45


def check_color_click(pos):
    global current_color
    x = 350
    for color in colors:
        rect = pygame.Rect(x, 35, 35, 25)
        if rect.collidepoint(pos):
            current_color = color
        x += 45


def draw_square(surface, start, end, color, width=3):
    x1, y1 = start
    x2, y2 = end

    size = min(abs(x2 - x1), abs(y2 - y1))
    if size == 0:
        return

    # Keep direction of dragging
    if x2 < x1:
        x1 -= size
    if y2 < y1:
        y1 -= size

    pygame.draw.rect(surface, color, (x1, y1, size, size), width)


def draw_right_triangle(surface, start, end, color, width=3):
    x1, y1 = start
    x2, y2 = end

    # Right triangle uses rectangle corners
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, start, end, color, width=3):
    x1, y1 = start
    x2, y2 = end

    # Base length depends on mouse drag
    side = abs(x2 - x1)
    if side == 0:
        return

    height = int(side * math.sqrt(3) / 2)

    # Direction: if dragged upward, triangle points up
    if y2 < y1:
        points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - height)]
    else:
        points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 + height)]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, start, end, color, width=3):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    # Rhombus points: top, right, bottom, left
    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y),
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_shape(surface, tool, start, end, color):
    if tool == "square":
        draw_square(surface, start, end, color)
    elif tool == "right triangle":
        draw_right_triangle(surface, start, end, color)
    elif tool == "equilateral triangle":
        draw_equilateral_triangle(surface, start, end, color)
    elif tool == "rhombus":
        draw_rhombus(surface, start, end, color)


def main():
    global current_tool, start_pos, is_drawing

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_tool = "square"
                elif event.key == pygame.K_2:
                    current_tool = "right triangle"
                elif event.key == pygame.K_3:
                    current_tool = "equilateral triangle"
                elif event.key == pygame.K_4:
                    current_tool = "rhombus"
                elif event.key == pygame.K_c:
                    canvas.fill(WHITE)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mouse_pos[1] < TOOLBAR_HEIGHT:
                    check_color_click(mouse_pos)
                else:
                    start_pos = get_canvas_pos(mouse_pos)
                    is_drawing = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if is_drawing and mouse_pos[1] >= TOOLBAR_HEIGHT:
                    end_pos = get_canvas_pos(mouse_pos)
                    # Draw final shape on canvas
                    draw_shape(canvas, current_tool, start_pos, end_pos, current_color)
                is_drawing = False
                start_pos = None

        screen.fill(WHITE)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))
        draw_toolbar()

        # Live preview while mouse is dragging
        if is_drawing and start_pos and mouse_pos[1] >= TOOLBAR_HEIGHT:
            preview_end = get_canvas_pos(mouse_pos)
            preview = canvas.copy()
            draw_shape(preview, current_tool, start_pos, preview_end, current_color)
            screen.blit(preview, (0, TOOLBAR_HEIGHT))
            draw_toolbar()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
