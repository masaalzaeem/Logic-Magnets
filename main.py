import pygame
from level import Level
from game import Game

pygame.init()

screen_width, screen_height = 700, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Logic Magnets")

level_screen = Level(screen)

running = True
current_level = None
game = None
in_game = False
win = False
game_over = False
resetting_to_level = False

def initialize_level(level_number):
    global game, in_game, game_over, win, resetting_to_level
    grid_size, grays, reds, purples, target_positions, moves_allowed, level_number = level_screen.get_level_properties(level_number)
    game = Game(screen, grid_size, grays, reds, purples, target_positions, moves_allowed, level_number)
    in_game = True
    game_over = False
    win = False
    resetting_to_level = False

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if game_over:
                    if resetting_to_level:
                        game_over = False
                        in_game = False
                        game = None
                        resetting_to_level = False
                    else:
                        resetting_to_level = True
                        initialize_level(current_level)
                    continue

                elif in_game:
                    in_game = False
                    game_over = False
                    game = None
                    resetting_to_level = False
                else:
                    in_game = False

            elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if in_game:
                    initialize_level(current_level)
                    continue
            
            elif event.key == pygame.K_b and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if in_game:
                    game.bfs_solve()
                    game.draw()
                    pygame.display.flip()
                    
            elif event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if in_game:
                    game.dfs_solve()
                    game.draw()
                    pygame.display.flip()

            elif event.key == pygame.K_u and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if in_game:
                    game.ucs_solve()
                    game.draw()
                    pygame.display.flip()

            elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if in_game:
                    game.hill_climb_solve()
                    game.draw()
                    pygame.display.flip()

        if in_game and game:
            exit_to_levels = game.handle_event(event)

            if game.game_over:
                game_over = True
                in_game = False
                resetting_to_level = False
                continue

            if game.check_win_condition():
                win = True
                in_game = False
                continue

        elif not in_game:
            selected_level = level_screen.handle_event(event)
            if selected_level is not None:
                current_level = selected_level
                initialize_level(current_level)

    screen.fill((0, 0, 0))

    if in_game and game:
        game.draw()

    if win:
        game.draw()
        game.display_win_screen()
        pygame.display.flip()
        pygame.time.wait(2000)

        current_level += 1
        if current_level > 30:
            current_level = 1
        initialize_level(current_level)

    if game_over:
        game.draw()
        game.display_game_over()
        pygame.display.flip()

    if not in_game and not game_over:
        level_screen.draw()

    pygame.display.flip()
