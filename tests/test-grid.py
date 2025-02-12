import unittest
from src.grid import Grid


class TestGrid(unittest.TestCase):
    """
    Unit tests for the Grid class.
    """

    def setUp(self):
        """
        Runs before each test to initialize a common grid state.
        """
        self.grid = Grid(n=10, m=10, initial_positions=[(4, 4), (4, 5), (5, 4), (5, 5)])

    def test_initial_connectivity(self):
        """Test that the matter elements start as a connected structure."""
        self.assertTrue(self.grid.is_connected(), "Initial state should be connected.")

    def test_valid_move(self):
        """Test that a valid move keeps the matter connected."""
        self.grid.move(0, 1)  # Move right
        self.assertTrue(
            self.grid.is_connected(),
            "Matter should remain connected after a valid move.",
        )

    def test_out_of_bounds_move(self):
        """Test that an out-of-bounds move is prevented."""
        self.grid.move(0, -10)  # Move left beyond the boundary
        self.assertTrue(
            self.grid.is_connected(),
            "Matter should remain unchanged after an invalid move.",
        )

    def test_disconnected_state(self):
        """Test that a manually disconnected grid is detected as False."""
        self.grid.matter_elements = [
            (4, 4),
            (4, 5),
            (6, 4),
            (6, 5),
        ]  # Manually break connectivity
        self.assertFalse(
            self.grid.is_connected(), "Disconnected shape should return False."
        )


if __name__ == "__main__":
    unittest.main()
