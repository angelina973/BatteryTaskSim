import matplotlib.pyplot as plt
import numpy as np
from preprocess import preprocess_variable

def extract_and_plot_variables(solution, parameter_values, battery_info, plot=False):
    """
    提取变量并（可选）绘制曲线，支持多任务仿真结果的拼接。
    """
    # 初始化变量
    initial_soh = battery_info.get("SOH", 100.0)
    initial_temperature = battery_info.get("Temperature", 298.15)  # 开尔文
    initial_sei_resistivity = battery_info.get("SEI_resistivity", 1e5)

    # 提取时间序列并转换为小时
    time_data = solution["Time [s]"].data / 3600

    # 定义需要提取的变量
    variables_to_extract = {
        "SOC": "X-averaged negative particle surface concentration [mol.m-3]",
        "SOH": "Loss of lithium inventory [%]",
        "Temperature (°C)": "Cell temperature [K]",
        "Resistance (Ohm)": None,  # 估算的内阻
    }

    results = {"Time [h]": time_data}  # 初始化时间序列

    # 提取变量并验证初始条件
    for var_name, variable in variables_to_extract.items():
        # 提取并计算变量
        results[var_name] = calculate_variable(
            solution, parameter_values, time_data, var_name, variable,
            initial_soh, initial_sei_resistivity
        )

        # 验证初始条件一致性
        validate_initial_condition(var_name, results[var_name], battery_info)
    return results


def calculate_variable(solution, parameter_values, time_data, var_name, variable, initial_soh, initial_sei_resistivity):
    """
    计算指定变量值。
    """
    if variable:
        var_data = preprocess_variable(solution, variable, time_data)
        if var_name == "SOC":
            max_conc = parameter_values["Maximum concentration in negative electrode [mol.m-3]"]
            return var_data / max_conc  # 归一化 SOC
        elif var_name == "SOH":
            return initial_soh - var_data  # 计算剩余 SOH
        elif var_name == "Temperature (°C)":
            return var_data - 273.15  # 从 Kelvin 转换为摄氏度
    else:
        sei_resistivity = initial_sei_resistivity + 1e3 * np.cumsum(np.gradient(
            preprocess_variable(solution, "Loss of lithium inventory [%]", time_data)
        ))
        return sei_resistivity / 1e6  # 转换为 Ohm


def validate_initial_condition(var_name, var_data, battery_info):
    tolerance = 0.1  # 增加容忍误差范围
    expected = battery_info.get(var_name, None)
    if expected is not None:
        actual = var_data[0]
        if not np.isclose(expected, actual, atol=tolerance):
            print(f"WARNING: {var_name} initial condition mismatch. Expected: {expected}, Actual: {actual}")

