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
        "Ambient temperature [K]": 300.65,  # 确保环境温度为 25°C
        "Initial temperature [K]": initial_temperature,
        "SEI resistivity [Ohm.m]": initial_sei_resistivity,
    }, check_already_exists=False)
