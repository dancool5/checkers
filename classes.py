import pygame


class Checker(pygame.sprite.Sprite):
    # b_checker = load_image('black_checker.png')
    # b_king = load_image('black_king.png')
    # w_checker = load_image('white_checker.png')
    # w_king = load_image('black_king.png')

    def __init__(self, x, y, color, all_sprites, image, left, top, cell_length, lines, rows):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites

        self.left, self.top = left, top
        self.cell_length = cell_length
        self.lines, self.rows = lines, rows

        self.color = color
        self.image = image

        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.is_king = False

    def make_move(self, pos):
        x, y = pos[0], pos[1]
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, *args):
        self.get_event(args[0])


class Board:
    def __init__(self, left, top, cell_length, lines, rows):
        self.left, self.top = left, top
        self.cell_length = cell_length
        self.lines, self.rows = lines, rows
        self.board = []

    def render(self, screen):
        for i in range(self.rows):
            for j in range(self.lines):
                self.render_cell(i, j, screen)

    def render_cell(self, row, col, screen):
        rect = (row * self.cell_length + self.left, col * self.cell_length + self.top,
                self.cell_length, self.cell_length)

        if row % 2 == 0:
            if col % 2 == 0:
                color_flag = False
            else:
                color_flag = True
        else:
            if col % 2 == 0:
                color_flag = True
            else:
                color_flag = False
        pygame.draw.rect(screen, (255, 255, 255), rect, color_flag)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x = (x - self.left) // self.cell_length
        y = (y - self.top) // self.cell_length
        if 0 <= x < self.rows and 0 <= y < self.lines:
            return (x, y)

    def get_click(self, mouse_pos):
        return self.get_cell(mouse_pos)

