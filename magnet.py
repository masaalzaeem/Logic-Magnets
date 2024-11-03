import pygame

class Magnet:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def draw(self, screen, margin_x, margin_y, cell_size, selected):
        x = margin_x + self.pos[1] * cell_size - self.image.get_width() // 2
        y = margin_y + self.pos[0] * cell_size - self.image.get_height() // 2
        screen.blit(self.color, (x, y))
