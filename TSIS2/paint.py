import pygame
from tools import draw_shape, flood_fill, save_canvas

pygame.init()
WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Application")
clock = pygame.time.Clock()


font = pygame.font.SysFont("Arial", 22)

text_font = pygame.font.SysFont("Arial", 32)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill("white")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (210, 210, 210)
DARK_GRAY = (120, 120, 120)
RED = (230, 50, 50)
GREEN = (50, 180, 70)
BLUE = (60, 120, 230)
YELLOW = (240, 220, 40)
PURPLE = (160, 80, 220)

colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, WHITE]


current_color = BLACK



tools = [
    "pencil",
    "line",
    "rectangle",
    "circle",
    "eraser",
    "fill",
    "text",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus"
]


current_tool = "pencil"


brush_size = 5


drawing = False

start_pos = None


last_pos = None



typing = False


text_pos = None


typed_text = ""



def canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


# Mouse canvas ішінде тұр ма, соны тексереді
def in_canvas(pos):
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def get_tool_from_click(pos):
    x, y = pos

    tool_x = 10

    for tool in tools:
       
        rect = pygame.Rect(tool_x, 10, 80, 30)

        
        if rect.collidepoint(x, y):
            return tool

        tool_x += 85

    return None



def get_color_from_click(pos):
    x, y = pos

    color_x = 10

    for color in colors:
        
        rect = pygame.Rect(color_x, 52, 32, 32)

        if rect.collidepoint(x, y):
            return color

        color_x += 40

    return None



def draw_toolbar():
    
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    tool_x = 10

    
    for tool in tools:
        rect = pygame.Rect(tool_x, 10, 80, 30)

        
        if tool == current_tool:
            pygame.draw.rect(screen, DARK_GRAY, rect)
        else:
            pygame.draw.rect(screen, WHITE, rect)

        # Батырма шекарасы
        pygame.draw.rect(screen, BLACK, rect, 2)

        # Tool атауын жазу
        tool_text = font.render(tool[:8], True, BLACK)
        screen.blit(tool_text, (tool_x + 5, 16))

        tool_x += 85

    color_x = 10

    # Түс батырмаларын салу
    for color in colors:
        rect = pygame.Rect(color_x, 52, 32, 32)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        # Таңдалған түс қалың қара шекарамен көрсетіледі
        if color == current_color:
            pygame.draw.rect(screen, BLACK, rect, 4)

        color_x += 40

    # Brush size және save shortcut туралы ақпарат
    info = font.render(
        f"Brush: {brush_size}px | 1=Small 2=Medium 3=Large | Ctrl+S=Save",
        True,
        BLACK
    )

    screen.blit(info, (330, 57))


running = True

while running:
    # Экранды ақ түске тазалау
    screen.fill(WHITE)

    # Canvas-ты toolbar-дың астына шығару
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Қазіргі mouse позициясы
    mouse_pos = pygame.mouse.get_pos()

    if drawing and start_pos and current_tool in [
        "line",
        "rectangle",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus"
    ]:
        preview = canvas.copy()

        
        end_pos = canvas_pos(mouse_pos)

        
        draw_shape(preview, current_tool, start_pos, end_pos, current_color, brush_size)

        
        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    
    if typing and text_pos:
        text_surface = text_font.render(typed_text + "|", True, current_color)
        screen.blit(text_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    
    draw_toolbar()

    
    for event in pygame.event.get():

        
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            # Ctrl + S басылса canvas сақталады
            if event.key == pygame.K_s and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                save_canvas(canvas)

            # Brush size ауыстыру
            if event.key == pygame.K_1:
                brush_size = 2

            elif event.key == pygame.K_2:
                brush_size = 5

            elif event.key == pygame.K_3:
                brush_size = 10

            # Егер text режимі қосулы болса
            if typing:

                # Enter басылса текст canvas-қа тұрақты сақталады
                if event.key == pygame.K_RETURN:
                    final_text = text_font.render(typed_text, True, current_color)
                    canvas.blit(final_text, text_pos)

                    typing = False
                    typed_text = ""
                    text_pos = None

                # Escape басылса текст жазу отмена болады
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    typed_text = ""
                    text_pos = None

                # Backspace соңғы әріпті өшіреді
                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                # Басқа клавиша болса, оны текстке қосамыз
                else:
                    typed_text += event.unicode

        
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Тек сол жақ mouse button
            if event.button == 1:
                pos = event.pos

                # Егер toolbar-ды басса
                if pos[1] < TOOLBAR_HEIGHT:
                    selected_tool = get_tool_from_click(pos)
                    selected_color = get_color_from_click(pos)

                    # Tool таңдау
                    if selected_tool:
                        current_tool = selected_tool
                        typing = False

                    # Color таңдау
                    if selected_color:
                        current_color = selected_color

                # Егер canvas-ты басса
                elif in_canvas(pos):
                    cpos = canvas_pos(pos)

                    # Fill tool болса, бірден аймақты бояйды
                    if current_tool == "fill":
                        flood_fill(canvas, cpos, current_color)

                    # Text tool болса, текст жазу режимін бастайды
                    elif current_tool == "text":
                        typing = True
                        text_pos = cpos
                        typed_text = ""

                    # Басқа drawing tool болса, drawing басталады
                    else:
                        drawing = True
                        start_pos = cpos
                        last_pos = cpos

        # ---------------- MOUSE MOTION ----------------
        if event.type == pygame.MOUSEMOTION:

            # Mouse қозғалып жатыр және drawing қосулы болса
            if drawing and in_canvas(event.pos):
                cpos = canvas_pos(event.pos)

                # Pencil үздіксіз сызық салады
                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, cpos, brush_size)
                    last_pos = cpos

                # Eraser ақ түспен өшіреді
                elif current_tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, cpos, brush_size)
                    last_pos = cpos

        # ---------------- MOUSE UP ----------------
        if event.type == pygame.MOUSEBUTTONUP:

            # Mouse жіберілгенде final shape салынады
            if event.button == 1 and drawing:
                if in_canvas(event.pos):
                    end_pos = canvas_pos(event.pos)

                    # Фигура canvas-қа енді ғана сақталады
                    if current_tool in [
                        "line",
                        "rectangle",
                        "circle",
                        "square",
                        "right_triangle",
                        "equilateral_triangle",
                        "rhombus"
                    ]:
                        draw_shape(canvas, current_tool, start_pos, end_pos, current_color, brush_size)

                # Drawing режимін тоқтату
                drawing = False
                start_pos = None
                last_pos = None

    # Экранды жаңарту
    pygame.display.flip()

    # FPS = 60
    clock.tick(60)


pygame.quit()