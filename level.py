import pygame

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.instructions_font = pygame.font.Font(None, 24)  # Smaller font for instructions
        self.levels = list(range(1, 31))
        self.button_size = 50

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, level in enumerate(self.levels):
                level_x = 100 + (i % 5) * (self.button_size + 10) + 90  # Position in a row
                level_y = 150 + (i // 5) * (self.button_size + 10) - 50 # Position in a column
                if level_x < mouse_x < level_x + self.button_size and level_y < mouse_y < level_y + self.button_size:
                    return level
        return None

    def draw_instructions(self):
        # Define instructions text
        instructions = [
            "Controls:",
            "Mouse Click: Select a level",
            "Arrow Keys - Move cursor",
            "Enter - Select / Move magnet",
            "Shift + R - Reset level",
            "Backspace - Return to level selection",
            "to deselect a magnet, press Enter again!"
        ]

        # Display each line of instructions
        for i, text in enumerate(instructions):
            instruction_surface = self.instructions_font.render(text, True, (255, 255, 255))
            self.screen.blit(instruction_surface, (50, 465 + i * 30))  # Adjust Y position for each line

    def draw(self):
        # Fill the screen background
        self.screen.fill((75, 75, 75))
        
        # Draw title text
        title_text = self.font.render("Select a Level", True, (255, 255, 255))
        self.screen.blit(title_text, (250, 50))

        # Draw level buttons in a grid
        for i, level in enumerate(self.levels):
            button_x = 100 + (i % 5) * (self.button_size + 10) + 90  # Position in a row
            button_y = 150 + (i // 5) * (self.button_size + 10) - 50 # Position in a column
            pygame.draw.rect(self.screen, (0, 128, 128), (button_x, button_y, self.button_size, self.button_size))  # Button
            level_text = self.font.render(str(level), True, (255, 255, 255))  # Level number
            text_rect = level_text.get_rect(center=(button_x + self.button_size // 2, button_y + self.button_size // 2))  # Center text
            self.screen.blit(level_text, text_rect)  # Draw level number

        # Draw instructions
        self.draw_instructions()  # Call the new method to render instructions

    def get_level_properties(self, level):
        """Return level properties based on the selected level."""
        if level == 1:
            grid_size = (3, 4)
            grays = [(1, 2)]
            reds = []
            purples = [(2, 0)]
            target_positions = [(1, 1), (1, 3)]
            moves_allowed = 2
        elif level == 2:
            grid_size = (5, 5)
            grays = [(1, 2), (2, 1), (2, 3), (3, 2)]
            reds = []
            purples = [(4, 0)]
            target_positions = [(0, 2), (2, 0), (2, 2), (2, 4), (4, 2)]
            moves_allowed = 4
        elif level == 3:
            grid_size = (3, 4)
            grays = [(1, 2)]
            reds = []
            purples = [(2, 0)]
            target_positions = [(0, 3), (2, 3)]
            moves_allowed = 2
        elif level == 4:
            grid_size = (5, 3)
            grays = [(1, 1), (3, 1)]
            reds = []
            purples = [(0, 2)]
            target_positions = [(0, 0), (0, 2), (4, 1)]
            moves_allowed = 2
        elif level == 5:
            grid_size = (4, 3)
            grays = [(1, 0), (1, 2), (2, 0), (2, 2)]
            reds = []
            purples = [(3, 1)]
            target_positions = [(0, 0), (0, 2), (1, 0), (1, 2), (3, 0)]
            moves_allowed = 2
        elif level == 6:
            grid_size = (3, 5)
            grays = [(1, 1), (1, 3)]
            reds = []
            purples = [(2, 0)]
            target_positions = [(0, 3), (1, 2), (2, 3)]
            moves_allowed = 2
        elif level == 7:
            grid_size = (5, 4)
            grays = [(1, 0), (2, 0), (3, 1), (3, 2)]
            reds = []
            purples = [(2, 1)]
            target_positions = [(0, 0), (1, 0), (2, 3), (3, 2), (4, 3)]
            moves_allowed = 2
        elif level == 8:
            grid_size = (3, 4)
            grays = [(1, 1), (1, 2)]
            reds = []
            purples = [(2, 0)]
            target_positions = [(0, 0), (0, 2), (2, 2)]
            moves_allowed = 2
        elif level == 9:
            grid_size = (1, 7)
            grays = [(0, 5), (0, 3)]
            reds = []
            purples = [(0, 0)]
            target_positions = [(0, 1), (0, 3), (0, 6)]
            moves_allowed = 4
        elif level == 10:
            grid_size = (4, 4)
            grays = [(3, 1), (2, 2), (2, 3)]
            reds = []
            purples = [(0, 0)]
            target_positions = [(1, 1), (1, 3), (3, 0), (3, 3)]
            moves_allowed = 2
        elif level == 11:
            grid_size = (2, 5)
            grays = [(0, 0), (0, 4)]
            reds = [(1, 2)]
            purples = []
            target_positions = [(0, 1), (0, 2), (0, 3)]
            moves_allowed = 1
        elif level == 12:
            grid_size = (5, 4)
            grays = [(0, 0), (1, 0), (4, 3)]
            reds = [(3, 1)]
            purples = []
            target_positions = [(1, 0), (2, 0), (4, 0), (4, 2)]
            moves_allowed = 1
        elif level == 13:
            grid_size = (3, 6)
            grays = [(0, 0), (0, 3), (0, 4)]
            reds = [(2, 3)]
            purples = []
            target_positions = [(0, 3), (0, 4), (1, 1),(2, 1)]
            moves_allowed = 3
        elif level == 14:
            grid_size = (4, 4)
            grays = [(0, 3), (3, 0), (2, 0)]
            reds = [(3, 3)]
            purples = []
            target_positions = [(1, 0), (1, 2), (2, 1), (2, 2)]
            moves_allowed = 2
        elif level == 15:
            grid_size = (3, 5)
            grays = [(0, 1), (0, 3)]
            reds = [(2, 2)]
            purples = [(1, 2)]
            target_positions = [(0, 0), (0, 2), (1, 4), (2, 4)]
            moves_allowed = 2
        elif level == 16:
            grid_size = (5, 5)
            grays = [(1, 2), (3, 2)]
            reds = [(2, 0)]
            purples = [(2, 4)]
            target_positions = [(0, 3), (0, 4), (4, 0), (4, 3)]
            moves_allowed = 3
        elif level == 17:
            grid_size = (4, 4)
            grays = [(0, 2), (2, 0)]
            reds = [(0, 0)]
            purples = [(3, 3)]
            target_positions = [(1, 1), (1, 3), (2, 2), (3, 1)]
            moves_allowed = 2
        elif level == 18:
            grid_size = (5, 6)
            grays = [(2, 0), (0, 3), (2, 5)]
            reds = [(4, 2)]
            purples = [(4, 3)]
            target_positions = [(2, 1), (2, 2), (2, 3), (2, 5), (1, 3)]
            moves_allowed = 2
        elif level == 19:
            grid_size = (5, 5)
            grays = [(0, 1), (0, 3), (4, 1), (4, 3)]
            reds = [(2, 2)]
            purples = [(0, 2)]
            target_positions = [(1, 0), (3, 0), (1, 4), (2, 1), (3, 2), (3, 4)]
            moves_allowed = 4
        elif level == 20:
            grid_size = (5, 4)
            grays = [(0, 1), (0, 2), (4, 0)]
            reds = [(4, 3)]
            purples = [(4, 2)]
            target_positions = [(0, 1), (0, 3), (1, 0), (2, 0), (3, 0)]
            moves_allowed = 2
        elif level == 21:
            grid_size = (3, 4)
            grays = [(0, 1), (1, 1), (1, 2)]
            reds = [(2, 3)]
            purples = [(2, 0)]
            target_positions = [(0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
            moves_allowed = 2
        elif level == 22:
            grid_size = (4, 5)
            grays = [(0, 4), (0, 3), (3, 0)]
            reds = [(3, 2)]
            purples = [(0, 0)]
            target_positions = [(0, 1), (0, 3), (1, 0), (1, 4), (2, 1)]
            moves_allowed = 3
        elif level == 23:
            grid_size = (4, 5)
            grays = [(0, 3), (1, 4), (2, 0)]
            reds = [(3, 2)]
            purples = [(3, 4)]
            target_positions = [(0, 2), (2, 1), (2, 2), (2, 3), (3, 2)]
            moves_allowed = 3
        elif level == 24:
            grid_size = (5, 5)
            grays = [(0, 1), (1, 3), (3, 3)]
            reds = [(3, 0)]
            purples = [(1, 4)]
            target_positions = [(0, 4), (2, 1), (2, 3), (4, 1), (4, 2)]
            moves_allowed = 3
        elif level == 25:
            grid_size = (5, 4)
            grays = [(0, 0), (1, 2), (3, 2), (4, 3)]
            reds = [(0, 3)]
            purples = [(4, 0)]
            target_positions = [(0, 0), (0, 3), (2, 0), (4, 0), (4, 1), (4, 2)]
            moves_allowed = 3
        elif level == 26:
            grid_size = (4, 5)
            grays = [(1, 1), (2, 3)]
            reds = [(3, 0)]
            purples = [(1, 0)]
            target_positions = [(0, 0), (3, 0), (3, 2), (3, 3)]
            moves_allowed = 3
        elif level == 27:
            grid_size = (4, 6)
            grays = [(0, 4), (2, 1), (2, 4), (3, 4)]
            reds = [(2, 3), (3, 3)]
            purples = [(2, 3)]
            target_positions = [(0, 1), (0, 2), (0, 3), (0, 5), (1, 1), (1, 4), (2, 4)]
            moves_allowed = 3
        elif level == 28:
            grid_size = (6, 3)
            grays = [(0, 1), (4, 1), (5, 1)]
            reds = [(3, 0)]
            purples = [(2, 2)]
            target_positions = [(1, 0), (1, 2), (2, 1), (4, 1), (5, 0)]
            moves_allowed = 3
        elif level == 29:
            grid_size = (4, 7)
            grays = [(0, 3), (1, 1), (2, 5), (3, 2)]
            reds = [(1, 3), (3, 5)]
            purples = [(3, 1)]
            target_positions = [(0, 4), (0, 5), (1, 0), (1, 1), (1, 3), (1, 5), (2, 2)]
            moves_allowed = 3
        elif level == 30:
            grid_size = (6, 5)
            grays = [(0, 2), (3, 4), (4, 2)]
            reds = [(3, 0)]
            purples = [(5, 2)]
            target_positions = [(1, 1), (1, 3), (2, 2), (3, 3), (4, 1)]
            moves_allowed = 3
        else:
            return None, None, None, None, None, None

        return grid_size, grays, reds, purples, target_positions, moves_allowed, level
