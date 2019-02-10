import sys
import os

import pygame

FPS = 50
WIDTH, HEIGHT = 800, 800
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

                pygame.draw.rect(screen, COLORS[self.board[row][col] - 1],
                                 (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))

                pygame.draw.rect(screen, (30, 30, 30), (x, y, self.cell_size, self.cell_size), 1)

        bottom, right = self.top + self.height * self.cell_size, self.left + self.width * self.cell_size
        pygame.draw.lines(screen, pygame.Color('white'), False,
                          ((self.left - 1, self.top),
                           (self.left - 1, bottom),
                           (right, bottom),
                           (right, self.top)))

    def line(self, x, y):
        pass

    def square(self, x, y):
        pass


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
    font = pygame.font.Font(None, 60)

    start_button = font.render('Начать игру', 1, pygame.Color('white'))
    start_button_rect = start_button.get_rect()
    start_button_rect.topleft = (80, 100)
    screen.blit(start_button, start_button_rect)

    quit_button = font.render('Выйти на рабочий стол', 1, pygame.Color('white'))
    quit_button_rect = quit_button.get_rect()
    quit_button_rect.topleft = (80, 200)
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
    background = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    display = Display(10, 20)
    display.set_view(100, 100, 30)

    next_block = NextBlock(4, 2)
    next_block.set_view(500, 350, 50)

    font = pygame.font.Font(None, 40)
    next_block_lbl = font.render('Следующий блок:', 1, pygame.Color('white'), pygame.Color('black'))
    next_block_lbl_rect = next_block_lbl.get_rect()
    next_block_lbl_rect.topleft = (470, 300)
    screen.blit(next_block_lbl, next_block_lbl_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass

        screen.blit(background, (0, 0))
        display.render()
        next_block.render()
        screen.blit(next_block_lbl, next_block_lbl_rect)
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    pass


def main():
    start_screen()

    while True:
        game()
        game_over()


if __name__ == '__main__':
    main()
