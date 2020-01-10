import pygame
from classes import Board, Checker

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 30

all_sprites = []
board = Board()

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(board.get_click(event.pos))
    screen.fill(pygame.Color('black'))
    board.render(screen)
    pygame.display.flip()


pygame.quit()