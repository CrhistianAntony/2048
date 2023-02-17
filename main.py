import pygame
from random import *

pygame.init()
width = 550
height = 700
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('bahnschrift', 36)

# Цвета
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
    pygame.draw.rect(screen, colors['bg'], [25, 175, 500, 500], 0, 7)
    pass

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    pygame.display.update()
pygame.quit()
