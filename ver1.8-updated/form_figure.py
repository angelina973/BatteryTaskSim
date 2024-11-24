import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

# Define function to automatically parse filenames and load data
def load_and_prepare_data(file_paths):
    data_frames = []
    for path in file_paths:
        # Automatically extract battery and temperature info from filename
        parts = os.path.basename(path).split("_")
        battery, temp = parts[1], parts[2].replace("results.csv", "")
        df = pd.read_csv(path)
        df["Battery"] = battery
        df["Temperature"] = temp
        data_frames.append(df)
    # Combine all data into one DataFrame
    return pd.concat(data_frames, ignore_index=True)

# Define function to plot data
def plot_data(data, parameters, labels):
    # Generate consistent colors based on unique temperatures
    unique_temperatures = data["Temperature"].unique()
    color_map = {
        temp: list(mcolors.TABLEAU_COLORS.values())[i % len(mcolors.TABLEAU_COLORS)]
        for i, temp in enumerate(unique_temperatures)
    }

    # Plot each parameter
    for param, label in zip(parameters, labels):
        plt.figure(figsize=(10, 6))
        for (battery, temperature), group in data.groupby(["Battery", "Temperature"]):
            # Format temperature for display
            formatted_temp = f"{int(float(temperature[:-1]))}°C"
            color = color_map[temperature]  # Assign consistent color
            alpha = 0.3 + 0.2 * int(battery)  # Adjust alpha for battery differentiation
            plt.plot(group["Time [h]"], group[param], label=f"Battery {battery}, {formatted_temp}",
                     color=color, alpha=alpha)
        plt.title(f"{label} vs Time", fontsize=14)
        plt.xlabel("Time [h]", fontsize=12)
        plt.ylabel(label, fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
        plt.gca().spines['top'].set_visible(True)
        plt.gca().spines['right'].set_visible(True)
        plt.gca().spines['left'].set_linewidth(1.2)
        plt.gca().spines['bottom'].set_linewidth(1.2)
        plt.tight_layout()
        plt.show()

# Define list of CSV file paths (replace with your actual file paths)
file_paths = [
    "/mnt/data/Battery_3_-0.0C_results.csv",
    "/mnt/data/Battery_3_15.0C_results.csv",
    "/mnt/data/Battery_3_20.0C_results.csv",
    "/mnt/data/Battery_1_-0.0C_results.csv",
    "/mnt/data/Battery_1_15.0C_results.csv",
    "/mnt/data/Battery_1_20.0C_results.csv",
    "/mnt/data/Battery_2_-0.0C_results.csv",
    "/mnt/data/Battery_2_15.0C_results.csv",
    "/mnt/data/Battery_2_20.0C_results.csv"
]

# Load and prepare data
combined_data = load_and_prepare_data(file_paths)

# Define parameters and their labels
parameters = ["SOC", "SOH", "Resistance (Ohm)", "Temperature (°C)"]
labels = ["State of Charge (SOC)", "State of Health (SOH)", "Resistance (Ohm)", "Temperature (°C)"]

# Plot the data
plot_data(combined_data, parameters, labels)
