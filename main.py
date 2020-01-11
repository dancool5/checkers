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
                selected_checker = functions.select(event.pos, board.board, moving_color)
            else:
                x, y = board.get_cell(event.pos)
                if x is not None:
                    for ch in board.board:
                        if ch.x == x and ch.y == y:
                            if ch.color == moving_color:
                                selected_checker = functions.select(event.pos, board.board, moving_color)
                                break
                            else:
                                break
                    else:
                        moving_ch = [ch for ch in board.board if ch.color == moving_color]
                        not_moving_ch = [ch for ch in board.board if ch.color != moving_color]
                        if functions.is_killing_possible(moving_ch, not_moving_ch, board.board):
                            for ch in not_moving_ch:
                                if (abs(x - ch.x) == 1 and abs(ch.y - y) == 1 and
                                        abs(selected_checker.x - ch.x) == 1 and abs(ch.y - selected_checker.y) == 1):
                                    killed_checker = ch
                                    break
                            else:
                                killed_checker = selected_checker
                            if functions.can_kill(selected_checker, killed_checker, board.board):
                                print(killed_checker)
                                all_sprites.remove(killed_checker)
                                board.board.remove(killed_checker)
                                selected_checker.make_move(x, y)
                                not_moving_ch = [ch for ch in board.board if ch.color != moving_color]
                                if not(functions.is_killing_possible([selected_checker], not_moving_ch, board.board)):
                                    moving_color = 'black' if moving_color == 'white' else 'white'
                                    selected_checker = None
                                else:
                                    print(1)
                        elif functions.can_move(selected_checker, x, y, moving_color):
                            selected_checker.make_move(x, y)
                            selected_checker = None
                            moving_color = 'black' if moving_color == 'white' else 'white'

    win_text = functions.check_winning(board.board)
    if win_text:
        running = False
        print(win_text)

    clock.tick(FPS)

    screen.fill(pygame.Color('black'))
    board.render(screen, selected_checker)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
