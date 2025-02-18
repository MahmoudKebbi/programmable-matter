# Programmable Matter Simulation

## Overview
This project implements a simulation of programmable matter using Python, NumPy, and Pygame. It supports:
- A grid-based environment.
- Uniform and shape-changing (individual) moves.
- 8-way (Moore) connectivity and movement, including diagonal moves.
- Real-time visualization and user interaction.

## Project Structure
programmable_matter_project/ │── src/ │ │── main.py # Entry point for the simulation. │ │── grid.py # Contains the Grid class and movement/connectivity logic. │ │── visualizer.py # Visualization module using Pygame. │── tests/ │ │── test_grid.py
│ │── test_movement.py │ │── test_connectivity.py │── README.md │── requirements.txt

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





