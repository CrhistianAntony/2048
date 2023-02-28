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

title = pygame.Rect(25, 25, 250, 75)

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

def before_start(field):
    empty = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    number_cell = choice(empty)
    number_cell -= 1
    x, y = number_cell // 4, number_cell % 4
    generator = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
    field[x][y] = choice(generator)
    check_empty(field)

# Игровое поле
field = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

score = 0

before_start(field)
before_start(field)

# Отрисовка поля
def draw_field():
    pygame.draw.rect(screen, WHITE, title)
    font = pygame.font.SysFont('bahnschrift', 50)
    printing(field)
    for row in range(4):
        for column in range(4):
            value = field[row][column]
            if value > 4:
                color = colors['light text']
            else:
                color = colors['dark text']
            text = font.render(f'{value}', True, color)
            x = column * 108 + (column + 1) * 10 + 35
            y = row * 108 + (row + 1) * 10 + 150 + 35
            pygame.draw.rect(screen, colors[value], (x, y, 108, 108))
            if value != 0:
                font_x, font_y = text.get_size()
                text_fir = x + (108 - font_x) / 2
                text_sec = y + (108 - font_y) / 2
                screen.blit(text, (text_fir, text_sec))

def move_right(field):
    add_score = 0
    for row in field:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if field[i][j] == field[i][j-1] and field[i][j] != 0:
                field[i][j]*=2
                add_score += field[i][j]
                field[i].pop(j-1)
                field[i].insert(0, 0)
    return field, add_score

def move_left(field):
    add_score = 0
    for row in field:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if field[i][j] == field[i][j+1] and field[i][j] != 0:
                field[i][j] *= 2
                add_score += field[i][j]
                field[i].pop(j+1)
                field[i].append(0)
    return field, add_score

def move_up(field):
    add_score = 0
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
                add_score += field[i][j]
                column.pop(i+1)
                column.append(0)
        for i in range(4):
            field[i][j] = column[i]
    return field, add_score

def move_down(field):
    add_score = 0
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
                add_score += field[i][j]
                column.pop(i - 1)
                column.insert(0, 0)
        for i in range(4):
            field[i][j] = column[i]
    return field, add_score

# Проигрыш
def game_loss():
    font = pygame.font.SysFont('bahnschrift', 75)
    loss = font.render('Ты проиграл!', True, (0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        screen.fill(colors['bg'])
        screen.blit(loss, (60, 75))
        sfont = pygame.font.SysFont('bahnschrift', 35)
        textscore = sfont.render('Очки:', True, (0, 0, 0))
        score_value = sfont.render(f'{score}', True, (0, 0, 0))
        screen.blit(textscore, (220, 175))
        screen.blit(score_value, (225, 217))
        pygame.display.update()

def movetrue(field):
    for x in range(3):
        for y in range(3):
            if field[x][y] == field[x][y+1] or field[x][y] == field[x+1][y]:
                return True
    return field[3][3] == field[2][3] or field[3][3] == field[3][2]

# Игровой цикл
while len(empty_cell) > 0 or movetrue(field):
    timer.tick(fps)
    screen.fill((250,248,239))
    pygame.draw.rect(screen, colors['bg'], [25, 175, 500, 500], 0, 7)
    draw_field()
    pygame.draw.rect(screen, colors['bg'], title, 0, 17)
    font = pygame.font.SysFont('bahnschrift', 35)
    textscore = font.render('Очки: ', True, colors['light text'])
    score_value = font.render(f'{score}', True, colors['light text'])
    screen.blit(textscore, (35, 45))
    screen.blit(score_value, (130, 47))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            add_score = 0
            if event.key == pygame.K_RIGHT:
                field, add_score = move_right(field)
            elif event.key == pygame.K_LEFT:
                field, add_score = move_left(field)
            elif event.key == pygame.K_UP:
                field, add_score = move_up(field)
            elif event.key == pygame.K_DOWN:
                field, add_score = move_down(field)
            score += add_score
            check_empty(field)
            if len(empty_cell) > 0:
                add_random_number_in_empty_cell(field)
                printing(field)
    pygame.display.update()
game_loss()
