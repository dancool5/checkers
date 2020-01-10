import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 30


class Board:
    def __init__(self):
        self.width, self.height = 8, 8
        self.board = [[(i + j) % 2 for j in range(self.width)]
                      for i in range(self.height)]
        self.cell_size = 50
        self.left = 15
        self.top = 15

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                self.render_cell(i, j)

    def render_cell(self, row, col):
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
    board.render()
    pygame.display.flip()


pygame.quit()