import pygame
import numpy as np
import random
import colorsys
import argparse
import datetime  # <-- MODIFIED
import os        # <-- MODIFIED
from colormath.color_objects import sRGBColor, LCHabColor  
from colormath.color_conversions import convert_color     

# --- Settings ---
RESULTS_DIR = "pixels_fighting_results"  # <-- MODIFIED: New directory for results
TEAM_NAMES_FILE = "team_names.txt"  # <-- MODIFIED: New file for names

def init_grid(width, height, num_teams):
    """Creates a new grid with random team assignments."""
    return np.random.randint(0, num_teams, size=(height, width), dtype=np.int32)

def run_simulation(grid, num_teams, grid_width, grid_height):
    """
    Runs one "step" of the simulation.
    Now takes grid_width and grid_height as arguments.
    """
    attacker_y = random.randint(0, grid_height - 1)
    attacker_x = random.randint(0, grid_width - 1)
    attacker_team = grid[attacker_y, attacker_x]
    
    defender_dy = random.randint(-1, 1)
    defender_dx = random.randint(-1, 1)
    
    if defender_dy == 0 and defender_dx == 0:
        return

    defender_y = (attacker_y + defender_dy) % grid_height
    defender_x = (attacker_x + defender_dx) % grid_width
    
    grid[defender_y, defender_x] = attacker_team

