import runpy

import pygame
from classes import Board, Checker
import functions
import settings as s

pygame.init()

old_width = s.width
old_height = s.height

# корректировка размеров экрана
if s.left > s.top:
    cell_length = (s.width - s.left - s.right) // s.lines
    s.height = cell_length * s.cols + s.top + s.bottom
else:
    cell_length = (s.width - s.top - s.bottom) // s.lines
    s.width = cell_length * s.lines + s.left + s.right

size = (s.width, s.height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Checkers')
pygame.display.set_icon(pygame.transform.scale(functions.load_image('icon.ico'), (32, 32)))

im_w_ch = pygame.transform.scale(functions.load_image('white_checker.png'), (cell_length, cell_length))
im_w_k = pygame.transform.scale(functions.load_image('white_king.png'), (cell_length, cell_length))
im_b_ch = pygame.transform.scale(functions.load_image('black_checker.png'), (cell_length, cell_length))
im_b_k = pygame.transform.scale(functions.load_image('black_king.png'), (cell_length, cell_length))

all_sprites = pygame.sprite.Group()
board = Board(s.left, s.top, cell_length, s.lines, s.cols)

# добавление шашек на доску
for line in range(s.lines - 3, s.lines):
    for col in range((line + 1) % 2, 8, 2):
        checker = Checker(col, line, 'white', all_sprites, im_w_ch, s.left, s.top,
                          cell_length, s.lines, s.cols)
        board.board.append(checker)

for line in range(0, 3):
    for col in range((line + 1) % 2, 8, 2):
        checker = Checker(col, line, 'black', all_sprites, im_b_ch, s.left, s.top,
                          cell_length, s.lines, s.cols)
        board.board.append(checker)

if s.player_color == 'black':
    board.rotate()
selected_checker = None

font = pygame.font.Font(None, (s.left - s.left // 20) // 5)

FPS = 30
clock = pygame.time.Clock()
running = True

while running:
    black_ch = [checker for checker in board.board if checker.color == 'black']
    white_ch = [checker for checker in board.board if checker.color == 'white']

    screen.fill(pygame.Color('black'))
    board.render(screen, selected_checker)
    all_sprites.draw(screen)

    str_turn = 'Ход: черных' if s.moving_color == 'black' else 'Ход: белых'
    text_turn = font.render(str_turn, 1, (255, 255, 255))
    screen.blit(text_turn, (s.left // 20, s.top))

    str_white_count = functions.declination(white_ch, 'белые')
    text_white_count = font.render(str_white_count, 1, (255, 255, 255))
    screen.blit(text_white_count, (s.left // 20, s.height - 2 * (s.left - s.left // 20) // 5))

    str_black_count = functions.declination(black_ch, 'черные')
    text_black_count = font.render(str_black_count, 1, (255, 255, 255))
    screen.blit(text_black_count, (s.left // 20, s.height - (s.left - s.left // 20) // 5))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            x, y = board.get_cell(event.pos)
            other_checker = functions.select(x, y, board.board, s.moving_color, event.pos)

            if type(other_checker) == Checker:
                # если шашка правильного цвета, то выделение перемещается на нее
                selected_checker = other_checker
            elif other_checker is None and selected_checker is not None and x is not None:
                # если выделена клетка без шашки
                moving_ch = [ch for ch in board.board if ch.color == s.moving_color]
                not_moving_ch = [ch for ch in board.board if ch.color != s.moving_color]

                if functions.is_killing_possible(moving_ch, not_moving_ch, board.board):
                    # если есть ходы c рубкой
                    killed_checker = functions.find_killed_checker(selected_checker,
                                                                   board.board, x, y, not_moving_ch)
                    if functions.can_kill(selected_checker, killed_checker, board.board, x, y, True):
                        # если данная рубка возможна
                        board.board.remove(killed_checker)
                        all_sprites.remove(killed_checker)
                        flag_king = selected_checker.make_move(x, y, board.is_rotate)

                        if flag_king:
                            functions.change_status(selected_checker, [im_w_k, im_b_k])

                        not_moving_ch = [ch for ch in board.board if ch.color != s.moving_color]
                        if not(functions.is_killing_possible([selected_checker], not_moving_ch, board.board)):
                            # если повторная рубка невозможна, то меняем ход
                            s.moving_color = 'black' if s.moving_color == 'white' else 'white'
                            # board.rotate()
                            selected_checker = None

                elif functions.can_move(selected_checker, x, y, s.moving_color, board):
                    # если рубка невозможна, но возможен ход
                    flag_king = selected_checker.make_move(x, y, board.is_rotate)

                    if flag_king:
                        functions.change_status(selected_checker, [im_w_k, im_b_k])

                    selected_checker = None
                    s.moving_color = 'black' if s.moving_color == 'white' else 'white'
                    # board.rotate()

    # проверка на конец игры
    s.winner = functions.check_winning(black_ch, white_ch)
    if s.winner:
        running = False
        s.state = 'end_game'
        s.width, s.height = old_width, old_height
        pygame.time.wait(250)
        runpy.run_module('menu')

    clock.tick(FPS)

pygame.quit()
