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

all_sprites = pygame.sprite.Group()
board = Board(width)

# добавление шашек на доску
for row in range(5, 8):
    for col in range((row + 1) % 2, 8, 2):
        image = pygame.transform.scale(load_image('white_checker.png'), (board.cell_length, board.cell_length))
        checker = Checker(board.left + col * board.cell_length, board.top + row * board.cell_length, 'white', all_sprites, image)
        board.board.append(checker)

for row in range(0, 3):
    for col in range((row + 1) % 2, 8, 2):
        image = pygame.transform.scale(load_image('black_checker.png'), (board.cell_length, board.cell_length))
        checker = Checker(board.left + col * board.cell_length, board.top + row * board.cell_length, 'black', all_sprites, image)
        board.board.append(checker)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(board.get_click(event.pos))

    clock.tick(FPS)

    screen.fill(pygame.Color('black'))
    board.render(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
print(board.board)