# Programmable Matter Simulation

## Overview
This project implements a simulation of programmable matter using Python, NumPy, and Pygame. It supports:
- A grid-based environment.
- Uniform and shape-changing (individual) moves.
- 8-way (Moore) connectivity and movement, including diagonal moves.
- Real-time visualization and user interaction.

## Project Structure
📂 programmable_matter_project/
│── 📂 src/                      # Source code directory
│   │── 📜 main.py               # Entry point to run the simulation
│   │── 📜 grid.py               # Grid class (handles movement and connectivity)
│   │── 📜 visualizer.py         # Visualization module (Pygame)
│   │── 📜 ai_agent.py           # AI agent for automated shape transformation
│── 📂 tests/                    # Unit tests directory
│   │── 📜 test_grid.py          # Tests for grid initialization and connectivity
│   │── 📜 test_movement.py      # Tests for uniform and individual movement
│   │── 📜 test_connectivity.py  # Tests for connectivity logic (Moore neighborhood)
│── 📂 docs/                     # Documentation directory (for future use)
│── 📜 README.md                 # Project overview and instructions
│── 📜 requirements.txt          # Dependencies (Pygame, NumPy)


markdown
Copy
Edit

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   ```bash
    python src/main.py
    ```

Controls
Uniform Mode:
Arrow keys: Move up, down, left, right.
Q/E/Z/C: Diagonal moves.
Individual Mode:
Tab: Toggle between uniform and individual modes.
R: Cycle to previous block.
F: Cycle to next block.
W/A/S/D: Cardinal moves for the selected block.
Q/E/Z/C: Diagonal moves for the selected block.





