import pygame
import numpy as np
from collections import deque

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 102, 204)


class Visualizer:
    """
    Handles rendering the programmable matter grid using Pygame.
    """

    def __init__(self, grid, cell_size=50):
        """
        Initializes the Pygame visualization.

        Args:
            grid (Grid): The Grid object containing the matter simulation.
            cell_size (int): Size of each grid cell in pixels.
        """
        self.grid = grid
        self.cell_size = cell_size
        self.width = grid.m * cell_size
        self.height = grid.n * cell_size
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Programmable Matter Simulation")

    def draw_grid(self):
        """
        Draws the grid lines and fills in the matter elements.
        """
        self.screen.fill(WHITE)  # Clear screen

        # Draw grid lines
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.width, y))

        # Draw matter elements
        for x, y in self.grid.matter_elements:
            pygame.draw.rect(
                self.screen,
                BLUE,
                (
                    y * self.cell_size,
                    x * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                ),
            )

        pygame.display.flip()  # Update the display

    def run(self):
        """
        Main loop to visualize movement with keyboard input.
        """
        running = True
        while running:
            self.draw_grid()  # Update grid rendering
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Handle arrow key movement
                    if event.key == pygame.K_UP:
                        self.grid.move(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.grid.move(1, 0)
                    elif event.key == pygame.K_LEFT:
                        self.grid.move(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        self.grid.move(0, 1)

            pygame.time.delay(100)  # Delay for smooth visualization

        pygame.quit()  # Close Pygame window
