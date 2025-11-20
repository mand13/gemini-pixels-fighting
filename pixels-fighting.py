import pygame
import numpy as np
import random
import colorsys
import argparse
import datetime
import os
from colormath.color_objects import sRGBColor, LCHabColor
from colormath.color_conversions import convert_color

# --- Settings ---
RESULTS_DIR = "results"
TEAM_NAMES_FILE = "team_names.txt"

def init_grid(width, height, num_teams):
    """Creates a new grid with random team assignments."""
    return np.random.randint(0, num_teams, size=(height, width), dtype=np.int32)

def choose_random_pixel(grid_width, grid_height):
    """Chooses a random pixel coordinate within the grid."""
    y = random.randint(0, grid_height - 1)
    x = random.randint(0, grid_width - 1)
    return y, x

def choose_random_nearby_pixel(y, x, grid_width, grid_height, range=1):
    """Chooses a random adjacent pixel coordinate, wrapping around edges."""
    dy = random.choice([-range, 0, range])
    dx = random.choice([-range, 0, range])
    new_y = (y + dy) % grid_height
    new_x = (x + dx) % grid_width
    return new_y, new_x

def attack(grid, grid_width, grid_height, attacker_y, attacker_x, defender_y, defender_x, team_classes, hitpoints):
    """
    Executes an attack from attacker to defender.
    """
    attacker_team = grid[attacker_y, attacker_x]
    if attacker_team < 0:
        return # dead pixel cannot attack
    attacker_class = team_classes[attacker_team]
    defender_team = grid[defender_y, defender_x]
    if defender_team < 0:
        grid[attacker_y, attacker_x] = defender_team # attacker becomes dead necromancer
        grid[defender_y, defender_x] = -1*defender_team # dead necromancer comes alive
        return
    defender_class = team_classes[defender_team]

    if defender_team == attacker_team:
        if attacker_class == "Healer":
            hitpoints[attacker_team] += 1 # Healer heals its collective
        if attacker_class != "Plague":
            return
    
    # --- Defensive mechanics apply first ---
    
    if defender_class == "Healer":
        if hitpoints[defender_team] > 0:
            hitpoints[defender_team] -= 1 # Healer uses hitpoint to survive
            return
    
    if defender_class == "Bunker":
        if random.random() < 0.5:
            return # 50% chance to block attack
    
    if defender_class == "Thorns":
        if random.random() < 0.3:
            grid[attacker_y, attacker_x] = defender_team # Reflect attack
            return
    
    if defender_class == "Phalanx":
        # count adjacent allies
        ally_count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny = (defender_y + dy) % grid_height
                nx = (defender_x + dx) % grid_width
                if grid[ny, nx] == defender_team:
                    ally_count += 1
        if ally_count >= 4:
            return # Phalanx defended successfully
    
    if defender_class == "Sniper":
        if random.random() < 0.4: # Sniper is sneaky
            return
        
    # --- Attacker mechanics apply second ---
        
    if attacker_class == "Berserker":
        # attack converts cluster of pixels
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                ny = (defender_y + dy) % grid_height
                nx = (defender_x + dx) % grid_width
                if grid[ny, nx] == defender_team:
                    # random chance of taking over neighboring allies of defender
                    if random.random() < 0.3:
                        grid[ny, nx] = attacker_team
        return
    
    if attacker_class == "Mortar":
        # attack affects a 3x3 area
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if random.random() < 0.3: # chance to convert each pixel in area
                    ny = (defender_y + dy) % grid_height
                    nx = (defender_x + dx) % grid_width
                    grid[ny, nx] = attacker_team
        return
    
    if attacker_class == "Plague":
        # newly converted pixels have a chance to convert neighbors
        grid[defender_y, defender_x] = attacker_team
        if random.random() < 0.5:
            attack(grid, grid_width, grid_height, defender_y, defender_x, *choose_random_nearby_pixel(defender_y, defender_x, grid_width, grid_height, range=1), team_classes, hitpoints)
    
    if attacker_class == "Nomad":
        # swap places up to 7 spaces away before attacking, and immune to defense
        swap_y, swap_x = choose_random_nearby_pixel(attacker_y, attacker_x, grid_width, grid_height, range=7)
        grid[attacker_y, attacker_x], grid[swap_y, swap_x] = grid[swap_y, swap_x], grid[attacker_y, attacker_x]
        grid[choose_random_nearby_pixel(swap_y, swap_x, grid_width, grid_height, range=1)] = attacker_team
        return
    
    if attacker_class == "Necromancer":
        # converts defender into a dead gray pixel, which doesn't do anything until attacked, when it turns into a necromancer pixel
        grid[defender_y, defender_x] = -1 * attacker_team # dead pixel
        return

    # Default attack
    grid[defender_y, defender_x] = attacker_team


