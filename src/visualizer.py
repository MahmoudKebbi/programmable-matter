import pygame
import time
from src.grid import Grid
from src.ai_agent import AI_Agent

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 102, 204)
GREEN = (0, 255, 0)  # Highlight selected block
RED = (255, 0, 0)  # AI execution mode color


class Visualizer:
    """
    Handles rendering the programmable matter grid using Pygame.
    Supports uniform, individual, and AI-based movement modes.
    """

    def __init__(self, grid: Grid, target_shape: list, cell_size: int = 50):
        """
        Initializes the Pygame visualization.

        Args:
            grid (Grid): The Grid object containing the simulation.
            target_shape (list): Target shape to be formed by the AI.
            cell_size (int): Size of each grid cell in pixels.
        """
        self.grid = grid
        self.target_shape = target_shape
        self.cell_size = cell_size
        self.width = grid.m * cell_size
        self.height = grid.n * cell_size
        self.mode = "manual"  # "manual" (user control) or "ai" (AI execution)
        self.selected_index = (
            0  # For individual mode, index of currently selected block.
        )
        self.ai_agent = AI_Agent(
            grid.n, grid.m, self.grid.matter_elements, self.target_shape
        )
        self.ai_plan = []
        self.ai_step = 0  # Track AI execution progress

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Programmable Matter Simulation")

    def draw_grid(self):
        """
        Draws grid lines and matter elements.
        Highlights the selected block in individual mode.
        If AI is active, shows a different color.
        """
        self.screen.fill(WHITE)
        # Draw grid lines.
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.width, y))

        # Draw matter elements.
        for i, (row, col) in enumerate(self.grid.matter_elements):
            if self.mode == "ai":
                color = RED  # AI mode highlight
            elif self.mode == "individual" and i == self.selected_index:
                color = GREEN  # Selected block highlight
            else:
                color = BLUE
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

    def execute_ai_plan(self):
        """
        Executes the AI-generated plan step by step.
        Ensures that all individual moves for a given step are executed as one batch.
        """
        if self.ai_step < len(self.ai_plan):
            move_set = self.ai_plan[self.ai_step]

            # Ensure move_set is a list of moves
            if isinstance(move_set, tuple) and len(move_set) == 3:
                move_set = [move_set]  # Convert single move into a list

            if not isinstance(move_set, list) or not all(
                len(move) == 3 for move in move_set
            ):
                print(f"Error: Unexpected move format: {move_set}")
                return

            # **Fix: Group all individual moves into one dictionary**
            moves = {i: (dx, dy) for i, dx, dy in move_set}

            # **Print to check grouped moves**
            print(
                f"Executing shape-changing move {self.ai_step + 1}/{len(self.ai_plan)}: {moves}"
            )

            success = self.grid.move_individual(moves)

            if not success:
                print(
                    "Invalid move! Removing it from the plan and retrying a different approach..."
                )
                self.ai_plan.pop(self.ai_step)  # Remove failed move
                return  # Do not increment `ai_step`, retry from the same step

            self.ai_step += 1
        else:
            print("AI execution complete!")
            self.mode = "manual"

    def run(self):
        """
        Main loop for visualization with keyboard input.
        Supports AI execution alongside manual control.
        """
        running = True
        while running:
            self.draw_grid()

            if self.mode == "ai":
                self.execute_ai_plan()
                time.sleep(0.5)  # Slow down execution for visualization

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    print(f"Key pressed: {event.key}")

                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_g:
                        self.grid.display_grid()

                    if event.key == pygame.K_t:  # Activate AI mode
                        print("AI mode activated: Computing plan...")
                        self.mode = "AI Auto"
                        self.ai_agent = AI_Agent(
                            self.grid.n,
                            self.grid.m,
                            self.grid.matter_elements,
                            self.target_shape,
                        )
                        self.ai_plan = self.ai_agent.plan()
                        if self.ai_plan:
                            print("Executing AI plan...")
                            self.mode = "ai"
                            self.ai_step = 0
                        else:
                            print("No valid AI plan found.")

                    if event.key == pygame.K_TAB:
                        self.mode = "individual" if self.mode == "manual" else "manual"

                    if self.mode == "manual":
                        # Move the entire structure
                        if event.key == pygame.K_UP:
                            self.grid.move(-1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.grid.move(1, 0)
                        elif event.key == pygame.K_LEFT:
                            self.grid.move(0, -1)
                        elif event.key == pygame.K_RIGHT:
                            self.grid.move(0, 1)
                        elif event.key == pygame.K_q:  # Diagonal up-left
                            self.grid.move(-1, -1)
                        elif event.key == pygame.K_e:  # Diagonal up-right
                            self.grid.move(-1, 1)
                        elif event.key == pygame.K_z:  # Diagonal down-left
                            self.grid.move(1, -1)
                        elif event.key == pygame.K_c:  # Diagonal down-right
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

                        # Move selected block.
                        moves = {}
                        if event.key == pygame.K_w:
                            moves[self.selected_index] = (-1, 0)
                        elif event.key == pygame.K_s:
                            moves[self.selected_index] = (1, 0)
                        elif event.key == pygame.K_a:
                            moves[self.selected_index] = (0, -1)
                        elif event.key == pygame.K_d:
                            moves[self.selected_index] = (0, 1)
                        elif event.key == pygame.K_q:
                            moves[self.selected_index] = (-1, -1)
                        elif event.key == pygame.K_e:
                            moves[self.selected_index] = (-1, 1)
                        elif event.key == pygame.K_z:
                            moves[self.selected_index] = (1, -1)
                        elif event.key == pygame.K_c:
                            moves[self.selected_index] = (1, 1)

                        if moves:
                            self.grid.move_individual(moves)

            pygame.time.delay(100)
        pygame.quit()
