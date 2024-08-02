# Conway's Game of Life using NumPy

Requirements: 
    `python 3.11.5`,
    `numpy 1.26.4`,
    `pygame 2.6.0`,
    `scipy 1.14.0`.

This is Conway's Game of Life with no for-loops. We instead use `NumPy` for calculations with array-operations. The game is visualized using `pygame` and has a resizable screen with square cells (meaning the game-grid will not be streched to fit the screen).

In `main.py` you can set the grid size with `(num_rows, num_columns)`. The grid is initalized with `initialize_grid_random` which creates 1/3 of the grid in the alive state and 2/3 in the dead state. Additional initializations can be added as child classes.

To run use `python main.py`.
