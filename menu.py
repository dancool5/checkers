import pygame

import functions

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

button = pygame.Rect(2 * width // 3.5, 5 * height // 6, width - 2 * width // 3.5 - width // 50,
                     height - 5 * height // 6 - height // 50)

str_black_count = 'Новая игра'
font = pygame.font.Font(None, int(width / 10))
text_black_count = font.render(str_black_count, 1, (0, 0, 0))

pygame.display.set_icon(pygame.transform.scale(functions.load_image('icon.ico'), (32, 32)))
FPS = 30
clock = pygame.time.Clock()
running = True

while running:
    # отрисовка фона
    screen.fill(pygame.Color('white'))
    screen.blit(image, (0, 0))
    screen.blit(grey_background, (0, 0))
    # отрисовка кнопки (рамки)
    pygame.draw.rect(screen, [255, 255, 255], button, 4)
    # отрисовка кнопки (текста)
    screen.blit(text_black_count, (2 * width // 3.5 + width // 75, 5 * height // 6 + height // 35))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if button.collidepoint(event.pos):
                pygame.time.wait(250)
                running = False
                import main


pygame.quit()
