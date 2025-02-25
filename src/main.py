import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grid import Grid
from src.visualizer import Visualizer


def main():
    """
    Entry point for the programmable matter simulation.
    Initializes a 10x10 grid with a starting shape and a target shape.
    """
    n, m = 10, 10
    start_positions = [(9, 0), (9, 1), (9, 2), (9, 3)]  # 2x2 starting shape
    target_positions = [(2, 2), (2, 3), (2, 4), (3, 3)]  # AI will try to move here

    grid = Grid(n, m, start_positions)
    visualizer = Visualizer(grid, target_positions)
    visualizer.run()


if __name__ == "__main__":
    main()
