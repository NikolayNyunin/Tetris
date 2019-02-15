import sys
import os
from random import choice

import pygame

FPS = 50
WIDTH, HEIGHT = 1200, 900
COLORS = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue'), pygame.Color('orange'),
          pygame.Color('yellow'), pygame.Color('purple'), (66, 170, 255), pygame.Color('black')]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.block, self.new = '', ''
        self.temp, self.coords = [], []
        self.color = 0
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for row in range(self.height):
            for col in range(self.width):
                x, y = col * self.cell_size + self.left, row * self.cell_size + self.top

                if (col, row) in self.coords:
                    pygame.draw.rect(screen, COLORS[self.color - 1],
                                     (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                else:
                    pygame.draw.rect(screen, COLORS[self.board[row][col] - 1],
                                     (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))

                pygame.draw.rect(screen, (30, 30, 30), (x, y, self.cell_size, self.cell_size), 1)

        bottom, right = self.top + self.height * self.cell_size, self.left + self.width * self.cell_size
        pygame.draw.lines(screen, pygame.Color('white'), False,
                          ((self.left - 1, self.top),
                           (self.left - 1, bottom),
                           (right, bottom),
                           (right, self.top)))

    def check_coords(self):
        for x, y in self.temp:
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                return False
            elif self.board[y][x] != 0:
                return False
        self.coords = self.temp.copy()
        return True

    def line1(self, x, y):
        self.temp = [(x - 1, y), (x, y), (x + 1, y), (x + 2, y)]
        self.color = 1
        self.new = 'line1'

    def line2(self, x, y):
        self.temp = [(x, y - 1), (x, y), (x, y + 1), (x, y + 2)]
        self.new = 'line2'

    def square(self, x, y):
        self.temp = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        self.color = 2
        self.new = 'square'

    def l1(self, x, y):
        self.temp = [(x, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)]
        self.color = 3
        self.new = 'l1'

    def l2(self, x, y):
        self.temp = [(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x + 2, y)]
        self.new = 'l2'

    def l3(self, x, y):
        self.temp = [(x, y), (x + 1, y), (x + 2, y), (x + 2, y + 1)]
        self.new = 'l3'

    def l4(self, x, y):
        self.temp = [(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x, y + 2)]
        self.new = 'l4'

    def r_l1(self, x, y):
        self.temp = [(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 2, y)]
        self.color = 4
        self.new = 'r_l1'

    def r_l2(self, x, y):
        self.temp = [(x + 1, y), (x + 1, y + 1), (x + 1, y + 2), (x + 2, y + 2)]
        self.new = 'r_l2'

    def r_l3(self, x, y):
        self.temp = [(x, y + 1), (x, y), (x + 1, y), (x + 2, y)]
        self.new = 'r_l3'

    def r_l4(self, x, y):
        self.temp = [(x, y), (x + 1, y), (x + 1, y + 1), (x + 1, y + 2)]
        self.new = 'r_l4'

    def z1(self, x, y):
        self.temp = [(x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 2, y)]
        self.color = 5
        self.new = 'z1'

    def z2(self, x, y):
        self.temp = [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y + 2)]
        self.new = 'z2'

    def r_z1(self, x, y):
        self.temp = [(x, y), (x + 1, y), (x + 1, y + 1), (x + 2, y + 1)]
        self.color = 6
        self.new = 'r_z1'

    def r_z2(self, x, y):
        self.temp = [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x, y + 2)]
        self.new = 'r_z2'

    def t1(self, x, y):
        self.temp = [(x, y + 1), (x + 1, y), (x + 1, y + 1), (x + 2, y + 1)]
        self.color = 7
        self.new = 't1'

    def t2(self, x, y):
        self.temp = [(x + 1, y), (x + 1, y + 1), (x + 2, y + 1), (x + 1, y + 2)]
        self.new = 't2'

    def t3(self, x, y):
        self.temp = [(x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 1, y + 2)]
        self.new = 't3'

    def t4(self, x, y):
        self.temp = [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x + 1, y + 2)]
        self.new = 't4'

    def add(self):
        for x, y in self.coords:
            self.board[y][x] = self.color

    def turn(self, x, y):
        if self.block == 'line1':
            self.line2(x, y)
        elif self.block == 'line2':
            self.line1(x, y)
        elif self.block == 'l1':
            self.l2(x, y)
        elif self.block == 'l2':
            self.l3(x, y)
        elif self.block == 'l3':
            self.l4(x, y)
        elif self.block == 'l4':
            self.l1(x, y)
        elif self.block == 'r_l1':
            self.r_l2(x, y)
        elif self.block == 'r_l2':
            self.r_l3(x, y)
        elif self.block == 'r_l3':
            self.r_l4(x, y)
        elif self.block == 'r_l4':
            self.r_l1(x, y)
        elif self.block == 'z1':
            self.z2(x, y)
        elif self.block == 'z2':
            self.z1(x, y)
        elif self.block == 'r_z1':
            self.r_z2(x, y)
        elif self.block == 'r_z2':
            self.r_z1(x, y)
        elif self.block == 't1':
            self.t2(x, y)
        elif self.block == 't2':
            self.t3(x, y)
        elif self.block == 't3':
            self.t4(x, y)
        elif self.block == 't4':
            self.t1(x, y)

    def perform(self, x, y):
        eval('self.{0}({1}, {2})'.format(self.block, x, y))

    def check_lines(self, score):
        for i in range(len(self.board)):
            if 0 not in self.board[i]:
                del self.board[i]
                self.board.insert(0, [0]*self.width)
                score += 10
        return score


def choose():
    block = choice(['line1', 'l1', 'r_l1', 'z1', 'r_z1', 'square', 't1'])
    return block


