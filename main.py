import pygame
from os import path
from classes import Board, Checker


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
        image = pygame.transform.average_color(image, (0, 0, 0, 0))
        checker = Checker(left + col * cell_length, top + row * cell_length, 'white', all_sprites, image, left, top,
                          cell_length, lines, rows)
        board.board.append(checker)

for row in range(0, 3):
    for col in range((row + 1) % 2, 8, 2):
        image = pygame.transform.scale(load_image('black_checker.png'), (cell_length, cell_length))
        checker = Checker(left + col * cell_length, top + row * cell_length, 'black', all_sprites, image, left, top,
                          cell_length, lines, rows)
        board.board.append(checker)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(board.get_click(event.pos))
            all_sprites.update(event)

    clock.tick(FPS)

    screen.fill(pygame.Color('black'))
    board.render(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
print(board.board)