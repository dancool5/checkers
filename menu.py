import runpy

from tkinter.filedialog import askopenfilename
from tkinter import Tk

import pygame

from classes import Button
import functions
import settings as s

pygame.init()

old_width = s.width
old_height = s.height

size = (s.width, s.height)
screen = pygame.display.set_mode(size)

# корректировка размеров экрана в соответствии с картинкой заднего фона
screen_saver_im = functions.load_image('screen_saver1.png')
s.height = s.width * s.height // screen_saver_im.get_rect().size[0]
size = (s.width, s.height)
screen_saver = pygame.transform.scale(screen_saver_im, (s.width, s.height))
# screen_saver = screen_saver_im
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Checkers')
pygame.display.set_icon(pygame.transform.scale(functions.load_image('icon.ico'), (32, 32)))

buttons_sprites = pygame.sprite.Group()
buttons = []

if s.state == 'main_menu':
    button_new_game = Button(functions.load_image('button_newgame.png'), buttons_sprites)
    button_new_game.set_pos(s.width // 2 - button_new_game.rect.width // 2, s.height // 4)
    buttons.append(button_new_game)

    button_download = Button(functions.load_image('button_download.png'), buttons_sprites)
    button_download.set_pos(s.width // 2 - button_download.rect.width // 2, s.height // 2)
    buttons.append(button_download)

    button_exit = Button(functions.load_image('button_exit.png'), buttons_sprites)
    button_exit.set_pos(s.width // 2 - button_exit.rect.width // 2, s.height - button_exit.rect.height - s.height // 11)
    buttons.append(button_exit)

elif s.state == 'end_game':
    if s.player_color == s.winner:
        end_sound = pygame.mixer.Sound('data/Audio/winning.wav')
        end_sound.play()
    else:
        end_sound = pygame.mixer.Sound('data/Audio/losing.wav')
        end_sound.play()

    s.moving_color = 'white'
    if s.winner == 'white':
        str_winning = 'Белые выиграли!'
    elif s.winner == 'black':
        str_winning = 'Черные выиграли'
    font = pygame.font.Font(None, s.width // 7)
    text_winning = font.render(str_winning, 1, (255, 255, 255))

    button_again = Button(functions.load_image('button_again.png'), buttons_sprites)
    button_again.set_pos(s.width // 2 - button_again.rect.width // 2, s.height // 4)
    buttons.append(button_again)

    button_main_menu = Button(functions.load_image('button_main_menu.png'), buttons_sprites)
    button_main_menu.set_pos(s.width // 2 - button_main_menu.rect.width // 2, s.height // 2)
    buttons.append(button_main_menu)

    button_exit = Button(functions.load_image('button_exit.png'), buttons_sprites)
    button_exit.set_pos(s.width // 2 - button_exit.rect.width // 2, s.height - button_exit.rect.height - s.height // 11)
    buttons.append(button_exit)

    s.winner = None

running = True
while running:
    # отрисовка фона и текстов вопросов
    screen.fill(pygame.Color('black'))

    if s.state == 'main_menu':
        screen.blit(screen_saver, (0, 0))

    elif s.state == 'count_players':
        screen.blit(text_count_player, (s.width // 40, s.height // 5))

    elif s.state == 'choosing_color':
        screen.blit(text_choose_color, (s.width // 6, s.height // 5))

    elif s.state == 'end_game':
        screen.blit(text_winning, (s.width // 13, s.height // 10))

    buttons_sprites.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if s.state == 'main_menu':
                if button_download.is_pressed(event.pos):
                    Tk().withdraw()
                    try:
                        file_name = askopenfilename()
                        f = open(file_name)
                        s.arrangement = f.read()
                        f.close()
                        is_downloaded = True

                    except FileNotFoundError:
                        is_downloaded = False

                if button_new_game.is_pressed(event.pos) or (button_download.is_pressed(event.pos) and is_downloaded):
                    is_downloaded = False
                    s.state = 'count_players'
                    buttons = []
                    buttons_sprites = pygame.sprite.Group()

                    button_1player = Button(functions.load_image('button_1player.png'), buttons_sprites)
                    button_1player.set_pos((s.width // 2 - button_1player.rect.width) // 2, 2 * s.height // 3)
                    buttons.append(button_1player)

                    button_2player = Button(functions.load_image('button_2player.png'), buttons_sprites)
                    button_2player.set_pos((s.width // 2 - button_2player.rect.width) // 2 + s.width // 2,
                                           2 * s.height // 3)
                    buttons.append(button_2player)

                    font = pygame.font.Font(None, s.width // 11)
                    str_count_player = 'Выберите количество игроков'
                    text_count_player = font.render(str_count_player, 1, (255, 255, 255))

                    flag = False  # флаг для проверки нажатия на кнопки выбора количества игроков

                    pygame.time.wait(250)

                elif button_exit.is_pressed(event.pos):
                    running = False

            elif s.state == 'count_players':
                if button_1player.is_pressed(event.pos):
                    s.AI = True

                    count_player = 1
                    flag = True

                elif button_2player.is_pressed(event.pos):
                    s.AI = False

                    count_player = 2
                    flag = True

                if flag:
                    if count_player == 2:
                        s.player_color = None

                        buttons, buttons_sprites = functions.start_game(old_width, old_height)

                        pygame.time.wait(250)
                        runpy.run_module('game')
                        running = False

                    elif count_player == 1:
                        s.state = 'choosing_color'

                        buttons = []
                        buttons_sprites = pygame.sprite.Group()

                        button_white = Button(functions.load_image('button_white.png'), buttons_sprites)
                        button_white.set_pos((s.width // 2 - button_white.rect.width) // 2, 2 * s.height // 3)
                        buttons.append(button_white)

                        button_black = Button(functions.load_image('button_black.png'), buttons_sprites)
                        button_black.set_pos((s.width // 2 - button_black.rect.width) // 2 + s.width // 2,
                                             2 * s.height // 3)
                        buttons.append(button_black)

                        font = pygame.font.Font(None, s.width // 11)
                        str_choose_color = 'Выберите цвет шашек'
                        text_choose_color = font.render(str_choose_color, 1, (255, 255, 255))

            elif s.state == 'choosing_color':
                if button_white.is_pressed(event.pos):
                    s.player_color = 'white'
                elif button_black.is_pressed(event.pos):
                    s.player_color = 'black'

                buttons, buttons_sprites = functions.start_game(old_width, old_height)
                runpy.run_module('game')
                running = False

            elif s.state == 'end_game':
                if button_again.is_pressed(event.pos):
                    end_sound.set_volume(0)

                    buttons, buttons_sprites = functions.start_game(old_width, old_height)
                    runpy.run_module('game')
                    running = False

                elif button_main_menu.is_pressed(event.pos):
                    end_sound.set_volume(0)

                    s.state = 'main_menu'
                    s.arrangement = None

                    buttons_sprites = pygame.sprite.Group()
                    buttons = []

                    button_new_game = Button(functions.load_image('button_newgame.png'), buttons_sprites)
                    button_new_game.set_pos(s.width // 2 - button_new_game.rect.width // 2, s.height // 4)
                    buttons.append(button_new_game)

                    button_download = Button(functions.load_image('button_download.png'), buttons_sprites)
                    button_download.set_pos(s.width // 2 - button_download.rect.width // 2, s.height // 2)
                    buttons.append(button_download)

                    button_exit = Button(functions.load_image('button_exit.png'), buttons_sprites)
                    button_exit.set_pos(s.width // 2 - button_exit.rect.width // 2,
                                        s.height - button_exit.rect.height - s.height // 11)
                    buttons.append(button_exit)

                    pygame.time.wait(250)

                elif button_exit.is_pressed(event.pos):
                    end_sound.set_volume(0)

                    s.arrangement = None
                    running = False


pygame.quit()
