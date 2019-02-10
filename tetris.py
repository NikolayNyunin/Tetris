import sys
import os

import pygame

FPS = 50
WIDTH, HEIGHT = 1280, 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


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
    font = pygame.font.Font(None, 70)

    start_button = font.render('Начать игру', 1, pygame.Color('white'))
    start_button_rect = start_button.get_rect()
    start_button_rect.topleft = (100, 100)
    screen.blit(start_button, start_button_rect)

    quit_button = font.render('Выйти на рабочий стол', 1, pygame.Color('white'))
    quit_button_rect = quit_button.get_rect()
    quit_button_rect.topleft = (100, 200)
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
        clock.tick(50)


def game_over():
    pass


def main():
    start_screen()


if __name__ == '__main__':
    main()
