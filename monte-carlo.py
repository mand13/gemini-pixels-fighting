import numpy as np
import random
import time

# --- Settings from your simulation ---
GRID_WIDTH = 100
GRID_HEIGHT = 100
NUM_TEAMS = 10
UPDATES_PER_FRAME = 1000  # This is the key link
TOTAL_PIXELS = GRID_WIDTH * GRID_HEIGHT

# --- Experiment Settings ---
NUM_TRIALS = 100  # How many times to run the "war" to get a good average

# (This is the same function from the simulation)
def init_grid(width, height, num_teams):
    return np.random.randint(0, num_teams, size=(height, width), dtype=np.int32)

# (This is the same function from the simulation)
def run_simulation_step(grid):
    attacker_y = random.randint(0, GRID_HEIGHT - 1)
    attacker_x = random.randint(0, GRID_WIDTH - 1)
    attacker_team = grid[attacker_y, attacker_x]
    
    defender_dy = random.randint(-1, 1)
    defender_dx = random.randint(-1, 1)
    
    if defender_dy == 0 and defender_dx == 0:
        return

    defender_y = (attacker_y + defender_dy) % GRID_HEIGHT
    defender_x = (attacker_x + defender_dx) % GRID_WIDTH
    
    grid[defender_y, defender_x] = attacker_team

def run_single_war():
    """
    Runs one full simulation until consensus is reached.
    Returns the total number of updates (fights) it took.
    """
    grid = init_grid(GRID_WIDTH, GRID_HEIGHT, NUM_TEAMS)
    update_count = 0
    
    while True:
        # Run one "fight"
        run_simulation_step(grid)
        update_count += 1
        
        # To speed things up, we only check for consensus every N updates.
        # Checking every single update is very slow.
        # We check every UPDATES_PER_FRAME, which is a good interval.
        if update_count % UPDATES_PER_FRAME == 0:
            
            # Check if all elements in the grid are the same
            # We can do this by comparing all elements to the first one.
            if np.all(grid == grid[0, 0]):
                return update_count # Consensus reached!

def main():
    print(f"--- Pixel War Monte Carlo Simulation ---")
    print(f"Grid: {GRID_WIDTH}x{GRID_HEIGHT}, Teams: {NUM_TEAMS}, Updates/Frame: {UPDATES_PER_FRAME}")
    print(f"Running {NUM_TRIALS} trials to find the average time to consensus...\n")
    
    start_time = time.time()
    
    all_update_counts = []
    
    for i in range(NUM_TRIALS):
        print(f"  Running trial {i + 1}/{NUM_TRIALS}...")
        updates_needed = run_single_war()
        all_update_counts.append(updates_needed)
        
    end_time = time.time()
    
    print("\n--- Results ---")
    print(f"Total time for experiment: {end_time - start_time:.2f} seconds")
    
    # Calculate statistics
    avg_updates = np.mean(all_update_counts)
    min_updates = np.min(all_update_counts)
    max_updates = np.max(all_update_counts)
    
    # Convert updates to frames
    avg_frames = avg_updates / UPDATES_PER_FRAME
    min_frames = min_updates / UPDATES_PER_FRAME
    max_frames = max_updates / UPDATES_PER_FRAME
    
    print(f"\nAverage Frames to Consensus: {avg_frames:.2f}")
    print(f"Fastest War: {min_frames:.0f} frames")
    print(f"Slowest War: {max_frames:.0f} frames")

if __name__ == "__main__":
    main()