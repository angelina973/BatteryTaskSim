def calculate_battery_score(battery):
    """
    计算电池的综合评分。
    """
    soc_weight = 0.5
    soh_weight = 0.3
    temp_weight = 0.2

    soc_score = battery["SOC"]  # SOC 越高越好
    soh_score = battery["SOH"] / 100.0  # 健康度转化为 0-1 范围
    temp_score = max(0, 1 - (battery["Temperature"] - 298.15) / 25.0)  # 温度过高时降低评分

    return soc_weight * soc_score + soh_weight * soh_score + temp_weight * temp_score
