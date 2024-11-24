def is_task_feasible(task, battery_info):
    """
    检查任务是否适合分配给特定电池。
    """
    required_capacity = task["power"] * task["time"]  # 任务所需能量
    available_capacity = battery_info["SOC"] * battery_info.get("Capacity", 1.0)  # 电池当前可用容量

    # 简单阈值检查
    if available_capacity < required_capacity:
        return False
    if battery_info["SOH"] < 80.0:  # 低于 80% 健康状态的电池不适合任务
        return False
    if battery_info["Temperature"] > 323.15:  # 温度高于 50°C 的电池不适合任务
        return False
    return True
