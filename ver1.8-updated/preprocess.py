def preprocess_variable(solution, variable_name, time_data):
    """
    预处理变量，确保其与时间数据对齐。
    """
    try:
        var_data = solution[variable_name].data
        if var_data.ndim > 1:  # 多维数据取平均值
            var_data = var_data.mean(axis=0)
        if len(var_data) != len(time_data):
            raise ValueError(f"Variable '{variable_name}' dimensions do not match time.")
        return var_data
    except KeyError:
        raise KeyError(f"Variable '{variable_name}' not found in solution.")
    except ValueError as e:
        raise ValueError(f"Error processing variable '{variable_name}': {e}")
