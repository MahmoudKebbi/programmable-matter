import numpy as np
from collections import deque


class Grid:
    """
    Represents the programmable matter simulation grid.

    Attributes:
        n (int): Number of rows in the grid.
        m (int): Number of columns in the grid.
        grid (np.ndarray): A 2D array representing the grid state.
        matter_elements (list of tuple): List of (x, y) coordinates of matter elements.
    """

    def __init__(self, n: int, m: int, initial_positions: list):
        """
        Initializes the grid with given dimensions and places matter elements.

        Args:
            n (int): Number of rows.
            m (int): Number of columns.
            initial_positions (list of tuple): List of (x, y) coordinates for matter elements.
        """
        self.n = n
        self.m = m
        self.grid = np.zeros((n, m), dtype=int)
        self.matter_elements = initial_positions.copy()

        # Place matter elements in the grid
        for x, y in self.matter_elements:
            self.grid[x, y] = 1

    def display_grid(self):
        """
        Prints the grid state for debugging.
        """
        print("\nGrid State:")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def is_connected(self) -> bool:
        """
        Checks if all matter elements form a single connected component using BFS based on Moore (8-way) connectivity.
        Diagonally adjacent blocks are considered connected.

        Returns:
            bool: True if all elements are connected, False otherwise.
        """
        if not self.matter_elements:
            return True  # An empty set is trivially connected

        matter_set = set(self.matter_elements)
        visited = set()
        queue = deque()

        # Start BFS from the first matter element.
        start = self.matter_elements[0]
        queue.append(start)
        visited.add(start)

        # Moore neighborhood: 8 directions.
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        while queue:
            cx, cy = queue.popleft()
            for dx, dy in directions:
                neighbor = (cx + dx, cy + dy)
                if neighbor in matter_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(visited) == len(self.matter_elements)

    def is_valid_move(self, dx: int, dy: int) -> bool:
        """
        Checks if moving the entire matter block by (dx, dy) is valid:
          1. New positions must be within grid boundaries.
          2. The structure must remain connected.

        Args:
            dx (int): Change in row direction.
            dy (int): Change in column direction.

        Returns:
            bool: True if the uniform move is valid, False otherwise.
        """
        new_positions = [(x + dx, y + dy) for x, y in self.matter_elements]

        # Check boundaries.
        for x, y in new_positions:
            if not (0 <= x < self.n and 0 <= y < self.m):
                return False

        # Temporarily update positions to check connectivity.
        original_positions = self.matter_elements.copy()
        self.matter_elements = new_positions
        connected = self.is_connected()
        self.matter_elements = original_positions  # Revert
        return connected

    def move(self, dx: int, dy: int):
        """
        Moves the entire matter block by (dx, dy) if valid (within bounds and preserving connectivity).

        Args:
            dx (int): Change in row direction.
            dy (int): Change in column direction.
        """
        if self.is_valid_move(dx, dy):
            # Clear previous positions.
            for x, y in self.matter_elements:
                self.grid[x, y] = 0

            # Update positions.
            self.matter_elements = [(x + dx, y + dy) for x, y in self.matter_elements]

            # Write new positions.
            for x, y in self.matter_elements:
                self.grid[x, y] = 1
        else:
            print("Invalid move! It would break connectivity or go out of bounds.")

    def move_individual(self, moves: dict) -> bool:
        """
        Performs shape-changing moves by moving individual matter elements.
        The move is specified as a dictionary where keys are indices (of matter_elements)
        and values are (dx, dy) tuples.

        Args:
            moves (dict): Mapping from matter element index to (dx, dy).

        Returns:
            bool: True if the move is applied successfully, False if it is invalid.
        """
        # Create new positions; elements not specified in moves remain stationary.
        new_positions = []
        for i, (x, y) in enumerate(self.matter_elements):
            dx, dy = moves.get(i, (0, 0))
            new_positions.append((x + dx, y + dy))

        # Check boundaries.
        for x, y in new_positions:
            if not (0 <= x < self.n and 0 <= y < self.m):
                print("Invalid individual move: out of bounds.")
                return False

        # Temporarily update and check connectivity.
        original_positions = self.matter_elements.copy()
        self.matter_elements = new_positions
        if not self.is_connected():
            self.matter_elements = original_positions  # Revert changes.
            print("Invalid individual move: move breaks connectivity.")
            return False

        # Update the grid.
        self.grid.fill(0)
        for x, y in self.matter_elements:
            self.grid[x, y] = 1

        return True
