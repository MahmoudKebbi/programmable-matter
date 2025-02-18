import unittest
from src.grid import Grid


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(n=10, m=10, initial_positions=[(4, 4), (4, 5), (5, 4), (5, 5)])

    def test_grid_initialization(self):
        """Test that the grid is initialized correctly."""
        self.assertEqual(len(self.grid.matter_elements), 4)

    def test_initial_connectivity(self):
        """Test that the initial block is connected."""
        self.assertTrue(self.grid.is_connected())


if __name__ == "__main__":
    unittest.main()
