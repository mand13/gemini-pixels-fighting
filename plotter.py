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
        help=f'Specific .npy file to plot (e.g., "Game_2025-10-31.npy"). Must be inside the "{RESULTS_DIR}" folder. If not set, the most recent file will be plotted.'
    )
    args = parser.parse_args()
    # --- END MODIFIED ---

    # --- MODIFIED: Logic to find the correct data file ---
    data_file = ""
    
    if args.file:
        # User specified a file
        data_file = os.path.join(RESULTS_DIR, args.file)
        if not os.path.exists(data_file):
            print(f"Error: File not found: {data_file}")
            print(f"Please make sure the file '{args.file}' is inside the '{RESULTS_DIR}' directory.")
            return
    else:
        # User did not specify. Find the most recent.
        print("No file specified. Finding most recent results file...")
        list_of_files = glob.glob(os.path.join(RESULTS_DIR, '*.npy'))
        
        if not list_of_files:
            print(f"Error: No .npy files found in '{RESULTS_DIR}'.")
            print("Please run the 'pixels_fighting.py' simulation first.")
            return
        
        data_file = max(list_of_files, key=os.path.getctime)
        print(f"Found most recent file: {data_file}")
    # --- END MODIFIED ---

    print(f"Loading data from {data_file}...")
    # 2. Load the saved NumPy data
    data_wide = np.load(data_file)
    
    # 3. Convert to a Pandas DataFrame for easier manipulation
    df_wide = pd.DataFrame(data_wide)

    # 4. Reshape data from "wide" to "long" format
    df_wide = df_wide.reset_index() # Adds an 'index' column (our frames)
    df_wide = df_wide.rename(columns={'index': 'Frame'})
    df_long = df_wide.melt(
        id_vars=['Frame'], 
        var_name='Team', 
        value_name='Percentage'
    )
    
    # Convert 'Team' to a string, so Plotly treats it as a category (not a number)
    df_long['Team'] = df_long['Team'].astype(str)

    print("Data loaded and reshaped. Generating plot...")

    # --- MODIFIED: Use the filename to create a dynamic title ---
    plot_title_name = os.path.basename(data_file).replace('.npy', '')
    fig = px.line(
        df_long,
        x='Frame',
        y='Percentage',
        color='Team',
        title=f'Pixel Fighting: Team Control Over Time<br><i>{plot_title_name}</i>'
    )
    # --- END MODIFIED ---
    
    # 6. Customize the plot
    fig.update_layout(yaxis_tickformat='.1%')
    fig.update_traces(
        hovertemplate="<b>Team %{color}</b><br>Frame: %{x}<br>Percentage: %{y:.2%}"
    )

    print("Plot generated. Opening in your browser...")
    # 7. Show the plot!
    fig.show()

if __name__ == "__main__":
    main()