def run_simulation(grid, grid_width, grid_height, team_classes, hitpoints):
    """
    Runs one "step" of the simulation.
    Now takes grid_width and grid_height as arguments.
    """
    attacker_x, attacker_y = choose_random_pixel(grid_width, grid_height)
    attacker_team = grid[attacker_y, attacker_x]
    if attacker_team < 0:
        return # dead pixel cannot attack
    attacker_class = team_classes[attacker_team]

    attack_range = 1
    if attacker_class == "Sniper" or attacker_class == "Mortar":
        attack_range = 10
    
    defender_x, defender_y = choose_random_nearby_pixel(attacker_y, attacker_x, grid_width, grid_height, range=attack_range)
    defender_team = grid[defender_y, defender_x]

    if attacker_class == "Assassin" and defender_team == attacker_team:
        # retry up to three times
        for _ in range(3):
            defender_y, defender_x = choose_random_nearby_pixel(attacker_y, attacker_x, grid_width, grid_height, range=attack_range)
            defender_team = grid[defender_y, defender_x]
            if defender_team != attacker_team:
                break

    attack(grid, grid_width, grid_height, attacker_y, attacker_x, defender_y, defender_x, team_classes, hitpoints)
    


def format_time(milliseconds):
    """Converts milliseconds to a HH:MM:SS string."""
    seconds = int(milliseconds / 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def load_team_names(filepath, num_teams):
    """
    Loads a list of names from a file and randomly selects the required number.
    Returns a fallback list (e.g., "Team 0") if file is missing or insufficient.
    """
    try:
        with open(filepath, 'r') as f:
            all_names = [line.strip() for line in f if line.strip()]
        
        if len(all_names) < num_teams:
            print(f"Warning: Not enough names in {filepath} (found {len(all_names)}, need {num_teams}).")
            raise ValueError("Not enough names")
            
        return random.sample(all_names, num_teams)
        
    except (IOError, ValueError):
        print(f"Using generic names (e.g., 'Team 0').")
        return [f"Team {i}" for i in range(num_teams)]

def generate_distinct_colors(num_teams):
    """
    Generates a list of perceptually distinct colors using the
    LCHab (Lightness, Chroma, Hue) color space.
    """
    colors_rgb_list = []
    
    for i in range(num_teams):
        hue = i * (360.0 / num_teams)
        lightness = 70.0 if i % 2 == 0 else 55.0
        chroma = 60.0
        lch_color = LCHabColor(lightness, chroma, hue)
        rgb_color = convert_color(lch_color, sRGBColor)
        
        r_clamped = rgb_color.clamped_rgb_r
        g_clamped = rgb_color.clamped_rgb_g
        b_clamped = rgb_color.clamped_rgb_b
        
        r_int = int(r_clamped * 255)
        g_int = int(g_clamped * 255)
        b_int = int(b_clamped * 255)
        
        colors_rgb_list.append((r_int, g_int, b_int))
    
    return np.array(colors_rgb_list, dtype=np.uint8)


def pause_game(screen, clock, pause_font, sim_width, sim_height):
    """
    Pauses the game, freezes the screen, and waits for unpause or quit.
    This function takes over the game loop until it returns.
    Returns 'unpause' or 'quit'.
    """
    # 1. Draw the "PAUSED" overlay ONCE
    # Create a semi-transparent overlay for the sim area
    overlay = pygame.Surface((sim_width, sim_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128)) # 128 is 50% transparency
    screen.blit(overlay, (0, 0))
    
    # Draw the "PAUSED" text
    pause_surf = pause_font.render("PAUSED", True, (255, 255, 255))
    pause_rect = pause_surf.get_rect(center=(sim_width // 2, sim_height // 2))
    screen.blit(pause_surf, pause_rect)

    # 2. Update the display ONCE to show the pause screen
    pygame.display.flip()
    
    # 3. Enter the blocking pause loop
    # This loop does NO drawing and NO logic, only event checking.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return 'unpause' # Exit the pause loop
                if event.key == pygame.K_q:
                    return 'quit'
        
        # 4. Tick the clock to stay responsive without eating CPU
        clock.tick(30) # No need to run at 60 FPS while paused


def main():
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Pixel Fighting Simulation")
    # ... (all arguments are the same) ...
    parser.add_argument(
        '-s', '--grid_size',
        type=int, 
        default=100, 
        help='Side length of the square grid (e.g., 100 for 100x100). Default: 100'
    )
    parser.add_argument(
        '-t', '--num_teams',
        type=int, 
        default=8, 
        help='Number of competing teams/colors. Default: 8'
    )
    parser.add_argument(
        '-u', '--updates_per_frame',
        type=int, 
        default=1000, 
        help='Number of pixel "fights" per frame. Higher is faster. Default: 1000'
    )
    parser.add_argument(
        '-l', '--title',
        type=str,
        default=None,
        help='A specific title for this game run. If not set, a unique title will be auto-generated.'
    )
    parser.add_argument(
        '-p', '--pixels',
        type=int,
        default=760,
        help='Max number of real screen pixels along the grid height. Default: 760'
    )
    parser.add_argument(
        '-f', '--frame_rate',
        type=int,
        default=60,
        help='Frame rate for the simulation. Default: 60'
    )
    args = parser.parse_args()

    # --- Handle Game Title and Filename ---
    # ... (this section is the same) ...
    if args.title:
        game_title = args.title
        game_title_safe = args.title.replace(' ', '_').replace('/', '').replace('\\', '')
    else:
        now = datetime.datetime.now()
        game_title = now.strftime("Game_%Y-%m-%d_%H-M-%S")
        game_title_safe = game_title
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    save_filename = os.path.join(RESULTS_DIR, f"{game_title_safe}.npz")
    
    print(f"--- Starting Game: {game_title} ---")
    print(f"--- Data will be saved to: {save_filename} ---")

    # --- Settings derived from args ---
    # ... (this section is the same) ...
    GRID_WIDTH = args.grid_size
    GRID_HEIGHT = args.grid_size
    NUM_TEAMS = args.num_teams
    UPDATES_PER_FRAME = args.updates_per_frame
    FRAME_RATE = args.frame_rate
    LEADERBOARD_WIDTH = 150
    MAX_REAL_PIXELS = args.pixels
    PIXEL_SIZE = max(1, MAX_REAL_PIXELS // GRID_WIDTH)

    # --- Calculated Settings ---
    SIM_WIDTH = GRID_WIDTH * PIXEL_SIZE
    SIM_HEIGHT = GRID_HEIGHT * PIXEL_SIZE
    WINDOW_WIDTH = SIM_WIDTH + LEADERBOARD_WIDTH
    WINDOW_HEIGHT = SIM_HEIGHT
    TOTAL_PIXELS = GRID_WIDTH * GRID_HEIGHT
    
    # --- Pygame & Grid Setup ---
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"Pixels Fighting: {game_title} (R to Reset, P to Pause)")
    clock = pygame.time.Clock()

    # --- Font Setup ---
    ui_font = pygame.font.SysFont(None, 24)
    elim_font = pygame.font.SysFont(None, 20)
    final_font_big = pygame.font.SysFont(None, 100)
    final_font_small = pygame.font.SysFont(None, 70)
    comeback_font = pygame.font.SysFont(None, 50)
    pause_font = pygame.font.SysFont(None, 80)
    text_color = (255, 255, 255)
    elim_text_color = (0, 0, 0)
    percent_text_color = (255, 255, 255)

    # --- Simulation State ---
    grid = init_grid(GRID_WIDTH, GRID_HEIGHT, NUM_TEAMS)
    colors = generate_distinct_colors(NUM_TEAMS)
    dead_color = (173, 173, 173) # Gray for dead pixels
    team_names = load_team_names(TEAM_NAMES_FILE, NUM_TEAMS)
    color_surface_array = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3), dtype=np.uint8)

    # --- Classes ---
    TEAM_CLASSES = {}
    possible_classes = ["Berserker", "Sniper", "Assassin", "Bunker", "Phalanx", "Thorns", "Plague", "Nomad", "Necromancer", "Healer", "Mortar"]
    HITPOINTS = {i: 0 for i in range(NUM_TEAMS)} # Track hitpoints for each team

    for i in range(NUM_TEAMS):
        TEAM_CLASSES[i] = random.choice(possible_classes)
    
    # --- Game State Variables ---
    frame_count = 0
    start_time = pygame.time.get_ticks()
    simulation_running = True
    elapsed_ms = 0
    
    team_active = [True] * NUM_TEAMS
    elimination_times = [None] * NUM_TEAMS
    team_low_percents = np.full(NUM_TEAMS, 1.0)
    team_high_percents = np.zeros(NUM_TEAMS)
    elimination_order = []
    
    history_data = []

    # --- Final State Variables ---
    final_time_string = ""
    winner_color = (0,0,0)
    final_fps_string = ""
    final_timer_string = ""
    final_frames_string = ""
    final_lowest_string = ""

    running = True
    while running:
        # --- Event Handling (Always runs) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # --- RESET ---
                    if args.title:
                        game_title = args.title + " (Reset)"
                        game_title_safe = args.title.replace(' ', '_').replace('/', '').replace('\\', '') + "_Reset"
                    else:
                        now = datetime.datetime.now()
                        game_title = now.strftime("Game_%Y-%m-%d_%H-M-%S")
                        game_title_safe = game_title
                    
                    save_filename = os.path.join(RESULTS_DIR, f"{game_title_safe}.npz")
                    pygame.display.set_caption(f"Pixels Fighting: {game_title} (R to Reset, P to Pause)")
                    print(f"--- RESET: Starting New Game: {game_title} ---")
                    print(f"--- Data will be saved to: {save_filename} ---")

                    grid = init_grid(GRID_WIDTH, GRID_HEIGHT, NUM_TEAMS)
                    team_names = load_team_names(TEAM_NAMES_FILE, NUM_TEAMS)
                    frame_count = 0
                    start_time = pygame.time.get_ticks()
                    simulation_running = True
                    elapsed_ms = 0
                    team_active = [True] * NUM_TEAMS
                    elimination_times = [None] * NUM_TEAMS
                    team_low_percents = np.full(NUM_TEAMS, 1.0)
                    team_high_percents = np.zeros(NUM_TEAMS)
                    elimination_order = []
                    history_data = []  
                    final_time_string = ""
                    final_fps_string = ""
                    final_timer_string = ""
                    final_frames_string = ""
                    final_lowest_string = ""
                
                if event.key == pygame.K_q:
                    running = False
                
                if event.key == pygame.K_p:
                    # Call the blocking pause function
                    pause_result = pause_game(screen, clock, pause_font, SIM_WIDTH, SIM_HEIGHT)
                    
                    if pause_result == 'quit':
                        running = False
                    
                    # When we unpause, we must correct the timer
                    # 'elapsed_ms' holds the time from *before* the pause.
                    # We reset 'start_time' to be the new 'now' MINUS
                    # the elapsed time, so the timer resumes correctly.
                    start_time = pygame.time.get_ticks() - elapsed_ms

        # --- Timer Logic (Only if running) ---
        if simulation_running:
            elapsed_ms = pygame.time.get_ticks() - start_time
            current_time_string = format_time(elapsed_ms)

        # --- Simulation Logic (Only if running) ---
        if simulation_running:
            for _ in range(UPDATES_PER_FRAME):
                run_simulation(grid, GRID_WIDTH, GRID_HEIGHT, TEAM_CLASSES, HITPOINTS)
            frame_count += 1
            
            filtered_grid = grid[grid >= 0] # Exclude dead pixels
            counts = np.bincount(filtered_grid.ravel(), minlength=NUM_TEAMS)
            
            current_percents = counts / TOTAL_PIXELS
            history_data.append(current_percents)
            
            team_low_percents = np.minimum(team_low_percents, current_percents)
            team_high_percents = np.maximum(team_high_percents, current_percents)

            active_team_count = 0
            for i in range(NUM_TEAMS):
                if team_active[i]:
                    if counts[i] == 0: # Team was just eliminated
                        team_active[i] = False
                        elimination_order.append(i)
                        max_percent = team_high_percents[i]
                        elimination_times[i] = (
                            f"Elim at: {current_time_string}", 
                            f"Max: {max_percent * 100:.1f}%"
                        )
                    else:
                        active_team_count += 1
            
            if active_team_count == 1:
                simulation_running = False
                final_time_string = current_time_string
                winner_team_index = team_active.index(True)
                winner_color = colors[winner_team_index]
                
                final_fps_string = f"FPS: {clock.get_fps():.1f}"
                final_timer_string = current_time_string
                final_frames_string = f"Frames: {frame_count}"
                
                winner_lowest_percent = team_low_percents[winner_team_index]
                final_lowest_string = f"Comeback From: {winner_lowest_percent * 100:.1f}%"
                
                try:
                    print("Simulation ended. Saving data...")
                    final_data_array = np.array(history_data)
                    np.savez_compressed(
                        save_filename, 
                        history=final_data_array, 
                        colors=colors, 
                        names=team_names
                    )
                    print(f"Data saved to '{save_filename}' with shape {final_data_array.shape}")
                except Exception as e:
                    print(f"Error saving data: {e}")
                
        else: 
            # Simulation is not running (game has ended)
            filtered_grid = grid[grid >= 0] # Exclude dead pixels
            counts = np.bincount(filtered_grid.ravel(), minlength=NUM_TEAMS)

        # --- Leaderboard Drawing Logic (Always runs) ---
        # ... (this section is the same) ...
        leaderboard_x_start = SIM_WIDTH
        pygame.draw.rect(
            screen, (0, 0, 0),
            (leaderboard_x_start, 0, LEADERBOARD_WIDTH, WINDOW_HEIGHT)
        )
        
        bar_padding = 2
        text_y_offset = 60
        bar_area_height = WINDOW_HEIGHT - text_y_offset
        bar_slot_height = bar_area_height / NUM_TEAMS
        bar_draw_height = bar_slot_height - bar_padding
        
        active_team_indices = [i for i in range(NUM_TEAMS) if team_active[i]]
        sorted_active_indices = sorted(active_team_indices, key=lambda i: counts[i], reverse=True)
        draw_order_indices = sorted_active_indices + list(reversed(elimination_order))

        for slot, i in enumerate(draw_order_indices):
            bar_y = (slot * bar_slot_height) + text_y_offset
            bg_bar_rect = pygame.Rect(
                leaderboard_x_start + 2, bar_y, LEADERBOARD_WIDTH - 4, bar_draw_height
            )

            if team_active[i]:
                percent = counts[i] / TOTAL_PIXELS
                color = colors[i]
                filled_width = int(percent * (LEADERBOARD_WIDTH - 4))
                
                pygame.draw.rect(screen, (40, 40, 40), bg_bar_rect)
                
                fill_bar_rect = pygame.Rect(
                    leaderboard_x_start + 2, bar_y, filled_width, bar_draw_height
                )
                pygame.draw.rect(screen, color, fill_bar_rect)
                
                name_surf = elim_font.render(team_names[i] + " (" + TEAM_CLASSES[i] + ")", True, percent_text_color)
                name_rect = name_surf.get_rect(
                    centery=bg_bar_rect.centery - 7, 
                    left=bg_bar_rect.left + 5
                )
                screen.blit(name_surf, name_rect)

                percent_string = f"{percent * 100:.1f}%"
                percent_surf = elim_font.render(percent_string, True, percent_text_color)
                
                percent_rect = percent_surf.get_rect(
                    centery=bg_bar_rect.centery + 7,
                    right=bg_bar_rect.right - 5
                )
                screen.blit(percent_surf, percent_rect)
                
            else:
                color = colors[i]
                pygame.draw.rect(screen, color, bg_bar_rect) 
                
                name_surf = elim_font.render(team_names[i] + " (" + TEAM_CLASSES[i] + ")", True, elim_text_color)
                name_rect = name_surf.get_rect(
                    center=(bg_bar_rect.centerx, bg_bar_rect.centery - 10)
                )
                screen.blit(name_surf, name_rect)

                elim_time_str, elim_max_str = elimination_times[i]
                
                elim_surf_1 = elim_font.render(elim_time_str, True, elim_text_color)
                elim_rect_1 = elim_surf_1.get_rect(center=(bg_bar_rect.centerx, bg_bar_rect.centery + 2))
                screen.blit(elim_surf_1, elim_rect_1)
                
                elim_surf_2 = elim_font.render(elim_max_str, True, elim_text_color)
                elim_rect_2 = elim_surf_2.get_rect(center=(bg_bar_rect.centerx, bg_bar_rect.centery + 14))
                screen.blit(elim_surf_2, elim_rect_2)

        # --- Simulation Drawing Logic (Always runs) ---
        color_surface_array[...] = colors[grid]
        negative_mask = (grid < 0)
        color_surface_array[negative_mask] = dead_color
        surface = pygame.surfarray.make_surface(np.transpose(color_surface_array, (1, 0, 2)))
        scaled_surface = pygame.transform.scale(surface, (SIM_WIDTH, SIM_HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        # --- UI Text Drawing (Handles both running and frozen) ---
        text_x = leaderboard_x_start + 5
        
        if simulation_running:
            fps_string = f"FPS: {clock.get_fps():.1f}"
            timer_string = current_time_string
            frames_string = f"Frames: {frame_count}"
        else:
            fps_string = final_fps_string
            timer_string = final_timer_string
            frames_string = final_frames_string

        fps_text_surf = ui_font.render(fps_string, True, text_color)
        screen.blit(fps_text_surf, (text_x, 5))

        timer_text_surf = ui_font.render(timer_string, True, text_color)
        screen.blit(timer_text_surf, (text_x, 25))

        frames_text_surf = ui_font.render(frames_string, True, text_color)
        screen.blit(frames_text_surf, (text_x, 45))
        
        # --- Win Screen Drawing (Only if sim is not running) ---
        if not simulation_running:
            # ... (this section is the same) ...
            win_surf = final_font_big.render("WINNER!", True, winner_color)
            win_rect = win_surf.get_rect(center=(SIM_WIDTH // 2, SIM_HEIGHT // 2 - 60))
            
            outline_surf = final_font_big.render("WINNER!", True, (0,0,0))
            screen.blit(outline_surf, win_rect.move(3,3))
            screen.blit(win_surf, win_rect)

            time_surf = final_font_small.render(final_time_string, True, text_color)
            time_rect = time_surf.get_rect(center=(SIM_WIDTH // 2, SIM_HEIGHT // 2 + 10))
            
            outline_surf_small = final_font_small.render(final_time_string, True, (0,0,0))
            screen.blit(outline_surf_small, time_rect.move(2,2))
            screen.blit(time_surf, time_rect)

            comeback_surf = comeback_font.render(final_lowest_string, True, text_color)
            comeback_rect = comeback_surf.get_rect(center=(SIM_WIDTH // 2, SIM_HEIGHT // 2 + 60))
            
            outline_surf_comeback = comeback_font.render(final_lowest_string, True, (0,0,0))
            screen.blit(outline_surf_comeback, comeback_rect.move(2,2))
            screen.blit(comeback_surf, comeback_rect)
        
        # --- Final Update (Always runs) ---
        pygame.display.flip()
        clock.tick(FRAME_RATE) 

    pygame.quit()

if __name__ == "__main__":
    main()