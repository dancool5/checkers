import pygame
from classes import Board, Checker
import functions


pygame.init()
pygame.display.set_caption('Checkers')
width, height = 1024, 10424
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_icon(pygame.transform.scale(functions.load_image('icon.ico'), (32, 32)))
FPS = 30
clock = pygame.time.Clock()
running = True

left, top = 10, 10  # границы рамки
cell_length = (width - left * 2) // 8
lines, rows = 8, 8

all_sprites = pygame.sprite.Group()
board = Board(left, top, cell_length, lines, rows)

im_w_ch = pygame.transform.scale(functions.load_image('white_checker.png'), (cell_length, cell_length))
im_w_k = pygame.transform.scale(functions.load_image('white_king.png'), (cell_length, cell_length))
im_b_ch = pygame.transform.scale(functions.load_image('black_checker.png'), (cell_length, cell_length))
im_b_k = pygame.transform.scale(functions.load_image('black_king.png'), (cell_length, cell_length))

# добавление шашек на доску
for row in range(5, 8):
    for col in range((row + 1) % 2, 8, 2):
        checker = Checker(col, row, 'white', all_sprites, im_w_ch, left, top,
                          cell_length, lines, rows)
        board.board.append(checker)

for row in range(0, 3):
    for col in range((row + 1) % 2, 8, 2):
        checker = Checker(col, row, 'black', all_sprites, im_b_ch, left, top,
                          cell_length, lines, rows)
        board.board.append(checker)

moving_color = 'white'
selected_checker = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if selected_checker is None:  # если выбранной клетки еще нет
                selected_checker = functions.select(event.pos, board.board, moving_color)

            else:  # если выбранная клетка есть
                x, y = board.get_cell(event.pos)
                other_checker = functions.sel_other(x, y, board.board, moving_color, event.pos)

                if other_checker == 'false_color':  # если шашка не того цвета, то выделение сбрасывается
                    selected_checker = None
                elif other_checker:  # если шашка правильного цвета, то выделение перемещается на нее
                    selected_checker = other_checker
                else:  # если выделена клетка без шашки
                    moving_ch = [ch for ch in board.board if ch.color == moving_color]
                    not_moving_ch = [ch for ch in board.board if ch.color != moving_color]

                    if functions.is_killing_possible(moving_ch, not_moving_ch, board.board):  # если есть ходы с рубкой
                        killed_checker = functions.find_killed_checker(selected_checker, board.board, x, y,
                                                                       not_moving_ch)

                        if functions.can_kill(selected_checker, killed_checker, board.board, x, y):  # если даная рубка
                            board.board.remove(killed_checker)                                       # возможна
                            flag_king = selected_checker.make_move(x, y)

                            if flag_king:
                                functions.change_status(selected_checker, [im_w_k, im_b_k])

                            not_moving_ch = [ch for ch in board.board if ch.color != moving_color]
                            if not(functions.is_killing_possible([selected_checker], not_moving_ch, board.board)):
                                moving_color = 'black' if moving_color == 'white' else 'white'  # если повторная рубка
                                selected_checker = None                                      # невозможна, то меняем ход

                    elif functions.can_move(selected_checker, x, y, moving_color, board.board):  # если рубка невозможна
                        flag_king = selected_checker.make_move(x, y)                             # но возможен ход

                        if flag_king:
                            functions.change_status(selected_checker, [im_w_k, im_b_k])

                        selected_checker = None
                        moving_color = 'black' if moving_color == 'white' else 'white'

    win_text = functions.check_winning(board.board)  # проверка на конец игры
    if win_text:
        running = False
        print(win_text)

    clock.tick(FPS)

    screen.fill(pygame.Color('black'))
    board.render(screen, selected_checker)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
