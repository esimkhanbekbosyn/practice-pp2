import pygame
import math
from collections import deque
from datetime import datetime


# Әртүрлі фигураларды салатын функция
def draw_shape(surface, tool, start, end, color, size):
    x1, y1 = start
    x2, y2 = end

    # Түзу сызық салу
    if tool == "line":
        pygame.draw.line(surface, color, start, end, size)

    # Тік төртбұрыш салу
    elif tool == "rectangle":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, rect, size)

    # Шеңбер салу (start → центр, end → радиус)
    elif tool == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, color, start, radius, size)

    # Квадрат салу (барлық қабырғалары тең)
    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))

        if x2 < x1:
            x1 = x1 - side

        if y2 < y1:
            y1 = y1 - side

        rect = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(surface, color, rect, size)

    # Тік бұрышты үшбұрыш
    elif tool == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, size)

    # Теңқабырғалы үшбұрыш
    elif tool == "equilateral_triangle":
        side = x2 - x1
        height = int(abs(side) * math.sqrt(3) / 2)

        if y2 < y1:
            points = [(x1, y1), (x2, y1), ((x1 + x2) // 2, y1 - height)]
        else:
            points = [(x1, y1), (x2, y1), ((x1 + x2) // 2, y1 + height)]

        pygame.draw.polygon(surface, color, points, size)

    # Ромб салу
    elif tool == "rhombus":
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        points = [
            (center_x, y1),
            (x2, center_y),
            (center_x, y2),
            (x1, center_y)
        ]

        pygame.draw.polygon(surface, color, points, size)


# Flood fill — "ведро" сияқты бояу
def flood_fill(surface, start_pos, new_color):
    width, height = surface.get_size()
    x, y = start_pos

    # Егер тышқан canvas сыртында болса — ештеңе істемейміз
    if x < 0 or x >= width or y < 0 or y >= height:
        return

    # Бастапқы пиксельдің түсі
    old_color = surface.get_at((x, y))

    # Егер жаңа түс сол түспен бірдей болса — толтыру қажет емес
    if old_color == new_color:
        return

    # Кезек (queue) арқылы барлық көрші пиксельдерді қараймыз
    queue = deque()
    queue.append((x, y))

    while queue:
        cx, cy = queue.popleft()

        # Шекарадан шықса — өткізіп жібереміз
        if cx < 0 or cx >= width or cy < 0 or cy >= height:
            continue

        # Тек бастапқы түске тең пиксельдерді ғана бояймыз
        if surface.get_at((cx, cy)) != old_color:
            continue

        # Пиксельді жаңа түске бояу
        surface.set_at((cx, cy), new_color)

        # Көрші пиксельдерді қосу
        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))


# Canvas-ты PNG файлға сақтау (уақытпен бірге)
def save_canvas(canvas):
    filename = datetime.now().strftime("paint_%Y-%m-%d_%H-%M-%S.png")
    pygame.image.save(canvas, filename)
    print("Save: ", filename)