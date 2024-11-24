import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot_gantt_chart(tasks):
    """
    绘制任务的甘特图，展示每个任务的分配时间和电池。
    """
    if not tasks:
        print("No tasks to plot.")
        return

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
    plt.title("Gantt Chart of Task Assignments")
    plt.grid(axis="x", linestyle="--", alpha=0.6)

    # 添加图例
    handles = [mpatches.Patch(color=color_map[task["id"]], label=f"Task {task['id']}") for task in tasks]
    plt.legend(handles=handles, loc="upper right", title="Tasks")

    plt.tight_layout()
    plt.show()
