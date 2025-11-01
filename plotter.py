import plotly.express as px
import pandas as pd
import numpy as np
import os
import argparse  # <-- MODIFIED
import glob      # <-- MODIFIED

# --- Settings ---
RESULTS_DIR = 'pixels_fighting_results'  # <-- MODIFIED

def main():
    # --- MODIFIED: Add argument parsing ---
    parser = argparse.ArgumentParser(description="Plot Pixel Fighting simulation results.")
    parser.add_argument(
        '-f', '--file', 
        type=str, 
        default=None, 
        help=f'Specific .npz file to plot (e.g., "Game_2025-10-31.npz"). Must be inside the "{RESULTS_DIR}" folder. If not set, the most recent file will be plotted.'
    )
    args = parser.parse_args()
    # --- END MODIFIED ---

    # --- MODIFIED: Logic to find the correct data file ---
    data_file = ""
    
    if args.file:
        # User specified a file
        filename = args.file
        # Automatically add .npz extension if it's missing
        if not filename.endswith('.npz'):
            filename = filename + '.npz'
            
        data_file = os.path.join(RESULTS_DIR, filename)
        
        if not os.path.exists(data_file):
            print(f"Error: File not found: {data_file}")
            print(f"Please make sure the file '{args.file}' is inside the '{RESULTS_DIR}' directory.")
            return
    else:
        # User did not specify. Find the most recent.
        print("No file specified. Finding most recent results file...")
        list_of_files = glob.glob(os.path.join(RESULTS_DIR, '*.npz'))
        
        if not list_of_files:
            print(f"Error: No .npz files found in '{RESULTS_DIR}'.")
            print("Please run the 'pixels_fighting.py' simulation first.")
            return
    # --- MODIFIED: Load .npz file and extract all arrays ---
    print(f"Loading data from {data_file}...")
    # 2. Load the saved .npz data
    #    data is a dict-like object {'history': ..., 'colors': ..., 'names': ...}
    try:
        data = np.load(data_file, allow_pickle=True)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}")
        return

    data_wide = data['history']
    
    # 3. Get team colors and names, with fallbacks for old files
    num_teams = data_wide.shape[1]
    
    if 'names' in data:
        team_names = data['names']
    else:
        print("Warning: 'names' array not in data file. Using generic names.")
        team_names = [f"Team {i}" for i in range(num_teams)]

    if 'colors' in data:
        colors_rgb = data['colors']
        # Create a color map for Plotly: {'Team Name': 'rgb(R, G, B)'}
        color_map = {
            team_names[i]: f'rgb({r}, {g}, {b})' 
            for i, (r, g, b) in enumerate(colors_rgb)
        }
    else:
        print("Warning: 'colors' array not in data file. Using default palette.")
        color_map = {} # Let Plotly use its default colors
    
    # --- END MODIFIED ---
    
    df_wide = pd.DataFrame(data_wide)

    # 4. Reshape data from "wide" to "long" format
    df_wide = df_wide.reset_index() # Adds an 'index' column (our frames)
    df_wide = df_wide.rename(columns={'index': 'Frame'})
    df_long = df_wide.melt(
        id_vars=['Frame'], 
        var_name='Team', 
        value_name='Percentage'
    )
    
    # --- MODIFIED: Map team index (0, 1, ..) to the loaded names
    # Create a mapping dict: {0: 'Lion', 1: 'Tiger', ...}
    name_map = {i: team_names[i] for i in range(num_teams)}
    df_long['Team Name'] = df_long['Team'].astype(int).map(name_map)
    # --- END MODIFIED ---

    print("Data loaded and reshaped. Generating plot...")

    # --- MODIFIED: Use the filename to create a dynamic title ---
    plot_title_name = os.path.basename(data_file).replace('.npz', '')
    fig = px.line(
         df_long,
         x='Frame',
         y='Percentage',
        color='Team Name',  # Use the new 'Team Name' column for the legend
        title=f'Pixel Fighting: Team Control Over Time<br><i>{plot_title_name}</i>',
        color_discrete_map=color_map # Apply the exact RGB colors
    )
    # --- END MODIFIED ---
    
    # 6. Customize the plot
    fig.update_layout(yaxis_tickformat='.1%')
    fig.update_traces(
        # Use 'customdata' to show the correct team name (color) in the hover
        hovertemplate="<b>%{data.name}</b><br>Frame: %{x}<br>Percentage: %{y:.2%}"
    )

    print("Plot generated. Opening in your browser...")
    # 7. Show the plot!
    fig.show()

if __name__ == "__main__":
    main()


