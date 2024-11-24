import pybamm

def setup_battery_model(battery_info):
    """
    配置电池模型和参数。
    """
    model = pybamm.lithium_ion.DFN({"thermal": "lumped", "SEI": "ec reaction limited"})
    param = pybamm.ParameterValues("Chen2020")

    # 动态更新参数
    update_parameters(param, battery_info)
    
    # 打印初始参数
    print("Updated Parameters:")
    for key, value in param.items():
        print(f"{key}: {value}")
    
    return model, param

def update_parameters(param, battery_info):
    """
    根据输入信息动态更新参数。
    """
    initial_soc = battery_info.get("SOC", 1.0)
    initial_temperature = battery_info.get("Temperature", 290.15)
    initial_sei_resistivity = battery_info.get("SEI_resistivity", 1e5)

    param.update({
        "Initial concentration in negative electrode [mol.m-3]": param[
        "Maximum concentration in negative electrode [mol.m-3]"
        ] * initial_soc,
        "Ambient temperature [K]": initial_temperature,  # 环境温度,与电池初始值相同（假设电池恒温环境中存放）
        "Initial temperature [K]": initial_temperature,
        "SEI resistivity [Ohm.m]": initial_sei_resistivity,
        "Cell thermal conductivity [W.m-1.K-1]": 0.1,  # 降低热导率
        "Total heat transfer coefficient [W.m-2.K-1]": 10.0,  # 从10降低到5
        "Edge heat transfer coefficient [W.m-2.K-1]": 3.0, # 假设增加边界绝热性
        "Cell thermal conductivity [W.m-1.K-1]": 0.05,  # 减小电池热导率
        "Cell cooling surface area [m2]": 0.000131,
        "SEI growth activation energy [J.mol-1]": 50000.0  # 增加到50 kJ/mol
    }, check_already_exists=False)
