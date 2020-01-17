import pygame

import functions


class Button(pygame.sprite.Sprite):
    def __init__(self, image):
        self.image, functions.load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def is_pressed(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


pygame.init()
width, height = 800, 800
left, right, bottom, top = 10, 10, 10, 10  # границы рамки
lines, cols = 8, 8
# корректировка размеров экрана
if left > top:
    cell_length = (width - left - right) // lines
    height = cell_length * cols + top + bottom
else:
    cell_length = (width - top - bottom) // lines
    width = cell_length * lines + left + right
pygame.display.set_caption('Checkers')
size = (width, height)
screen = pygame.display.set_mode(size)
image = functions.load_image('screen_saver.png')
image.set_alpha(0)
height = int(width / image.get_rect().size[0] * height)
size = (width, height)
image = pygame.transform.scale(image, (width, height))
screen = pygame.display.set_mode(size)
grey_background = pygame.Surface(size, pygame.SRCALPHA)
GREY = (0, 0, 0, 50)
pygame.draw.rect(grey_background, GREY, grey_background.get_rect())

button_new_game = pygame.Rect(2 * width // 3.5, 5 * height // 6, width - 2 * width // 3.5 - width // 50,
                     height - 5 * height // 6 - height // 50)
str_new_game = 'Новая игра'
font = pygame.font.Font(None, int(width / 10))
text_new_game = font.render(str_new_game, 1, (0, 0, 0))

button_two_players = pygame.Rect(2 * width // 3.5, 5 * height // 6, width - 2 * width // 3.5 - width // 50,
                     height - 5 * height // 6 - height // 50)
str_two_players = '2 игрока'
font = pygame.font.Font(None, int(width / 10))
text_two_players = font.render(str_two_players, 1, (0, 0, 0))

pygame.display.set_icon(pygame.transform.scale(functions.load_image('icon.ico'), (32, 32)))
running = True

state = 'main_menu'

while running:
    if state == 'main_menu':
        # отрисовка фона
        screen.fill(pygame.Color('white'))
        screen.blit(image, (0, 0))
        screen.blit(grey_background, (0, 0))
        # отрисовка кнопки 'Новая игра' (рамки)
        pygame.draw.rect(screen, [255, 255, 255], button_new_game, 4)
        # отрисовка кнопки 'Новая игра' (текста)
        screen.blit(text_new_game, (2 * width // 3.5 + width // 75, 5 * height // 6 + height // 35))

    elif state == 'count_players':
        screen.fill(pygame.Color('grey'))
        pygame.draw.rect(screen, [255, 255, 255], button_two_players, 4)
        screen.blit(text_two_players, (2 * width // 3.5 + width // 75, 5 * height // 6 + height // 35))
        pass

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if state == 'main_menu':
                if button_new_game.collidepoint(event.pos):
                    state = 'count_players'
                    pygame.time.wait(250)
            elif state == 'count_players':
                pygame.time.wait(250)
                pass


pygame.quit()
