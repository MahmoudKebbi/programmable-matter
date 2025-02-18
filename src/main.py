from src.grid import Grid
from src.visualizer import Visualizer


def main():
    """
    Entry point for the programmable matter simulation.
    Initializes a 10x10 grid with a simple 2x2 block and starts the visualizer.
    """
    n, m = 10, 10  # Grid dimensions.
    initial_positions = [(4, 4), (4, 5), (5, 4), (5, 5)]  # 2x2 block.
    grid = Grid(n, m, initial_positions)
    visualizer = Visualizer(grid)
    visualizer.run()


if __name__ == "__main__":
    main()
