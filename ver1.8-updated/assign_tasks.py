import heapq
from sort_tasks import sort_tasks_by_priority
from update_battery_health import update_battery_health
from is_task_feasible import is_task_feasible
from scores import calculate_battery_score

def predict_voltage_drop(battery, task):
    """
    根据任务预测电池的电压变化，判断是否会到达截止电压。

    Parameters:
        battery (dict): 电池状态，包含 Voltage, SOC, Resistance, Capacity。
        task (dict): 任务信息，包括 power 和 time。

    Returns:
        bool: 如果任务可行（不会到达截止电压），返回 True；否则返回 False。
    """
    power = task["power"]
    time = task["time"]
    voltage = battery.get("Voltage", 3.7)  # 当前电压
    resistance = battery.get("Resistance", 0.1)  # 内阻
    capacity = battery.get("Capacity", 1.0)  # 容量（Ah）
    soc = battery.get("SOC", 1.0)  # SOC (0-1)

    # 计算任务电流
    current = power / voltage  # 电流 = 功率 / 电压

    # 预测 SOC 变化
    capacity_used = current * time / 3600  # 单位：Ah
    soc_after_task = soc - capacity_used / capacity
    if soc_after_task <= 0:
        return False  # SOC 低于 0，不可行

    # 预测电压变化
    voltage_drop = current * resistance
    predicted_voltage = voltage - voltage_drop
    cutoff_voltage = 3.0  # 假设截止电压为 3.0V

    return predicted_voltage > cutoff_voltage

def assign_tasks_to_batteries(batteries, tasks):
    """
    分配任务到电池，整合电压预测模型。

    Parameters:
        batteries (list): 电池列表，每个电池包含 SOC, Voltage, Resistance, 等信息。
        tasks (list): 任务列表，每个任务包含 power 和 time。

    Returns:
        list: 分配好的任务列表。
    """
    tasks = sort_tasks_by_priority(tasks)
    battery_queue = [(0, i, battery) for i, battery in enumerate(batteries)]
    heapq.heapify(battery_queue)

    assigned_tasks = []
    unassigned_tasks = []

    for task in tasks:
        best_battery = None
        best_score = float('-inf')
        best_idx = None

        # 尝试为任务找到最佳电池
        for _, idx, battery in battery_queue:
            if is_task_feasible(task, battery) and predict_voltage_drop(battery, task):
                score = calculate_battery_score(battery)
                if score > best_score:
                    best_battery = battery
                    best_score = score
                    best_idx = idx

        if best_battery:
            start_time = best_battery.get("current_time", 0)
            end_time = start_time + task["time"]
            task.update({"battery": best_idx + 1, "start_time": start_time, "end_time": end_time})
            assigned_tasks.append(task)

            # 更新电池状态
            update_battery_health(best_battery, task)
            best_battery["current_time"] = end_time
        else:
            unassigned_tasks.append(task)  # 无法分配的任务

    # 打印未分配的任务
    if unassigned_tasks:
        for task in unassigned_tasks:
            print(f"Task {task['id']} could not be assigned.")

    return assigned_tasks
