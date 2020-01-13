import pygame
from classes import Board, Checker
import functions


pygame.init()

width, height = 800, 800
left, right, bottom, top = 200, 10, 10, 10  # границы рамки
lines, cols = 8, 8
# корректировка размеров экрана
if left > top:
    cell_length = (width - left - right) // lines
    height = cell_length * cols + top + bottom
else:
    cell_length = (width - top - bottom) // lines
    width = cell_length * lines + left + right

size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Checkers')
pygame.display.set_icon(pygame.transform.scale(functions.load_image('icon.ico'), (32, 32)))

FPS = 30
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, (left - left // 20) // 5)

all_sprites = pygame.sprite.Group()
board = Board(left, top, cell_length, lines, cols)

im_w_ch = pygame.transform.scale(functions.load_image('white_checker.png'), (cell_length, cell_length))
im_w_k = pygame.transform.scale(functions.load_image('white_king.png'), (cell_length, cell_length))
im_b_ch = pygame.transform.scale(functions.load_image('black_checker.png'), (cell_length, cell_length))
im_b_k = pygame.transform.scale(functions.load_image('black_king.png'), (cell_length, cell_length))

# добавление шашек на доску
for line in range(lines - 3, lines):
    for col in range((line + 1) % 2, 8, 2):
        checker = Checker(col, line, 'white', all_sprites, im_w_ch, left, top,
                          cell_length, lines, cols)
        board.board.append(checker)

for line in range(0, 3):
    for col in range((line + 1) % 2, 8, 2):
        checker = Checker(col, line, 'black', all_sprites, im_b_ch, left, top,
                          cell_length, lines, cols)
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
                    if functions.can_kill(selected_checker, killed_checker, board.board, x, y, True):
                        # если данная рубка возможна
                        board.board.remove(killed_checker)
                        all_sprites.remove(killed_checker)
                        flag_king = selected_checker.make_move(x, y, board.is_rotate)

                        if flag_king:
                            functions.change_status(selected_checker, [im_w_k, im_b_k])

                        not_moving_ch = [ch for ch in board.board if ch.color != moving_color]
                        if not(functions.is_killing_possible([selected_checker], not_moving_ch, board.board)):
                            # если повторная рубка невозможна, то меняем ход
                            moving_color = 'black' if moving_color == 'white' else 'white'
                            # board.rotate()
                            selected_checker = None

                elif functions.can_move(selected_checker, x, y, moving_color, board):
                    # если рубка невозможна, но возможен ход
                    flag_king = selected_checker.make_move(x, y, board.is_rotate)

                    if flag_king:
                        functions.change_status(selected_checker, [im_w_k, im_b_k])

                    selected_checker = None
                    moving_color = 'black' if moving_color == 'white' else 'white'
                    # board.rotate()

    # проверка на конец игры
    win_text, black_ch, white_ch = functions.check_winning(board.board)
    if win_text:
        running = False
        print(win_text)

    clock.tick(FPS)

    screen.fill(pygame.Color('black'))
    board.render(screen, selected_checker)
    all_sprites.draw(screen)

    str_turn = 'Ход: черных' if moving_color == 'black' else 'Ход: белых'
    text_turn = font.render(str_turn, 1, (255, 255, 255))
    screen.blit(text_turn, (left // 20, top))

    srt_white_count = str(len(white_ch)) + ' б шашек'
    text_white_count = font.render(srt_white_count, 1, (255, 255, 255))
    screen.blit(text_white_count, (left // 20, height - 2 * (left - left // 20) // 5))

    str_black_count = str(len(black_ch)) + ' ч шашек'
    text_black_count = font.render(str_black_count, 1, (255, 255, 255))
    screen.blit(text_black_count, (left // 20, height - (left - left // 20) // 5))

    pygame.display.flip()

pygame.quit()
