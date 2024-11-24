import os
import json

def calculate_battery_score(
    battery, weights=None, save_dir="scores", use_saved=False, temperature_label=None
):
    """
    计算电池的综合评分，支持保存和读取功能，同时约束温度不能超过 42°C。
    
    Parameters:
        battery (dict): 包含电池状态的字典，需包含 "SOC", "SOH", "Temperature"。
        weights (dict): 可选，包含 "SOC", "SOH", "Temperature" 的权重字典。
        save_dir (str): 保存评分结果的目录路径。
        use_saved (bool): 是否直接读取保存的结果而不重新计算。
        temperature_label (str): 指定读取的温度标签，用于查找保存的评分结果。

    Returns:
        float: 电池的综合评分（0-1）。
    """
    # 默认权重（可动态调整）
    if weights is None:
        weights = {"SOC": 0.4, "SOH": 0.25, "Temperature": 0.25, "SEI_resistivity": 0.1}

    # 检查保存目录是否存在
    os.makedirs(save_dir, exist_ok=True)

    # 生成温度标签
    temperature = battery.get("Temperature")
    if temperature is None:
        raise ValueError("Missing required attribute: Temperature")
    temperature_label = temperature_label or f"{temperature:.1f}K"

    # 保存文件路径
    save_path = os.path.join(save_dir, f"score_{temperature_label}.json")

    # 如果启用了读取功能，从保存的文件中读取评分
    if use_saved:
        if os.path.exists(save_path):
            with open(save_path, "r") as f:
                saved_data = json.load(f)
                print(f"Using saved score for temperature {temperature_label}: {saved_data['score']}")
                return saved_data["score"]
        else:
            raise FileNotFoundError(f"No saved score found for temperature {temperature_label}")

    # 容错处理：检查数据完整性
    if any(key not in battery for key in ["SOC", "SOH", "Temperature"]):
        raise ValueError("Missing required battery attributes: SOC, SOH, or Temperature")

    # 强制约束：温度不能超过 45°C
    max_allowed_temperature = 318.15  # 45°C 转为开尔文
    if temperature > max_allowed_temperature:
        print(f"Temperature exceeds 45°C ({temperature - 273.15:.2f}°C). Score set to 0.")
        return 0.0

    # SOC评分：线性映射到 0-1 范围
    soc_score = max(0, min(1, battery["SOC"] / 100.0))  # 假设 SOC 范围为 0-100%

    # SOH评分：线性映射到 0-1 范围
    soh_score = max(0, min(1, battery["SOH"] / 100.0))  # 假设 SOH 范围为 0-100%

    # 温度评分：平滑处理，温度最佳范围为 298.15K（25°C）
    temp_optimal = 298.15
    temp_tolerance = 25.0  # 最大可接受的偏差范围
    temp_deviation = abs(battery["Temperature"] - temp_optimal)
    temp_score = max(0, 1 - (temp_deviation / temp_tolerance) ** 1.5)  # 平滑衰减

    # 电阻评分（可选，如果数据可用）
    if "SEI_resistivity" in battery:
        resistance = battery["SEI_resistivity"]
        resistance_threshold = 0.01  # 电阻阈值（单位：Ohm）
        resistance_score = max(0, 1 - resistance / resistance_threshold)  # 电阻越低越好
    else:
        resistance_score = 0.0

    # 计算综合评分
    score = (
        weights["SOC"] * soc_score +
        weights["SOH"] * soh_score +
        weights["Temperature"] * temp_score +
        weights.get("SEI_resistivity", 0.0) * resistance_score
    )
    score = max(0, min(1, score))  # 限制评分范围为 0-1

    # 保存评分结果
    result_data = {
        "temperature": battery["Temperature"],
        "score": score,
        "soc_score": soc_score,
        "soh_score": soh_score,
        "temp_score": temp_score,
        "resistance_score": resistance_score,
        "weights": weights,
    }
    with open(save_path, "w") as f:
        json.dump(result_data, f)
    print(f"Saved score for temperature {temperature_label}: {score}")

    return score
