import pygame
from grid import Grid
from magnet import Magnet
from cursor import Cursor
from level import Level

class Game:
    def __init__(self, screen, grid_size, grays, reds, purples, target_positions, moves_allowed, level_number):
        self.screen = screen
        self.grid_size = grid_size
        screen_width, screen_height = screen.get_width(), screen.get_height()
        self.level_number = level_number

        self.grid = Grid(grid_size[0], grid_size[1], 90, target_positions, screen_width, screen_height)
        
        self.grays = [Magnet(pos, None) for pos in grays]
        self.reds = [Magnet(pos, None) for pos in reds]
        self.purples = [Magnet(pos, None) for pos in purples]

        self.target_positions = target_positions
        self.moves_allowed = moves_allowed
        self.remaining_moves = moves_allowed

        self.cursor = Cursor((0, 0), (100, 100, 100))
        self.selected_magnet = None
        self.selected_magnet_type = None

        self.game_over = False

    def reset_with_level(self, level_number):
        grid_size, grays, reds, purples, target_positions, moves_allowed, level_number = Level.get_level_properties(self, level_number)
        
        self.grid_size = grid_size
        self.grays = grays
        self.reds = reds
        self.purples = purples
        self.target_positions = target_positions
        self.moves_allowed = moves_allowed
        self.remaining_moves = moves_allowed

    def draw(self):
        self.screen.fill((0, 128, 128))
        
        if self.game_over:
            self.display_game_over()
            return

        self.grid.draw(self.screen)

        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {self.level_number}", True, (50, 50, 50))
        self.screen.blit(level_text, (10, 10))

        for gray in self.grays:
            self.draw_circle(gray.pos, (50, 50, 50), 25)
        for red in self.reds:
            self.draw_circle(red.pos, (150, 0, 0), 25)
        for purple in self.purples:
            self.draw_circle(purple.pos, (90, 0, 90), 25)

        for target in self.target_positions:
            self.draw_circle(target, (255, 255, 255), 6)
            self.draw_circle(target, (255, 255, 255), 13, 2)

        if self.selected_magnet:
            self.draw_circle(self.selected_magnet.pos, (255, 255, 255), 32, 5)
        
        self.cursor.draw(self.screen, self.grid.margin_x, self.grid.margin_y, self.grid.cell_size)
        self.draw_remaining_moves()

    # Draw a circle, centered within the grid cell
    def draw_circle(self, pos, color, radius, width=0):

        x = self.grid.margin_x + pos[1] * self.grid.cell_size
        y = self.grid.margin_y + pos[0] * self.grid.cell_size
        pygame.draw.circle(self.screen, color, (int(x), int(y)), radius, width)

    def draw_remaining_moves(self):
        dot_radius = 5
        dot_spacing = 15
        start_x, start_y = 320, 20

        font = pygame.font.Font(None, 36)
        moves_text = font.render("Moves:", True, (255, 255, 255))

        self.screen.blit(moves_text, (start_x - moves_text.get_width() - 10, start_y - moves_text.get_height() // 2))

        for i in range(self.remaining_moves):
            x = start_x + i * dot_spacing
            pygame.draw.circle(self.screen, (255, 255, 255), (x, start_y), dot_radius)

    def handle_event(self, event):
        self.update_cursor_color()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return True

            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                dx, dy = {
                    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0),
                    pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)
                }[event.key]
                self.cursor.move(dx, dy, self.grid.rows, self.grid.cols)

            elif event.key == pygame.K_RETURN:
                if self.selected_magnet:
                    if tuple(self.cursor.pos) == self.selected_magnet.pos:
                        self.selected_magnet = None
                        self.selected_magnet_type = None
                    else:
                        if not self.is_position_occupied(tuple(self.cursor.pos)) and self.is_within_bounds(tuple(self.cursor.pos)):
                            self.selected_magnet.pos = tuple(self.cursor.pos)

                            if self.selected_magnet_type == "red":
                                self.pull_magnets()
                            elif self.selected_magnet_type == "purple":
                                self.push_magnets()

                            self.selected_magnet = None
                            self.selected_magnet_type = None
                            self.remaining_moves = max(0, self.remaining_moves - 1)

                            if self.check_win_condition():
                                print("Congratulations! You've solved the game!")
                            elif self.remaining_moves == 0:
                                self.game_over = True
                        else:
                            print("Cannot move magnet here; position is occupied.")
                else:
                    self.selected_magnet, self.selected_magnet_type = self.get_magnet_at_position(self.cursor.pos)

        return False

    def is_position_occupied(self, pos):
        for magnet in self.grays + self.reds + self.purples:
            if magnet.pos == tuple(pos):
                return True
        return False

    def check_win_condition(self):
        occupied_positions = {magnet.pos for magnet in self.grays + self.reds + self.purples}
        target_set = set(self.target_positions)

        if occupied_positions == target_set and self.remaining_moves >= 0:
            return True
        return False

    def display_win_screen(self):
        font = pygame.font.Font(None, 80)
        text = font.render("WINNER!", True, (0, 210, 210))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        darker_color = (0, 150, 150)
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    self.screen.blit(font.render("WINNER!", True, darker_color), text_rect.move(dx, dy))

        white_color = (255, 255, 255)
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    self.screen.blit(font.render("WINNER!", True, white_color), text_rect.move(dx, dy))

        self.screen.blit(text, text_rect)

    def display_game_over(self):
        font = pygame.font.Font(None, 45)
        text = font.render("MOVES_OUT_OF_BOUND_EXCEPTION", True, (255, 0, 0))
        game_over_text = font.render("GAME OVER :(", True, (0, 155, 255))
    
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.screen.blit(text, text_rect)
        self.screen.blit(game_over_text, game_over_rect)

    def update_cursor_color(self):
        magnet, magnet_type = self.get_magnet_at_position(self.cursor.pos)
        if magnet_type == "red":
            self.cursor.color = (255, 100, 0)
        elif magnet_type == "purple":
            self.cursor.color = (200, 0, 200)
        else:
            self.cursor.color = (100, 100, 100)

    def get_magnet_at_position(self, pos):
        for magnet in self.reds:
            if magnet.pos == tuple(pos):
                return magnet, "red"
        for magnet in self.purples:
            if magnet.pos == tuple(pos):
                return magnet, "purple"
        return None, None

    def pull_magnets(self):
        for red in self.reds:
            row_magnets_left = sorted(
                [magnet for magnet in self.grays + self.purples if magnet.pos[0] == red.pos[0] and magnet.pos[1] < red.pos[1]],
                key=lambda m: abs(m.pos[1] - red.pos[1]), reverse=True
            )
            row_magnets_right = sorted(
                [magnet for magnet in self.grays + self.purples if magnet.pos[0] == red.pos[0] and magnet.pos[1] > red.pos[1]],
                key=lambda m: abs(m.pos[1] - red.pos[1])
            )
            self.pull_line_magnets(red, row_magnets_left, axis=1, direction="left")
            self.pull_line_magnets(red, row_magnets_right, axis=1, direction="right")

            col_magnets_up = sorted(
                [magnet for magnet in self.grays + self.purples if magnet.pos[1] == red.pos[1] and magnet.pos[0] < red.pos[0]],
                key=lambda m: abs(m.pos[0] - red.pos[0]), reverse=True
            )
            col_magnets_down = sorted(
                [magnet for magnet in self.grays + self.purples if magnet.pos[1] == red.pos[1] and magnet.pos[0] > red.pos[0]],
                key=lambda m: abs(m.pos[0] - red.pos[0])
            )
            self.pull_line_magnets(red, col_magnets_up, axis=0, direction="up")
            self.pull_line_magnets(red, col_magnets_down, axis=0, direction="down")

    def pull_line_magnets(self, red, magnets, axis, direction):
        if not magnets:
            return

        for magnet in magnets:
            if self.is_space_between(red, magnet, axis):
                self.move_magnet_towards(red, magnet)
            else:
                break

    def is_space_between(self, red, magnet, axis):
        start, end = (red.pos[axis], magnet.pos[axis])
        if start > end:
            start, end = end, start

        for pos in range(start + 1, end):
            check_pos = (magnet.pos[0], pos) if axis == 1 else (pos, magnet.pos[1])
            if not self.is_position_occupied(check_pos):
                return True
        return False

    def move_magnet_towards(self, red, magnet):
        if magnet.pos[0] < red.pos[0]:
            magnet.pos = (magnet.pos[0] + 1, magnet.pos[1])
        elif magnet.pos[0] > red.pos[0]:
            magnet.pos = (magnet.pos[0] - 1, magnet.pos[1])
        elif magnet.pos[1] < red.pos[1]:
            magnet.pos = (magnet.pos[0], magnet.pos[1] + 1)
        elif magnet.pos[1] > red.pos[1]:
            magnet.pos = (magnet.pos[0], magnet.pos[1] - 1)
            
    def get_closest_magnet(self, red, magnets):

        if not magnets:
            return None

        magnets.sort(key=lambda m: abs(m.pos[0] - red.pos[0]) + abs(m.pos[1] - red.pos[1]))
        return magnets[0]

    def push_magnets(self):
        for purple in self.purples:
            for direction in ["left", "right", "up", "down"]:
                adjacent_magnets = self.get_adjacent_magnets(purple, direction)
                if adjacent_magnets:
                    self.push_magnets_according_to_rules(purple, direction)

    def get_adjacent_magnets(self, purple, direction):
        """Return a list of magnets directly adjacent to the purple magnet in the specified direction."""
        x, y = purple.pos
        adjacent_positions = []

        if direction == "left":
            adjacent_positions = [(x, y - 1), (x, y - 2)]
        elif direction == "right":
            adjacent_positions = [(x, y + 1), (x, y + 2)]
        elif direction == "up":
            adjacent_positions = [(x - 1, y), (x - 2, y)]
        elif direction == "down":
            adjacent_positions = [(x + 1, y), (x + 2, y)]

        return [magnet for magnet in self.grays + self.reds if magnet.pos in adjacent_positions]

    def push_magnets_according_to_rules(self, purple, direction):
        adjacent_magnets = self.get_adjacent_magnets(purple, direction)

        if adjacent_magnets:
            if self.has_blank_space_next_to(purple, direction):
                self.push_magnets_away_from_purple(purple, adjacent_magnets, direction)
            else:
                self.push_magnets_away_from_purple(purple, adjacent_magnets, direction)

    def has_blank_space_next_to(self, purple, direction):
        """Check if there is a blank space immediately next to the purple magnet."""
        x, y = purple.pos
        if direction == "left":
            return self.is_position_empty((x, y - 1))
        elif direction == "right":
            return self.is_position_empty((x, y + 1))
        elif direction == "up":
            return self.is_position_empty((x - 1, y))
        elif direction == "down":
            return self.is_position_empty((x + 1, y))
        return False

    def push_magnets_away_from_purple(self, purple, adjacent_magnets, direction):
        """Push adjacent magnets away from the purple magnet to create space."""
        for magnet in adjacent_magnets:
            self.push_single_magnet(purple, magnet, direction)

    def push_single_magnet(self, purple, magnet, direction):
        """Push a single magnet according to the defined rules."""
        x, y = magnet.pos
        new_pos = (x, y)

        if direction == "left":
            new_pos = (x, y - 1)
        elif direction == "right":
            new_pos = (x, y + 1)
        elif direction == "up":
            new_pos = (x - 1, y)
        elif direction == "down":
            new_pos = (x + 1, y)

        if self.is_within_bounds(new_pos) and not self.is_position_occupied(new_pos):
            magnet.pos = new_pos

    def is_within_bounds(self, pos):
        """Check if a position is within the grid bounds."""
        x, y = pos
        return 0 <= x < self.grid.rows and 0 <= y < self.grid.cols

    def is_position_occupied(self, pos):
        """Check if a given position is occupied by any magnet."""
        return any(magnet.pos == pos for magnet in self.grays + self.reds + self.purples)

    def is_position_empty(self, pos):
        """Check if a given position is empty (not occupied by any magnet)."""
        return not self.is_position_occupied(pos)
