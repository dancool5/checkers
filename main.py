import pygame
from os import path
from classes import Board, Checker
import functions


def load_image(name):
    fullname = path.join('data', name)
    im = pygame.image.load(fullname).convert_alpha()
    return im


pygame.init()
width, height = 532, 532
size = (width, height)
screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()
running = True

left, top = 10, 10  # границы рамки
cell_length = (width - left * 2) // 8
lines, rows = 8, 8

all_sprites = pygame.sprite.Group()
board = Board(left, top, cell_length, lines, rows)

# добавление шашек на доску
for row in range(5, 8):
    for col in range((row + 1) % 2, 8, 2):
        image = pygame.transform.scale(load_image('white_checker.png'), (cell_length, cell_length))
        checker = Checker(col, row, 'white', all_sprites, image, left, top,
                          cell_length, lines, rows)
        board.board.append(checker)

for row in range(0, 3):
    for col in range((row + 1) % 2, 8, 2):
        image = pygame.transform.scale(load_image('black_checker.png'), (cell_length, cell_length))
        checker = Checker(col, row, 'black', all_sprites, image, left, top,
                          cell_length, lines, rows)
        board.board.append(checker)


moving_color = 'white'
selected_checker = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if selected_checker is None:
                for elem in board.board:
                    if elem.rect.collidepoint(event.pos):
                        if elem.color == moving_color:
                            selected_checker = elem
            else:
                x, y = board.get_cell(event.pos)
                if (x + y) % 2:
                    moving_checkers = [checker for checker in board.board if checker.color == moving_color]
                    not_moving_checkers = [checker for checker in board.board if checker.color != moving_color]
                    if functions.can_move(selected_checker, x, y, moving_checkers, not_moving_checkers):
                        selected_checker.make_move((x, y))
                        selected_checker = None
                        moving_color = 'white' if moving_color == 'black' else 'black'

    clock.tick(FPS)

    screen.fill(pygame.Color('black'))
    board.render(screen)
    all_sprites.draw(screen)
    pygame.display.flip()


pygame.quit()
print(board.board)