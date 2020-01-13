import pygame


class Checker(pygame.sprite.Sprite):
    def __init__(self, x, y, color, all_sprites, image, left, top, cell_length, lines, cols):
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

        self.is_king = False

    def make_move(self, x, y, is_rotate):
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x = self.left + self.cell_length * self.x
        self.rect.y = self.top + self.cell_length * self.y
        if is_rotate:
            if (self.color == 'white' and self.y == 7) or (self.y == 0 and self.color == 'black'):
                return True
            elif (self.color == 'white' and self.y == 0) or (self.y == 7 and self.color == 'black'):
                return True

        return False

    def update(self, *args):
        self.get_event(args[0])


class Board:
    def __init__(self, left, top, cell_length, lines, cols):
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
        for checker in self.board:
            checker.make_move(self.lines - checker.x - 1, self.cols - checker.y - 1, True)

        self.is_rotate = not self.is_rotate
