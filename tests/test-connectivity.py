import unittest
from src.grid import Grid


class TestConnectivity(unittest.TestCase):
    def setUp(self):
        # Start with a connected 2x2 block.
        self.grid = Grid(n=10, m=10, initial_positions=[(4, 4), (4, 5), (5, 4), (5, 5)])

    def test_connected(self):
        """Test that a connected structure is recognized."""
        self.assertTrue(self.grid.is_connected())

    def test_diagonal_connection(self):
        """Test that two diagonally adjacent nodes are considered connected."""
        self.grid.matter_elements = [(1, 1), (2, 2)]
        self.assertTrue(self.grid.is_connected())

    def test_disconnected(self):
        """Test that a clearly disconnected structure is flagged."""
        # Remove a connecting element.
        self.grid.matter_elements = [(4, 4), (4, 5), (6, 4)]
        self.assertFalse(self.grid.is_connected())


if __name__ == "__main__":
    unittest.main()
