import matplotlib.pyplot as plt
import os
import pandas as pd

def plot_results(all_results, assigned_tasks):
    """
    汇总并绘制所有电池的曲线，同时用点标记任务的起始点。
    """
    # 定义需要绘制的参数
    parameters = ["SOC", "SOH", "Temperature (°C)", "Resistance (Ohm)"]

    for param in parameters:
        plt.figure(figsize=(10, 6))
        for i, results in enumerate(all_results):
            # 获取时间和变量值
            time = results.get("Time [h]", None)
            value = results.get(param, None)

            # 调试时间和变量数据
            print(f"DEBUG: Battery {i + 1}, Parameter {param}, Time shape: {len(time)}, Value shape: {len(value)}")

            # 如果数据为空，跳过绘制
            if time is None or len(time) == 0:
                print(f"Battery {i + 1}: No time data available for {param}, skipping.")
                continue

            if value is None or len(value) == 0:
                print(f"Battery {i + 1}: No data available for {param}, skipping.")
                continue

            # 绘制当前电池的曲线
            plt.plot(time, value, label=f"Battery {i + 1}")

            # 添加任务起始点标记
            battery_tasks = [task for task in assigned_tasks if task["battery"] == i + 1]
            for task in battery_tasks:
                start_time = task["start_time"]
                start_index = next((j for j, t in enumerate(time) if t >= start_time), None)
                if start_index is not None:
                    plt.scatter(
                        time[start_index], value[start_index],
                        label=f"Task {task['id']} start",
                        marker='o', s=50, zorder=5
                    )

        # 设置图形标题和轴标签
        plt.title(f"{param} vs Time")
        plt.xlabel("Time [h]")
        plt.ylabel(param)
        plt.grid(True)
        plt.legend(loc="best")

    plt.tight_layout()  # 自动调整布局
    plt.show()  # 显示所有图

def save_results_as_csv(all_results, save_dir="results_data"):
    """
    将所有电池的仿真结果保存为 CSV 文件，并在文件名中加入温度标签。

    Parameters:
        all_results (list): 包含所有电池仿真结果的列表。
        save_dir (str): 保存 CSV 文件的目录路径。
    """
    # 创建保存目录（如果不存在）
    os.makedirs(save_dir, exist_ok=True)

    # 定义需要保存的参数
    parameters = ["Time [h]", "SOC", "SOH", "Temperature (°C)", "Resistance (Ohm)"]

    for i, results in enumerate(all_results):
        # 初始化 DataFrame
        data = {}

        # 提取每个参数的值
        for param in parameters:
            if param in results:
                data[param] = results[param]
            else:
                print(f"Battery {i + 1}: No data available for {param}, skipping.")
        
        # 如果没有有效数据，跳过该电池
        if not data:
            print(f"Battery {i + 1}: No valid data found, skipping CSV export.")
            continue

        # 保存为 DataFrame
        df = pd.DataFrame(data)

        # 获取温度的第一个值作为标签
        temperature = results.get("Temperature (°C)", [None])[0]
        if temperature is None:
            temperature_label = "UnknownTemp"
        else:
            temperature_label = f"{temperature:.1f}C"  # 格式化为整数

        # 构造文件名
        file_path = os.path.join(save_dir, f"Battery_{i + 1}_{temperature_label}_results.csv")

        # 保存到 CSV 文件
        df.to_csv(file_path, index=False)
        print(f"Saved results for Battery {i + 1} to: {file_path}")


