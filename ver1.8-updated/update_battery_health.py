def update_battery_health(battery, task):
    """
    根据任务估算电池健康状态。分配任务时使用，不作为最终仿真结果。
    """
    power = task["power"]
    time = task["time"]
    capacity_used = power * time

    # 更新 SOC
    battery["SOC"] -= capacity_used / battery.get("Capacity", 1.0)

    # 更新 SOH，假设简单线性退化模型
    battery["SOH"] -= 0.01 * capacity_used

    # 更新温度（简单示例，假设温度上升与功率相关）
    battery["Temperature"] += 0.15 * power  # 功率越高，温升越快
