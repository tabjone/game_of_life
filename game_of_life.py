import numpy as np
import pygame as pg
from scipy.ndimage import zoom

BACKGROUND_COLOR = (213, 213, 213)  # Light grey


class GameOfLife:
    def __init__(self, num_rows: int, num_columns: int) -> None:
        """
        Initialize the grid with the given number of rows and columns

        Parameters:
        num_rows (int): Number of rows in the grid
        num_columns (int): Number of columns in the grid

        Returns:
        None
        """

        self.num_rows = num_rows
        self.num_columns = num_columns

        # Create a grid with ghost cells on the edges
        self.is_alive = np.zeros((num_columns + 2, num_rows + 2), dtype=np.uint8)

    def initialize_grid_random(self) -> None:
        """
        Initialize the grid with 1/3 of the cells alive

        Parameters:
        None

        Returns:
        None
        """

        # Columns and rows are swapped to match the pygame screen
        self.is_alive[1:-1, 1:-1] = np.random.choice(
            [0, 1], size=(self.num_columns, self.num_rows), p=[2 / 3, 1 / 3]
        )

    def get_num_neighbors(self) -> np.array:
        """
        Finds the number of neighbors for each cell in the grid

        Parameters:
        None

        Returns:
        np.array: Number of neighbors for each cell without ghost cells
        """

        is_alive = self.is_alive

        # Use numpy for fast computation
        num_neighbors = (
            np.roll(is_alive, 1, axis=0)
            + np.roll(is_alive, -1, axis=0)
            + np.roll(is_alive, 1, axis=1)
            + np.roll(is_alive, -1, axis=1)
            + np.roll(np.roll(is_alive, 1, axis=0), 1, axis=1)
            + np.roll(np.roll(is_alive, 1, axis=0), -1, axis=1)
            + np.roll(np.roll(is_alive, -1, axis=0), 1, axis=1)
            + np.roll(np.roll(is_alive, -1, axis=0), -1, axis=1)
        )

        # Set ghost cells to 0
        num_neighbors[0, :] = 0
        num_neighbors[-1, :] = 0
        num_neighbors[:, 0] = 0
        num_neighbors[:, -1] = 0

        return num_neighbors[1:-1, 1:-1]

    def update_status(self) -> None:
        """
        Updates the is_alive grid according to the rules of Conway's Game of Life inside the grid (without ghost cells)

        Parameters:
        None

        Returns:
        None
        """

        # Get the number of neighbors for each cell
        num_neighbors = self.get_num_neighbors()

        # Remove ghost cells
        is_alive = self.is_alive[1:-1, 1:-1]

        # Update the status of the cells
        self.is_alive[1:-1, 1:-1] = np.where(
            (is_alive == 1) & ((num_neighbors < 2) | (num_neighbors > 3)), 0, is_alive
        )
        self.is_alive[1:-1, 1:-1] = np.where(
            (is_alive == 0) & (num_neighbors == 3), 1, is_alive
        )

    def fit_is_alive_to_screen(self, screen_width: int, screen_height: int) -> np.array:
        """
        Fit the is_alive grid to the screen by zooming in and padding the array

        Parameters:
        screen_width (int): Width of the screen
        screen_height (int): Height of the screen

        Returns:
        np.array: is_alive grid zoomed in/out and padded to fit the screen
        """

        # Remove ghost cells
        is_alive = self.is_alive[1:-1, 1:-1]

        # find the difference between the screen and the array
        diff_width = screen_width - self.num_columns
        diff_height = screen_height - self.num_rows

        # find the shortest direction to zoom in
        if diff_width < diff_height:
            zoom_factor = screen_width / self.num_columns
        else:
            zoom_factor = screen_height / self.num_rows

        # zoom the array
        is_alive = zoom(is_alive, zoom=(zoom_factor, zoom_factor), order=0)

        # find the amount of padding needed
        if diff_width > diff_height:
            pad_width = (screen_width - is_alive.shape[0]) // 2

            # if the pad width is not filling the screen, add additional padding
            if 2 * pad_width + is_alive.shape[0] != screen_width:
                additional_pad = int(
                    (screen_width - (2 * pad_width + is_alive.shape[0]))
                )
            else:
                additional_pad = 0

            # pad the array
            is_alive = np.pad(
                is_alive,
                pad_width=((pad_width, pad_width + additional_pad), (0, 0)),
                mode="constant",
                constant_values=0,
            )

        else:
            pad_height = (screen_height - is_alive.shape[1]) // 2

            # if the pad height is not filling the screen, add additional padding
            if 2 * pad_height + is_alive.shape[1] != screen_height:
                additional_pad = int(
                    (screen_height - (2 * pad_height + is_alive.shape[1]))
                )
            else:
                additional_pad = 0

            # pad the array
            is_alive = np.pad(
                is_alive,
                pad_width=((0, 0), (pad_height, pad_height + additional_pad)),
                mode="constant",
                constant_values=0,
            )

        return is_alive

    def draw_surface(
        self, screen: pg.Surface, screen_width: int, screen_height: int
    ) -> None:
        """
        Draw the is_alive grid to the screen

        Parameters:
        screen (pg.Surface): Pygame screen
        screen_width (int): Width of the screen
        screen_height (int): Height of the screen

        Returns:
        None
        """

        # Fit the is_alive grid to the screen
        is_alive = self.fit_is_alive_to_screen(screen_width, screen_height)
        # Create a pygame surface
        surface = pg.Surface((screen_width, screen_height))
        # Create a numpy array with the correct colors
        surface_array = (1 - is_alive[:, :, np.newaxis]) * BACKGROUND_COLOR
        # Blit the numpy array to the surface
        pg.surfarray.blit_array(surface, surface_array)
        # Blit the surface to the screen
        screen.blit(surface, (0, 0))
        # Update the screen
        pg.display.flip()
