import pygame


class Checker(pygame.sprite.Sprite):
    def __init__(self, x, y, color, color_group, all_sprites):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        self.add(color_group)
        self.x = x
        self.y = y
        self.color = color
        self.is_king = False

    def move(self, x, y):
        self.x, self.y = x, y

    def delete(self, color_group):
        self.all_sprites.remove(self)
        color_group.remove(self)


class Board:
    def __init__(self):
        self.width, self.height = 8, 8
        self.board = [[(i + j) % 2 for j in range(self.width)]
                      for i in range(self.height)]
        self.cell_size = 50
        self.left = 15
        self.top = 15

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                self.render_cell(i, j, screen)

    def render_cell(self, row, col, screen):
        rect = (row * self.cell_size + self.left, col * self.cell_size + self.top, self.cell_size, self.cell_size)
        cc = False if self.board[row][col] else True
        pygame.draw.rect(screen, (255, 255, 255), rect, cc)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x = (x - self.left) // self.cell_size
        y = (y - self.top) // self.cell_size
        if 0 <= x < self.height and 0 <= y < self.width:
            return (x, y)

    def get_click(self, mouse_pos):
        return self.get_cell(mouse_pos)

