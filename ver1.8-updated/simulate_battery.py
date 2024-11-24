import numpy as np
from setup_model import setup_battery_model
from run_simulation import run_simulation
from extract_plot import  extract_and_plot_variables

def simulate_battery(battery_info, tasks):
    """
    针对单块电池运行分配的任务，并提取详细仿真数据。
    """
    if not tasks:
        print(f"Battery has no tasks assigned. Skipping simulation.")
        return {
            "Time [h]": np.array([]),  # 添加空时间序列
            "SOC": np.array([]),
            "SOH": np.array([]),
            "Temperature (°C)": np.array([]),
            "Resistance (Ohm)": np.array([]),
        }

    # 构建模型和参数
    model, param = setup_battery_model(battery_info)
    experiments = [(task["power"], task["time"]) for task in tasks]
    solution, parameter_values = run_simulation(model, param, experiments)

    # 提取并返回详细变量数据
    results = extract_and_plot_variables(solution, parameter_values, battery_info)
    return results
