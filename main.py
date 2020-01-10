import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 30

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color('black'))
    pygame.display.flip()


pygame.quit()