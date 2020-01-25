import pygame
from settings import *


class Checker(pygame.sprite.Sprite):
    def __init__(self, x, y, color, all_sprites, image, cell_length):
        super().__init__(all_sprites)

        self.left, self.top = left, top
        self.cell_length = cell_length
        self.lines, self.cols = lines, cols

        self.color = color
        self.image = image

        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x = left + x * cell_length
        self.rect.y = top + y * cell_length

        self.is_update = False

        self.is_king = False

    def make_move(self, x, y, is_rotate, is_play_sound=True):
        if is_play_sound:
            move_sound = pygame.mixer.Sound('data/Audio/moving.wav')
            move_sound.play()

        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x = self.left + self.cell_length * self.x
        self.rect.y = self.top + self.cell_length * self.y
        if is_rotate:
            if (self.color == 'white' and self.y == lines - 1) or (self.y == 0 and self.color == 'black'):
                return True
        else:
            if (self.color == 'white' and self.y == 0) or (self.y == lines - 1 and self.color == 'black'):
                return True

        return False

    def update(self):
        if self.is_update:
            if self.color == 'white':
                self.image = self.images[0][self.num_image]
            else:
                self.image = self.images[1][self.num_image]

            self.rect = self.image.get_rect()
            self.rect.x = left + self.x * self.cell_length
            self.rect.y = top + self.y * self.cell_length
            self.num_image += 1
            if self.num_image > 3:
                self.is_update = False

    def change_status(self, images):
        self.is_update = True
        self.is_king = True
        self.images = images
        self.num_image = 0


class Board:
    def __init__(self, cell_length):
        self.left, self.top = left, top
        self.cell_length = cell_length
        self.lines, self.cols = lines, cols
        self.board = []

        self.is_rotate = False

    def render(self, screen, selected_checker):
        for i in range(self.cols):
            for j in range(self.lines):
                self.render_cell(i, j, screen, selected_checker)

    def render_cell(self, line, col, screen, selected_checker):
        rect = (col * self.cell_length + self.left, line * self.cell_length + self.top,
                self.cell_length, self.cell_length)
        color = None
        if selected_checker:
            if selected_checker.rect == rect:
                color = (255, 0, 0)
                color_flag = False
        if not color:
            if line % 2 == 0:
                if col % 2 == 0:
                    color_flag = False
                else:
                    color_flag = True
                color = (255, 255, 255)
            else:
                if col % 2 == 0:
                    color_flag = True
                else:
                    color_flag = False
                color = (255, 255, 255)
        pygame.draw.rect(screen, color, rect, color_flag)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x = (x - self.left) // self.cell_length
        y = (y - self.top) // self.cell_length
        if 0 <= x <= self.cols and 0 <= y <= self.lines:
            return x, y
        return None, None

    def rotate(self):
        images = []
        for checker in self.board:
            images.append(checker.image)
            checker.image = None

        pygame.time.wait(250)

        for checker in self.board:
            checker.image = images[0]
            del images[0]
            checker.make_move(self.lines - checker.x - 1, self.cols - checker.y - 1, True, False)

        self.is_rotate = not self.is_rotate


class Button(pygame.sprite.Sprite):
    def __init__(self, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def is_pressed(self, pos):
        if self.rect.collidepoint(pos):
            click_sound = pygame.mixer.Sound('data/Audio/click.wav')
            click_sound.play()

            return True
        return False
