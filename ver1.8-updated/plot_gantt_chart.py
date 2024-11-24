import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

def plot_gantt_chart(tasks, temperature, save_dir="gantt_charts"):
    """
    绘制任务的甘特图，展示每个任务的分配时间和电池，同时自动保存图表。

    Parameters:
        tasks (list): 包含任务信息的列表，每个任务是一个字典，需包含 "battery", "start_time", "end_time", "id", "power"。
        temperature (float): 温度值（单位：开尔文），将用于保存文件名和图表提示。
        save_dir (str): 保存甘特图的目录路径。
    """
    if not tasks:
        print("No tasks to plot.")
        return

    # 转换温度为摄氏度整数
    temp_celsius = int(round(temperature - 273.15))

    # 创建保存目录（如果不存在）
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"gantt_chart_{temp_celsius}C.png")

    # 获取电池列表
    batteries = sorted(set(task["battery"] for task in tasks))

    # 颜色映射，用于区分不同任务
    colors = plt.cm.tab20.colors
    color_map = {task["id"]: colors[task["id"] % len(colors)] for task in tasks}

    plt.figure(figsize=(12, 6))
    
    # 绘制每个任务的水平条
    for task in tasks:
        battery = task["battery"]
        start = task["start_time"]
        duration = task["end_time"] - task["start_time"]
        color = color_map[task["id"]]

        plt.barh(
            y=battery, 
            width=duration, 
            left=start, 
            color=color, 
            edgecolor="black"
        )

        # 添加任务信息文字
        plt.text(
            x=start + duration / 2, 
            y=battery, 
            s=f"Task {task['id']}\n{task['power']}W", 
            va="center", 
            ha="center", 
            fontsize=8, 
            color="white" if task['power'] > 3 else "black"
        )

    # 设置轴标签和标题
    plt.yticks(batteries, [f"Battery {b}" for b in batteries])
    plt.xlabel("Time [h]")
    plt.ylabel("Battery")
    plt.title(f"Gantt Chart of Task Assignments -- Temperature: {temp_celsius}°C")
    plt.grid(axis="x", linestyle="--", alpha=0.6)

    # 添加图例
    handles = [mpatches.Patch(color=color_map[task["id"]], label=f"Task {task['id']}") for task in tasks]
    plt.legend(handles=handles, loc="upper right", title="Tasks")

    plt.tight_layout()

    # 保存图表
    plt.savefig(save_path)
    print(f"Gantt chart saved to: {save_path}")

    plt.show()
