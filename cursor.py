import pygame

class Cursor:
    def __init__(self, start_pos, color):
        self.pos = list(start_pos)
        self.color = color

    def move(self, dx, dy, rows, cols):
        new_row = self.pos[0] + dy
        new_col = self.pos[1] + dx
        if 0 <= new_row < rows and 0 <= new_col < cols:
            self.pos = [new_row, new_col]

    def draw(self, screen, margin_x, margin_y, cell_size):
        x = margin_x + self.pos[1] * cell_size
        y = margin_y + self.pos[0] * cell_size
        pygame.draw.circle(screen, self.color, (x, y), 27, 4)