
# BatteryTaskSim

**BatteryTaskSim** is a Python framework focused on task allocation and thermal simulation for batteries based on Pybamm. It supports multi-battery task allocation, simulation, data visualization, and result export.

---

## Directory Structure

- **simulation_data/**
  - Stores all simulation results exported as CSV files for offline analysis.
- **assign_tasks.py**
  - Implements task allocation logic by dynamically assigning tasks based on priority, battery health, and temperature conditions.
- **extract_plot.py**
  - Extracts variables (e.g., SOC, SOH, temperature) from simulation results and supports data visualization and CSV export.
- **is_task_feasible.py**
  - Checks whether a task is suitable for a specific battery based on available capacity, health status, and temperature limits.
- **main.py**
  - Main entry point. Executes task allocation, simulation runs, and result output (including Gantt charts and simulation curves).
- **plot_gantt_chart.py**
  - Generates Gantt charts to visually display task allocation and timing across batteries.
- **plot_results.py**
  - Plots simulation results and saves them as CSV files for offline analysis.
- **preprocess.py**
  - Provides data preprocessing tools to align simulation variables with time and handle multidimensional data.
- **print_assignment_results.py**
  - Outputs task allocation results, detailing task assignment to batteries by time, power, and priority.
- **run_simulation.py**
  - Runs battery simulations using PyBaMM models, supporting multi-tasking and dynamic thermal models.
- **scores.py**
  - Provides battery scoring functions for dynamic decision-making in task allocation.
- **setup_model.py**
  - Configures battery models and parameters, supporting thermal model upgrades from "Lumped" to "x-lumped".
- **simulate_battery.py**
  - Runs multi-task simulations for individual batteries, returning key metrics like SOC, SOH, and temperature.
- **sort_tasks.py**
  - Sorts tasks by priority, ensuring high-priority tasks are allocated first.
- **update_battery_health.py**
  - Dynamically updates battery states, including SOC, SOH, and temperature, based on task results.

---

## Features

1. **Task Allocation**
   - Dynamically assigns tasks to multiple batteries.
   - Considers battery health (SOC, SOH, temperature) and task requirements (power, duration, priority).

2. **Thermal Model Simulation**
   - Supports thermal model upgrades from Lumped to x-lumped, enabling precise thermal behavior simulations.
   - Allows dynamic parameter configuration based on battery dimensions and geometry.

3. **Result Visualization and Export**
   - Automatically generates Gantt charts to display task allocation.
   - Extracts and plots SOC, SOH, temperature trends over time.
   - Exports all simulation data as CSV files for offline analysis.

---

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BatteryTaskSim.git
   cd BatteryTaskSim
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install matplotlib numpy pybamm pandas
   ```
4. Run the main program:
   ```bash
   python main.py
   ```

---

## Outputs

- **Gantt Chart**: Displays task allocation and battery usage over time.
- **Simulation Data**: Exports detailed time-series data (SOC, SOH, temperature, etc.) as CSV files.
- **Simulation Curves**: Plots trends of battery states over time.

---

## Use Cases

- **Electric Vehicle (EV) Task Scheduling**: Optimizes charging and discharging strategies to extend battery lifespan.
- **Energy Storage System (ESS) Analysis**: Task scheduling and battery thermal behavior simulation.
- **Research and Teaching**: Supports battery modeling and thermal simulation in academic environments.

---

## Future Plans

1. Add support for more battery chemistries, such as solid-state or lithium iron phosphate batteries.
2. Integrate advanced scheduling algorithms, such as real-time load balancing.
3. Expand environmental simulation, including cooling and temperature gradient modeling.

---

## Contribution

We welcome contributions and feedback! If you encounter any issues or have feature requests, feel free to submit an Issue on GitHub.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it.
