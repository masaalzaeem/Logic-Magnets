import pygame

class Grid:
    def __init__(self, rows, cols, cell_size, target_positions, screen_width, screen_height):
            self.rows = rows
            self.cols = cols
            self.cell_size = cell_size
            self.target_positions = target_positions

            self.margin_x = (screen_width - (cols * cell_size)) // 2 + 40
            self.margin_y = (screen_height - (rows * cell_size)) // 2 + 40

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.margin_x + col * self.cell_size
                y = self.margin_y + row * self.cell_size
                pygame.draw.circle(screen, (55, 235, 250), (x, y), 33)

                if (row, col) in self.target_positions:
                    pygame.draw.circle(screen, (255, 255, 255), (x, y), 15, 3)