import pygame
from random import *
import sys

pygame.init()
width = 550
height = 700
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('bahnschrift', 36)

title = pygame.Rect(0, 0, 550, 150)

# Цвета
WHITE = (255, 255, 255)
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          4096: (0, 0, 0),
          8192: (0, 0, 0),
          16384: (0, 0, 0),
          32768: (0, 0, 0),
          65536: (0, 0, 0),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'bg': (187, 173, 160)}

def printing(field): # Печать игрового поля в консоли
    print('-' * 10)
    for row in field:
        print(*row)
    print('-' * 10)

empty_cell = [] # Список пустых ячеек
def check_empty(field): # Проверка ячеек поля. Если ячейка пустая, то её номер добавляется в список
    empty_cell.clear()
    for line in range(4):
        for column in range(4):
            if field[line][column] == 0:
                empty_cell.append(line*4+column+1)

def add_random_number_in_empty_cell(field): # Добавление 2 или 4 в рандомную свободную ячейку
    if len(empty_cell) > 0:
        number_cell = choice(empty_cell)
        number_cell-=1
        x, y = number_cell // 4, number_cell % 4
        generator = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        field[x][y] = choice(generator)
        check_empty(field)
    else:
        loss = True

# Игровое поле
field = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

#
def draw_field():
    pygame.draw.rect(screen, WHITE, title)
    sfont = pygame.font.SysFont('bahnschrift', 50)
    printing(field)
    for row in range(4):
        for column in range(4):
            value = field[row][column]
            text = font.render(f'{value}', True, colors['dark text'])
            x = column * 108 + (column + 1) * 10 + 35
            y = row * 108 + (row + 1) * 10 + 150 + 35
            pygame.draw.rect(screen, colors[value], (x, y, 108, 108))
            if value != 0:
                font_x, font_y = text.get_size()
                text_fir = x + (108 - font_x) / 2
                text_sec = y + (108 - font_y) / 2
                screen.blit(text, (text_fir, text_sec))

def move_right(field):
    for row in field:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if field[i][j] == field[i][j-1] and field[i][j] != 0:
                field[i][j]*=2
                field[i].pop(j-1)
                field[i].insert(0, 0)
    return field

def move_left(field):
    for row in field:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if field[i][j] == field[i][j+1] and field[i][j] != 0:
                field[i][j] *= 2
                field[i].pop(j+1)
                field[i].append(0)
    return field

def move_up(field):
    for j in range(4):
        column = []
        for i in range(4):
            if field[i][j] != 0:
                column.append(field[i][j])
        while len(column) != 4:
            column.append(0)
        for i in range(3):
            if column[i] == column [i+1] and column[i] != 0:
                column[i] *= 2
                column.pop(i+1)
                column.append(0)
        for i in range(4):
            field[i][j] = column[i]
    return field

def move_down(field):
    for j in range(4):
        column = []
        for i in range(4):
            if field[i][j] != 0:
                column.append(field[i][j])
        while len(column) != 4:
            column.insert(0, 0)
        for i in range(3, 0, -1):
            if column[i] == column[i - 1] and column[i] != 0:
                column[i] *= 2
                column.pop(i - 1)
                column.insert(0, 0)
        for i in range(4):
            field[i][j] = column[i]
    return field

#
def draw_objects():
    pass

# Игровой цикл
play = True
while play:
    timer.tick(fps)
    screen.fill((250,248,239))
    draw_field()
    draw_objects()
    pygame.draw.rect(screen, (250, 248, 239), title)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                field = move_right(field)
            elif event.key == pygame.K_LEFT:
                field = move_left(field)
            elif event.key == pygame.K_UP:
                field = move_up(field)
            elif event.key == pygame.K_DOWN:
                field = move_down(field)
            check_empty(field)
            if len(empty_cell) > 0:
                add_random_number_in_empty_cell(field)
                printing(field)
    pygame.display.update()
