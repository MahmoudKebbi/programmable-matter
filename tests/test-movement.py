import unittest
from src.grid import Grid


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(n=10, m=10, initial_positions=[(4, 4), (4, 5), (5, 4), (5, 5)])

    def test_uniform_move_valid(self):
        """Test a valid uniform move (right)."""
        self.grid.move(0, 1)
        expected_positions = [(4, 5), (4, 6), (5, 5), (5, 6)]
        self.assertEqual(sorted(self.grid.matter_elements), sorted(expected_positions))

    def test_uniform_move_invalid(self):
        """Test that a move out of bounds is rejected."""
        original_positions = self.grid.matter_elements.copy()
        self.grid.move(0, -10)  # Invalid move.
        self.assertEqual(self.grid.matter_elements, original_positions)

    def test_diagonal_uniform_move(self):
        """Test a valid diagonal move (up-left)."""
        self.grid.move(-1, -1)
        expected_positions = [(3, 3), (3, 4), (4, 3), (4, 4)]
        self.assertEqual(sorted(self.grid.matter_elements), sorted(expected_positions))


if __name__ == "__main__":
    unittest.main()
