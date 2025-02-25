import heapq
from typing import List, Tuple, Optional
from collections import deque
from itertools import combinations

# Define the eight possible directions for movement (Moore neighborhood)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def is_safe_shape_change(old_state, new_state):
    """
    Ensures that no block gets isolated due to an individual move.
    - A move is safe if it keeps at least one Moore-connected neighbor.
    """
    old_set = set(old_state)
    new_set = set(new_state)

    for x, y in new_state:
        neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS]
        if any(neighbor in new_set for neighbor in neighbors):
            continue  # Block is still connected
        else:
            return False  # Block got isolated

    return True


def is_state_connected(state: List[Tuple[int, int]], n: int, m: int) -> bool:
    """
    Checks whether all blocks in 'state' are connected via 8-way (Moore) connectivity.
    """
    if not state:
        return True

    state_set = set(state)
    visited = set()
    queue = deque([state[0]])
    visited.add(state[0])

    while queue:
        x, y = queue.popleft()
        for dx, dy in DIRECTIONS:
            neighbor = (x + dx, y + dy)
            if neighbor in state_set and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == len(state)


def state_to_tuple(state: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
    """Converts a list of block positions to a sorted tuple for hashability."""
    return tuple(sorted(state))


def heuristic(state: List[Tuple[int, int]], target: List[Tuple[int, int]]) -> int:
    """
    Smarter heuristic:
    - Rewards states that match the target shape.
    - Penalizes states that spread blocks too far apart.
    """
    h = 0
    for x, y in state:
        min_dist = min(((x - tx) ** 2 + (y - ty) ** 2) ** 0.5 for tx, ty in target)
        h += min_dist

    # Penalize states where blocks are spread too far apart
    max_spread = max(
        abs(x1 - x2) + abs(y1 - y2) for x1, y1 in state for x2, y2 in state
    )
    h += max_spread * 0.5  # Reduce weight of spreading penalty

    return h


from itertools import combinations


from itertools import combinations


def get_successors(state: List[Tuple[int, int]], n: int, m: int):
    """
    Generates valid successor states while ensuring connectivity.
    Supports:
      - Uniform moves (all blocks move together)
      - Non-uniform (coordinated) moves: multiple blocks moving in sync

    Args:
        state (List[Tuple[int, int]]): Current configuration of block positions.
        n (int): Number of grid rows.
        m (int): Number of grid columns.

    Returns:
        List[Tuple[new_state, moves]]: Each successor is a tuple where:
          - new_state is the new configuration (a list of positions),
          - moves is a list of tuples (i, dx, dy) representing which block(s) moved and by how much.
    """
    successors = []

    # --- Uniform Moves: move all blocks by (dx, dy) ---
    for dx, dy in DIRECTIONS:
        new_state = [(x + dx, y + dy) for x, y in state]
        if all(0 <= x < n and 0 <= y < m for x, y in new_state) and is_state_connected(
            new_state, n, m
        ):
            successors.append((new_state, [(i, dx, dy) for i in range(len(state))]))

    # --- Group Moves (Shape Changes): Move subsets of blocks together ---
    indices = range(len(state))
    for k in range(2, len(state) + 1):  # Move at least 2 blocks together
        for subset in combinations(indices, k):
            for dx, dy in DIRECTIONS:
                new_state = list(state)  # Copy current state
                valid = True
                moves = []
                # Apply move to selected subset of blocks
                for i in subset:
                    new_x = state[i][0] + dx
                    new_y = state[i][1] + dy
                    # Check if new position is within grid bounds
                    if not (0 <= new_x < n and 0 <= new_y < m):
                        valid = False
                        break
                    new_state[i] = (new_x, new_y)
                    moves.append((i, dx, dy))

                # Only keep this move if it maintains connectivity
                if valid and is_state_connected(new_state, n, m):
                    successors.append((new_state, moves))

    return successors


class AI_Agent:
    def __init__(
        self,
        n: int,
        m: int,
        start_state: List[Tuple[int, int]],
        target_state: List[Tuple[int, int]],
    ):
        """Initializes AI agent with a smarter strategy."""
        self.n = n
        self.m = m
        self.start_state = start_state
        self.target_state = target_state

    def plan(self) -> Optional[List[List[Tuple[int, int, int]]]]:
        """
        Uses A* search to plan a sequence of moves to transform the shape.
        Prioritizes moves that shift multiple blocks together.
        """
        start = tuple(sorted(self.start_state))
        target = tuple(sorted(self.target_state))

        frontier = []
        heapq.heappush(
            frontier, (heuristic(self.start_state, self.target_state), 0, start, [])
        )
        explored = set()

        while frontier:
            _, cost, current, path = heapq.heappop(frontier)

            if current == target:
                return path

            if current in explored:
                continue

            explored.add(current)

            # **Ensure that successors favor group moves first**
            successors = sorted(
                get_successors(list(current), self.n, self.m), key=lambda s: -len(s[1])
            )

            for succ, moves in successors:
                succ_tuple = tuple(sorted(succ))
                if succ_tuple in explored:
                    continue
                new_cost = cost + 1
                new_path = path + [moves]  # Group moves together
                heapq.heappush(
                    frontier,
                    (
                        new_cost + heuristic(succ, list(target)),
                        new_cost,
                        succ_tuple,
                        new_path,
                    ),
                )

        return None


if __name__ == "__main__":
    # Example usage:
    n, m = 10, 10
    start_state = [(4, 4), (4, 5), (5, 4), (5, 5)]
    target_state = [(2, 2), (2, 3), (3, 2), (3, 3)]

    agent = AI_Agent(n, m, start_state, target_state)
    plan = agent.plan()

    if plan:
        print("Plan found:")
        for move in plan:
            print(f"Move {move}")
    else:
        print("No plan found.")
