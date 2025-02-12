from src.grid import Grid
from src.visualizer import Visualizer
import unittest


def main():
    """
    Initializes the programmable matter simulation and starts the visualization.
    """
    # Define grid size and initial matter positions
    n, m = 10, 10  # Grid dimensions
    initial_positions = [(4, 4), (4, 5), (5, 4), (5, 5)]  # 2x2 starting shape

    # Create grid and visualizer
    grid = Grid(n, m, initial_positions)
    visualizer = Visualizer(grid)

    # Run the visualization loop
    visualizer.run()


if __name__ == "__main__":
    # Set the correct start directory for test discovery
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)

    main()