class NextBlock(Display):
    def render(self):
        super().render()
        pygame.draw.line(screen, pygame.Color('white'), (self.left - 1, self.top - 1),
                         (self.left + self.width * self.cell_size, self.top - 1))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    background = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 80)

    start_button = font.render('Начать игру', 1, pygame.Color('white'))
    start_button_rect = start_button.get_rect()
    start_button_rect.topleft = (80, 100)
    screen.blit(start_button, start_button_rect)

    quit_button = font.render('Выйти на рабочий стол', 1, pygame.Color('white'))
    quit_button_rect = quit_button.get_rect()
    quit_button_rect.topleft = (80, 240)
    screen.blit(quit_button, quit_button_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.MOUSEMOTION:
                screen.blit(background, (0, 0))

                if start_button_rect.collidepoint(event.pos):
                    start_button = font.render('Начать игру', 1, pygame.Color('purple'))
                else:
                    start_button = font.render('Начать игру', 1, pygame.Color('white'))
                if quit_button_rect.collidepoint(event.pos):
                    quit_button = font.render('Выйти на рабочий стол', 1, pygame.Color('purple'))
                else:
                    quit_button = font.render('Выйти на рабочий стол', 1, pygame.Color('white'))

                screen.blit(start_button, start_button_rect)
                screen.blit(quit_button, quit_button_rect)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return
                elif quit_button_rect.collidepoint(event.pos):
                    terminate()

        pygame.display.flip()
        clock.tick(FPS)


def game():
    background = pygame.transform.scale(load_image('background2.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    display = Display(10, 20)
    display.set_view(400, 50, 40)

    next_block = NextBlock(4, 2)
    next_block.set_view(80, 180, 60)

    font = pygame.font.Font(None, 50)
    next_block_lbl = font.render('Следующий блок:', 1, pygame.Color('white'), pygame.Color('black'))
    next_block_lbl_rect = next_block_lbl.get_rect()
    next_block_lbl_rect.topleft = (45, 100)
    screen.blit(next_block_lbl, next_block_lbl_rect)

    score_lbl = font.render('Счёт:', 1, pygame.Color('white'), pygame.Color('black'))
    score_lbl_rect = score_lbl.get_rect()
    score_lbl_rect.topleft = (900, 200)
    screen.blit(score_lbl, score_lbl_rect)

    score = 0
    score_view = font.render(str(score), 1, pygame.Color('white'), pygame.Color('black'))
    score_view_rect = score_view.get_rect()
    score_view_rect.topleft = (1050, 200)
    screen.blit(score_view, score_view_rect)

    with open('data/highscore.txt', mode='r+', encoding='utf-8') as file:
        data = file.read()
        try:
            high_score = int(data)
        except ValueError:
            high_score = 0
            file.write('0')

    high_score_lbl = font.render('Рекорд:', 1, pygame.Color('white'), pygame.Color('black'))
    high_score_lbl_rect = high_score_lbl.get_rect()
    high_score_lbl_rect.topleft = (900, 100)
    screen.blit(high_score_lbl, high_score_lbl_rect)

    high_score_view = font.render(str(high_score), 1, pygame.Color('white'), pygame.Color('black'))
    high_score_view_rect = high_score_view.get_rect()
    high_score_view_rect.topleft = (1100, 100)
    screen.blit(high_score_view, high_score_view_rect)

    pos_x, pos_y = 4, 0
    count = 0
    speed = 50

    next_block.block = choose()
    display.block = choose()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score >= high_score:
                    with open('data/highscore.txt', mode='w', encoding='utf-8') as file:
                        file.write(str(high_score))
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    display.turn(pos_x, pos_y)

                    if display.check_coords():
                        display.block = display.new

                elif event.key == pygame.K_LEFT:
                    display.perform(pos_x - 1, pos_y)

                    if display.check_coords():
                        pos_x -= 1

                elif event.key == pygame.K_RIGHT:
                    display.perform(pos_x + 1, pos_y)

                    if display.check_coords():
                        pos_x += 1

                elif event.key == pygame.K_DOWN:
                    if speed == 50:
                        speed = 5
                    else:
                        speed = 50
                    count = 0

        count += 1
        if count == speed:
            pos_y += 1
            count = 0

        screen.blit(background, (0, 0))

        display.perform(pos_x, pos_y + 1)
        if not display.check_coords():
            if (pos_x, pos_y) == (4, 0):
                return
            display.perform(pos_x, pos_y)
            display.check_coords()
            display.add()
            pos_x, pos_y = 4, 0
            display.block = next_block.block
            next_block.block = choose()
            speed = 50

        display.perform(pos_x, pos_y)
        display.check_coords()

        if display.board[0] != [0] * display.width:
            with open('data/highscore.txt', mode='w', encoding='utf-8') as file:
                file.write(str(high_score))
            return

        score = display.check_lines(score)
        if score > high_score:
            high_score = score
        score_view = font.render(str(score), 1, pygame.Color('white'), pygame.Color('black'))

        next_block.perform(1, 0)
        next_block.check_coords()

        display.render()
        next_block.render()

        high_score_view = font.render(str(high_score), 1, pygame.Color('white'), pygame.Color('black'))

        screen.blit(next_block_lbl, next_block_lbl_rect)
        screen.blit(score_lbl, score_lbl_rect)
        screen.blit(score_view, score_view_rect)
        screen.blit(high_score_lbl, high_score_lbl_rect)
        screen.blit(high_score_view, high_score_view_rect)

        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    print('GAME OVER')


def main():
    start_screen()

    while True:
        game()
        game_over()


if __name__ == '__main__':
    main()
