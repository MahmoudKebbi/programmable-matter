import pygame
from src.grid import Grid

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 102, 204)
GREEN = (0, 255, 0)  # Highlight for selected block


class Visualizer:
    """
    Handles rendering the programmable matter grid using Pygame.
    Supports uniform and individual (shape-changing) movement modes.
    """

    def __init__(self, grid: Grid, cell_size: int = 50):
        """
        Initializes the Pygame visualization.

        Args:
            grid (Grid): The Grid object containing the simulation.
            cell_size (int): Pixel size of each grid cell.
        """
        self.grid = grid
        self.cell_size = cell_size
        self.width = grid.m * cell_size
        self.height = grid.n * cell_size
        self.mode = "uniform"  # "uniform" for moving all blocks; "individual" for single block movement.
        self.selected_index = (
            0  # For individual mode, index of currently selected block.
        )
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Programmable Matter Simulation")

    def draw_grid(self):
        """
        Draws grid lines and matter elements.
        Highlights the selected block in individual mode.
        """
        self.screen.fill(WHITE)
        # Draw grid lines.
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.width, y))

        # Draw matter elements.
        for i, (row, col) in enumerate(self.grid.matter_elements):
            color = (
                GREEN
                if (self.mode == "individual" and i == self.selected_index)
                else BLUE
            )
            rect = pygame.Rect(
                col * self.cell_size,
                row * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, color, rect)

        # Display current mode.
        font = pygame.font.Font(None, 24)
        mode_text = font.render(f"Mode: {self.mode}", True, BLACK)
        self.screen.blit(mode_text, (10, 10))
        pygame.display.flip()

    def run(self):
        """
        Main loop for visualization with keyboard input.
        Uniform mode uses arrow keys and diagonal keys.
        Individual mode uses W/A/S/D for cardinal moves and Q/E/Z/C for diagonal moves.
        Use R/F to cycle through blocks in individual mode.
        Tab toggles the movement mode.
        """
        running = True
        while running:
            self.draw_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # Toggle movement mode.
                    if event.key == pygame.K_TAB:
                        self.mode = (
                            "individual" if self.mode == "uniform" else "uniform"
                        )

                    if self.mode == "uniform":
                        # Uniform movement controls.
                        if event.key == pygame.K_UP:
                            self.grid.move(-1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.grid.move(1, 0)
                        elif event.key == pygame.K_LEFT:
                            self.grid.move(0, -1)
                        elif event.key == pygame.K_RIGHT:
                            self.grid.move(0, 1)
                        elif event.key == pygame.K_q:  # Diagonal up-left.
                            self.grid.move(-1, -1)
                        elif event.key == pygame.K_e:  # Diagonal up-right.
                            self.grid.move(-1, 1)
                        elif event.key == pygame.K_z:  # Diagonal down-left.
                            self.grid.move(1, -1)
                        elif event.key == pygame.K_c:  # Diagonal down-right.
                            self.grid.move(1, 1)

                    elif self.mode == "individual":
                        # In individual mode, use R and F to cycle through blocks.
                        if event.key == pygame.K_r:
                            self.selected_index = (self.selected_index - 1) % len(
                                self.grid.matter_elements
                            )
                        elif event.key == pygame.K_f:
                            self.selected_index = (self.selected_index + 1) % len(
                                self.grid.matter_elements
                            )

                        # Movement for the selected block.
                        moves = {}
                        if event.key == pygame.K_w:  # Move up.
                            moves[self.selected_index] = (-1, 0)
                        elif event.key == pygame.K_s:  # Move down.
                            moves[self.selected_index] = (1, 0)
                        elif event.key == pygame.K_a:  # Move left.
                            moves[self.selected_index] = (0, -1)
                        elif event.key == pygame.K_d:  # Move right.
                            moves[self.selected_index] = (0, 1)
                        elif event.key == pygame.K_q:  # Diagonal up-left.
                            moves[self.selected_index] = (-1, -1)
                        elif event.key == pygame.K_e:  # Diagonal up-right.
                            moves[self.selected_index] = (-1, 1)
                        elif event.key == pygame.K_z:  # Diagonal down-left.
                            moves[self.selected_index] = (1, -1)
                        elif event.key == pygame.K_c:  # Diagonal down-right.
                            moves[self.selected_index] = (1, 1)

                        if moves:
                            success = self.grid.move_individual(moves)
                            if not success:
                                print("Invalid individual move.")

            pygame.time.delay(100)
        pygame.quit()
