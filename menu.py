import pygame
from classes import Button
import functions
from settings import *

pygame.init()

old_width = width
old_height = height

size = (width, height)
screen = pygame.display.set_mode(size)

# корректировка размеров экрана в соответствии с картинкой заднего фона
screen_saver = functions.load_image('screen_saver.png')
height = int(width / screen_saver.get_rect().size[0] * height)
size = (width, height)
image = pygame.transform.scale(screen_saver, (width, height))
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Checkers')
pygame.display.set_icon(pygame.transform.scale(functions.load_image('icon.ico'), (32, 32)))

buttons_sprites = pygame.sprite.Group()
buttons = []

button_new_game = Button(functions.load_image('button_newgame.png'), buttons_sprites)
button_new_game.set_pos(3 * width // 5, 5 * height // 6)
buttons.append(button_new_game)

running = True

while running:
    # отрисовка фона и текстов вопросов
    screen.fill(pygame.Color('black'))

    if state == 'main_menu':
        screen.blit(image, (0, 0))

    elif state == 'count_players':
        screen.blit(text_count_player, (width // 40, height // 5))

    buttons_sprites.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if state == 'main_menu':
                if button_new_game.is_pressed(event.pos):
                    state = 'count_players'
                    buttons.remove(button_new_game)
                    buttons_sprites.remove(button_new_game)

                    button_1player = Button(functions.load_image('button_1player.png'), buttons_sprites)
                    button_1player.set_pos((width // 2 - button_1player.rect.width) // 2, 2 * height // 3)
                    buttons.append(button_1player)

                    button_2player = Button(functions.load_image('button_2player.png'), buttons_sprites)
                    button_2player.set_pos((width // 2 - button_2player.rect.width) // 2 + width // 2, 2 * height // 3)
                    buttons.append(button_2player)

                    font = pygame.font.Font(None, width // 11)
                    str_count_player = 'Выберите количество игроков'
                    text_count_player = font.render(str_count_player, 1, (255, 255, 255))

                    flag = False  # флаг для проверки нажатия на кнопки выбора количества игроков

                    pygame.time.wait(250)
            elif state == 'count_players':
                if button_1player.is_pressed(event.pos):
                    count_player = 1
                    flag = True
                elif button_2player.is_pressed(event.pos):
                    count_player = 2
                    flag = True

                if flag:
                    if count_player == 2:
                        state = 'game'

                        width = old_width
                        height = old_height

                        pygame.time.wait(250)
                        import main
                        running = False
                    elif count_player == 1:
                        state = ''
                pass


pygame.quit()
