import pygame
from classes import Board, Checker
import functions


pygame.init()
pygame.display.set_caption('Checkers')
width, height = 1024, 1024
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
            x, y = board.get_cell(event.pos)
            other_checker = functions.select(x, y, board.board, moving_color, event.pos)

            if type(other_checker) == Checker:
                # если шашка правильного цвета, то выделение перемещается на нее
                selected_checker = other_checker
            elif other_checker is None and selected_checker is not None and x is not None:
                # если выделена клетка без шашки
                moving_ch = [ch for ch in board.board if ch.color == moving_color]
                not_moving_ch = [ch for ch in board.board if ch.color != moving_color]

                if functions.is_killing_possible(moving_ch, not_moving_ch, board.board):
                    # если есть ходы c рубкой
                    killed_checker = functions.find_killed_checker(selected_checker,
                                                                   board.board, x, y, not_moving_ch)
                    print(functions.find_killed_checker(selected_checker, board.board, x, y, not_moving_ch))
                    print(functions.can_kill(selected_checker, killed_checker, board.board, x, y, True))
                    if functions.can_kill(selected_checker, killed_checker, board.board, x, y, True):
                        # если данная рубка возможна
                        print(2)
                        board.board.remove(killed_checker)
                        all_sprites.remove(killed_checker)
                        flag_king = selected_checker.make_move(x, y)

                        if flag_king:
                            functions.change_status(selected_checker, [im_w_k, im_b_k])

                        not_moving_ch = [ch for ch in board.board if ch.color != moving_color]
                        if not(functions.is_killing_possible([selected_checker], not_moving_ch, board.board)):
                            # если повторная рубка невозможна, то меняем ход
                            moving_color = 'black' if moving_color == 'white' else 'white'
                            selected_checker = None

                elif functions.can_move(selected_checker, x, y, moving_color, board.board):
                    # если рубка невозможна, но возможен ход
                    flag_king = selected_checker.make_move(x, y)

                    if flag_king:
                        functions.change_status(selected_checker, [im_w_k, im_b_k])

                    selected_checker = None
                    moving_color = 'black' if moving_color == 'white' else 'white'

    # проверка на конец игры
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
