from game_of_life import GameOfLife
import pygame as pg

BACKGROUND_COLOR = (213, 213, 213)  # Light grey
NUM_ROWS, NUM_COLUMNS = 3000, 3000  # Number of rows and columns in the grid
TIME_BETWEEN_UPDATES = 200  # Time between each update in milliseconds

def main() -> None:
    """
    Main function to run Conway's Game of Life

    Parameters:
    None

    Returns:
    None
    """

    # Screen width and height
    screen_width, screen_height = 200, 250

    # Create and initialize the grid
    grid = GameOfLife(NUM_ROWS, NUM_COLUMNS)
    grid.initialize_grid_random()

    # Initialize pygame, create the screen and the clock
    pg.init()
    pg.display.set_caption("Game of Life")
    screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
    screen.fill(BACKGROUND_COLOR)
    clock = pg.time.Clock()

    # Draw the grid to the screen
    grid.draw_surface(screen, screen_width, screen_height)

    time_since_last_update = 0  # time since the last update in milliseconds
    running = True  # Boolean to keep track of whether the game is running
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Quit the game
                running = False
            elif event.type == pg.VIDEORESIZE:
                # Resize the screen
                screen_width, screen_height = event.w, event.h
        if time_since_last_update >= TIME_BETWEEN_UPDATES:
            # Update the grid and draw it to the screen
            time_since_last_update = 0
            grid.update_status()
            grid.draw_surface(screen, screen_width, screen_height)

        time_since_last_update += clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
