import runpy
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import functions
import settings as s
from classes import *

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

im_w_ch_k1 = pygame.transform.scale(functions.load_image('white_ch-k1.png'), (cell_length, cell_length))
im_w_ch_k2 = pygame.transform.scale(functions.load_image('white_ch-k2.png'), (cell_length, cell_length))
im_w_ch_k3 = pygame.transform.scale(functions.load_image('white_ch-k3.png'), (cell_length, cell_length))

im_w_k = pygame.transform.scale(functions.load_image('white_king.png'), (cell_length, cell_length))

im_b_ch = pygame.transform.scale(functions.load_image('black_checker.png'), (cell_length, cell_length))

im_b_ch_k1 = pygame.transform.scale(functions.load_image('black_ch-k1.png'), (cell_length, cell_length))
im_b_ch_k2 = pygame.transform.scale(functions.load_image('black_ch-k2.png'), (cell_length, cell_length))
im_b_ch_k3 = pygame.transform.scale(functions.load_image('black_ch-k3.png'), (cell_length, cell_length))

im_b_k = pygame.transform.scale(functions.load_image('black_king.png'), (cell_length, cell_length))

all_sprites = pygame.sprite.Group()
buttons_sprites = pygame.sprite.Group()
board = Board(cell_length)

# добавление шашек на доску
if s.arrangement:
    # по загруженному файлу
    line, col = 0, 0
    if s.arrangement[0] == 'w':
        s.moving_color = 'white'
    elif s.arrangement[0] == 'b':
        s.moving_color = 'black'
    for char in s.arrangement[2:]:
        if line < s.lines and col < s.cols and line % 2 != col % 2:
            if char.lower() == 'w':
                checker = Checker(col, line, 'white', all_sprites, im_w_ch, cell_length)
                board.board.append(checker)
                if char == 'W' or line == 0:
                    functions.change_status(checker, [im_w_k, im_b_k])

            elif char.lower() == 'b':
                checker = Checker(col, line, 'black', all_sprites, im_b_ch, cell_length)
                board.board.append(checker)
                if char == 'B' or line == s.lines - 1:
                    functions.change_status(checker, [im_w_k, im_b_k])

        if char != '\n':
            col += 1
        if col == s.cols:
            col = 0
            line += 1
else:
    # по стандарту
    for line in range(s.lines - 3, s.lines):
        for col in range((line + 1) % 2, 8, 2):
            checker = Checker(col, line, 'white', all_sprites, im_w_ch, cell_length)
            board.board.append(checker)

    for line in range(0, 3):
        for col in range((line + 1) % 2, 8, 2):
            checker = Checker(col, line, 'black', all_sprites, im_b_ch, cell_length)
            board.board.append(checker)

if s.player_color == 'black':
    board.rotate()
selected_checker = None

font = pygame.font.Font(None, (s.left - s.left // 20) // 5)

# кнопки, текст и фон для паузы
font_pause = pygame.font.Font(None, s.width // 5)
str_pause = 'Пауза'
text_pause = font_pause.render(str_pause, 1, (255, 255, 255))

BLACK = (0, 0, 0, 128)
black_background = pygame.Surface(size, pygame.SRCALPHA)
pygame.draw.rect(black_background, BLACK, black_background.get_rect(), 0)

button_continue = Button(functions.load_image('button_continue.png'), buttons_sprites)
button_continue.set_pos(s.width // 2 - button_continue.rect.width // 2, s.height // 4)

button_save = Button(functions.load_image('button_save.png'), buttons_sprites)
button_save.set_pos(s.width // 2 - button_save.rect.width // 2, s.height // 2)

button_main_menu = Button(functions.load_image('button_main_menu.png'), buttons_sprites)
button_main_menu.set_pos(s.width // 2 - button_main_menu.rect.width // 2,
                         s.height - button_main_menu.rect.height - s.height // 11)

FPS = 30
clock = pygame.time.Clock()

is_paused = False
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

    if is_paused:
        screen.blit(black_background, (0, 0))
        buttons_sprites.draw(screen)
        screen.blit(text_pause, (s.width // 2 - text_pause.get_rect().width // 2, s.height // 20))

    pygame.display.flip()

    if s.AI and player_color != s.moving_color:  # ход AI
        old_moving_color = s.moving_color
        new_board = Board(cell_length)
        new_board.board = board.board.copy()

        move = functions.AI_turn(new_board, 6)

        s.moving_color = old_moving_color
        s.moving_color = 'black' if s.moving_color == 'white' else 'white'
        print(move)

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if is_paused:
                    if button_continue.is_pressed(event.pos):
                        is_paused = False

                    elif button_save.is_pressed(event.pos):
                        Tk().withdraw()
                        try:
                            file_name = askopenfilename()
                            f = open(file_name, 'w')

                            move_col = 'w' if s.moving_color == 'white' else 'b'
                            f.write(move_col + '\n')

                            arr = [['0' for col in range(s.cols)] for line in range(s.lines)]

                            if board.is_rotate:
                                board.rotate()
                                was_rotated = True
                            else:
                                was_rotated = False

                            for checker in board.board:
                                if checker.color == 'white':
                                    char = 'w'
                                elif checker.color == 'black':
                                    char = 'b'
                                if checker.is_king:
                                    char = char.upper()
                                arr[checker.y][checker.x] = char

                            for line in range(s.lines):
                                f.write(''.join(arr[line]) + '\n')

                            if was_rotated:
                                board.rotate()

                            f.close()

                        except FileNotFoundError:
                            pass

                    elif button_main_menu.is_pressed(event.pos):
                        s.state = 'main_menu'
                        running = False
                        s.width, s.height = old_width, old_height
                        s.moving_color = 'white'
                        pygame.time.wait(250)

                        runpy.run_module('menu')

                else:
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
                                win_sound = pygame.mixer.Sound('data/Audio/killing.wav')
                                win_sound.play()

                                board.board.remove(killed_checker)
                                all_sprites.remove(killed_checker)
                                flag_king = selected_checker.make_move(x, y, board.is_rotate)

                                if flag_king:
                                    functions.change_status(selected_checker,
                                                            [[im_w_ch_k1, im_w_ch_k2, im_b_ch_k3, im_w_k],
                                                             [im_b_ch_k1, im_b_ch_k2, im_b_ch_k3, im_b_k]])

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
                                functions.change_status(selected_checker,
                                                        [[im_w_ch_k1, im_w_ch_k2, im_b_ch_k3, im_w_k],
                                                         [im_b_ch_k1, im_b_ch_k2, im_b_ch_k3, im_b_k]])

                            selected_checker = None
                            s.moving_color = 'black' if s.moving_color == 'white' else 'white'
                            # board.rotate()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                click_sound = pygame.mixer.Sound('data/Audio/click.wav')
                click_sound.play()

                is_paused = not is_paused

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
