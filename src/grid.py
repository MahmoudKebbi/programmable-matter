import numpy as np
from collections import deque


class Grid:
    """
    Represents the programmable matter simulation grid.

    Attributes:
        n (int): Number of rows in the grid.
        m (int): Number of columns in the grid.
        grid (np.ndarray): A 2D array representing the grid state.
        matter_elements (list of tuple): List of coordinates (x, y) of matter elements.
    """

    def __init__(self, n: int, m: int, initial_positions: list):
        """
        Initializes the grid with the given dimensions and places matter elements.

        Args:
            n (int): Number of rows in the grid.
            m (int): Number of columns in the grid.
            initial_positions (list of tuple): List of (x, y) coordinates where matter elements are placed.
        """
        self.n = n  # Grid height
        self.m = m  # Grid width
        self.grid = np.zeros((n, m), dtype=int)  # 0 = empty, 1 = matter element
        self.matter_elements = initial_positions  # List of (x, y) positions

        # Place matter elements in the grid
        for x, y in self.matter_elements:
            self.grid[x, y] = 1

    def display_grid(self):
        """
        Prints the grid in a readable format for debugging purposes.
        """
        print("\nGrid State:")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def is_valid_move(self, dx: int, dy: int) -> bool:
        """
        Checks if moving the entire matter block by (dx, dy) is valid with respect to grid boundaries.

        Args:
            dx (int): Change in x-direction (-1, 0, or 1).
            dy (int): Change in y-direction (-1, 0, or 1).

        Returns:
            bool: True if the move is within grid boundaries, False otherwise.
        """
        new_positions = [(x + dx, y + dy) for x, y in self.matter_elements]

        # Check if new positions are within grid boundaries
        for x, y in new_positions:
            if not (0 <= x < self.n and 0 <= y < self.m):
                return False  # Out of bounds

        return True

    def move(self, dx: int, dy: int):
        """
        Moves the entire matter block by (dx, dy) if the move is valid.

        Args:
            dx (int): Change in x-direction (-1, 0, or 1).
            dy (int): Change in y-direction (-1, 0, or 1).
        """
        if self.is_valid_move(dx, dy):
            # Clear old positions
            for x, y in self.matter_elements:
                self.grid[x, y] = 0

            # Update positions
            self.matter_elements = [(x + dx, y + dy) for x, y in self.matter_elements]

            # Set new positions
            for x, y in self.matter_elements:
                self.grid[x, y] = 1
        else:
            print("Invalid move! Movement aborted.")

    def is_connected(self) -> bool:
        """
        Checks if the current matter elements form a single connected component
        using a BFS approach based on Von Neumann (4-way) connectivity.

        Returns:
            bool: True if all matter elements are connected, False otherwise.
        """
        if not self.matter_elements:
            # An empty grid is trivially connected.
            return True

        # Use a set for O(1) membership tests.
        matter_set = set(self.matter_elements)
        visited = set()
        queue = deque()

        # Start BFS from the first matter element.
        start = self.matter_elements[0]
        queue.append(start)
        visited.add(start)

        # Define the Von Neumann neighbors (up, down, left, right).
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            cx, cy = queue.popleft()
            for dx, dy in directions:
                neighbor = (cx + dx, cy + dy)
                # Only consider neighbors that are part of the matter elements.
                if neighbor in matter_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # If the number of visited blocks equals the total, the structure is connected.
        return len(visited) == len(self.matter_elements)
