import pygame
import functions


pygame.init()
pygame.display.set_caption('Checkers')
width, height = 766, 450
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_icon(pygame.transform.scale(functions.load_image('icon.ico'), (32, 32)))
FPS = 30
clock = pygame.time.Clock()
running = True
image = pygame.transform.scale(functions.load_image('screen_saver.jpg'), (width, height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            pass
    screen.fill(pygame.Color('black'))
    screen.blit(image, (0, 0))
    pygame.display.flip()

pygame.quit()