def format_time(milliseconds):
    """Converts milliseconds to a HH:MM:SS string."""
    seconds = int(milliseconds / 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# --- MODIFIED: New function to load team names ---
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
            
        # Select a random sample of unique names
        return random.sample(all_names, num_teams)
        
    except (IOError, ValueError):
        # Fallback to generic names
        print(f"Using generic names (e.g., 'Team 0').")
        return [f"Team {i}" for i in range(num_teams)]
# --- END MODIFIED ---

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


def main():
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Pixel Fighting Simulation")
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
    # --- MODIFIED: Added title argument ---
    parser.add_argument(
        '-l', '--title',
        type=str,
        default=None,
        help='A specific title for this game run. If not set, a unique title will be auto-generated.'
    )
    # --- END MODIFIED ---
    args = parser.parse_args()

    # --- MODIFIED: Handle Game Title and Filename ---
    if args.title:
        game_title = args.title
        # Simple sanitize for filename: replace spaces, remove slashes
        game_title_safe = args.title.replace(' ', '_').replace('/', '').replace('\\', '')
    else:
        # Auto-generate a unique title based on time
        now = datetime.datetime.now()
        game_title = now.strftime("Game_%Y-%m-%d_%H-M-%S")
        game_title_safe = game_title  # This is already file-safe
    
    # Create the results directory if it doesn't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    # Define the final save path
    save_filename = os.path.join(RESULTS_DIR, f"{game_title_safe}.npz") # <-- MODIFIED: Switched to .npz
    
    print(f"--- Starting Game: {game_title} ---")
    print(f"--- Data will be saved to: {save_filename} ---")
    # --- END MODIFIED ---

    # --- Settings derived from args ---
    GRID_WIDTH = args.grid_size
    GRID_HEIGHT = args.grid_size
    NUM_TEAMS = args.num_teams
    UPDATES_PER_FRAME = args.updates_per_frame
    FRAME_RATE = 60
    LEADERBOARD_WIDTH = 150
    PIXEL_SIZE = max(1, 760 // GRID_WIDTH)

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
    # --- MODIFIED: Use game_title in window caption ---
    pygame.display.set_caption(f"Pixels Fighting: {game_title} (SPACE to Reset)")
    # --- END MODIFIED ---
    clock = pygame.time.Clock()

    # --- Font Setup ---
    ui_font = pygame.font.SysFont(None, 24)
    elim_font = pygame.font.SysFont(None, 20)
    final_font_big = pygame.font.SysFont(None, 100)
    final_font_small = pygame.font.SysFont(None, 70)
    comeback_font = pygame.font.SysFont(None, 50)
    text_color = (255, 255, 255)
    elim_text_color = (0, 0, 0)
    percent_text_color = (255, 255, 255)

    # --- Simulation State ---
    grid = init_grid(GRID_WIDTH, GRID_HEIGHT, NUM_TEAMS)
    colors = generate_distinct_colors(NUM_TEAMS)
    team_names = load_team_names(TEAM_NAMES_FILE, NUM_TEAMS) # <-- MODIFIED: Load names
    color_surface_array = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3), dtype=np.uint8)
    
    # --- Game State Variables ---
    frame_count = 0
    start_time = pygame.time.get_ticks()
    simulation_running = True
    
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
                if event.key == pygame.K_SPACE:
                    # --- RESET ---
                    # --- MODIFIED: Must re-generate titles on reset ---
                    if args.title:
                        game_title = args.title + " (Reset)"
                        game_title_safe = args.title.replace(' ', '_').replace('/', '').replace('\\', '') + "_Reset"
                    else:
                        now = datetime.datetime.now()
                        game_title = now.strftime("Game_%Y-%m-%d_%H-%M-%S")
                        game_title_safe = game_title
                    
                    save_filename = os.path.join(RESULTS_DIR, f"{game_title_safe}.npz") # <-- MODIFIED: Switched to .npz
                    pygame.display.set_caption(f"Pixels Fighting: {game_title} (SPACE to Reset)")
                    print(f"--- RESET: Starting New Game: {game_title} ---")
                    print(f"--- Data will be saved to: {save_filename} ---")
                    # --- END MODIFIED ---

                    grid = init_grid(GRID_WIDTH, GRID_HEIGHT, NUM_TEAMS)
                    colors = generate_distinct_colors(NUM_TEAMS)
                    team_names = load_team_names(TEAM_NAMES_FILE, NUM_TEAMS) # <-- MODIFIED: Reload names
                    frame_count = 0
                    start_time = pygame.time.get_ticks()
                    simulation_running = True
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
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Timer Logic (Only if running) ---
        if simulation_running:
            elapsed_ms = pygame.time.get_ticks() - start_time
            current_time_string = format_time(elapsed_ms)

        # --- Simulation Logic (Only if running) ---
        if simulation_running:
            for _ in range(UPDATES_PER_FRAME):
                run_simulation(grid, NUM_TEAMS, GRID_WIDTH, GRID_HEIGHT)
            frame_count += 1
            
            counts = np.bincount(grid.ravel(), minlength=NUM_TEAMS)
            
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
                
                # --- MODIFIED: Save data to file when sim ends ---
                try:
                    print("Simulation ended. Saving data...")
                    final_data_array = np.array(history_data)
                    # Use np.savez_compressed to save multiple arrays into one file
                    np.savez_compressed(
                        save_filename, 
                        history=final_data_array, 
                        colors=colors, 
                        names=team_names
                    )
                    print(f"Data saved to '{save_filename}' with shape {final_data_array.shape}")
                except Exception as e:
                    print(f"Error saving data: {e}")
                # --- END MODIFIED ---
                
        else: 
            counts = np.bincount(grid.ravel(), minlength=NUM_TEAMS)

        # --- Leaderboard Drawing Logic (Always runs) ---
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
                
                # --- MODIFIED: Show name on leaderboard ---
                name_surf = elim_font.render(team_names[i], True, percent_text_color)
                name_rect = name_surf.get_rect(
                    centery=bg_bar_rect.centery - 7, 
                    left=bg_bar_rect.left + 5
                )
                screen.blit(name_surf, name_rect)

                percent_string = f"{percent * 100:.1f}%"
                percent_surf = elim_font.render(percent_string, True, percent_text_color)
                
                percent_rect = percent_surf.get_rect(
                    centery=bg_bar_rect.centery + 7, # Move percent down
                    right=bg_bar_rect.right - 5
                )
                # --- END MODIFIED ---
                screen.blit(percent_surf, percent_rect)
                
            else:
                color = colors[i]
                pygame.draw.rect(screen, color, bg_bar_rect) 
                
                # --- MODIFIED: Keep team name visible after elimination ---
                name_surf = elim_font.render(team_names[i], True, elim_text_color)
                name_rect = name_surf.get_rect(
                    center=(bg_bar_rect.centerx, bg_bar_rect.centery - 10)
                )
                screen.blit(name_surf, name_rect)
                # --- END MODIFIED ---

                elim_time_str, elim_max_str = elimination_times[i]
                
                elim_surf_1 = elim_font.render(elim_time_str, True, elim_text_color)
                # --- MODIFIED: Adjusted position ---
                elim_rect_1 = elim_surf_1.get_rect(center=(bg_bar_rect.centerx, bg_bar_rect.centery + 2))
                screen.blit(elim_surf_1, elim_rect_1)
                
                elim_surf_2 = elim_font.render(elim_max_str, True, elim_text_color)
                # --- MODIFIED: Adjusted position ---
                elim_rect_2 = elim_surf_2.get_rect(center=(bg_bar_rect.centerx, bg_bar_rect.centery + 14))
                screen.blit(elim_surf_2, elim_rect_2)

        # --- Simulation Drawing Logic (Always runs) ---
        color_surface_array[...] = colors[grid]
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