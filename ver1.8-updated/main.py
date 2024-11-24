from assign_tasks import assign_tasks_to_batteries
# from print_assignment_results import print_assignment_results
from plot_gantt_chart import plot_gantt_chart
from simulate_battery import simulate_battery
from plot_results import plot_results,save_results_as_csv

def main():
    """
    主函数，分配任务、运行仿真并生成汇总结果，包括甘特图。
    """
    zero_point_Temperature = 20 + 273.15 #初始温度
    # 定义电池列表（原始初始值）
    original_batteries = [
        {"SOC": 0.98, "SOH": 100, "Temperature": zero_point_Temperature, "Capacity": 12.0, "current_time": 0, "SEI_resistivity": 0.002*1e6}, 
        {"SOC": 0.98, "SOH": 100, "Temperature": zero_point_Temperature, "Capacity": 9.0, "current_time": 0, "SEI_resistivity": 0.0021*1e6},
        {"SOC": 0.98, "SOH": 100, "Temperature": zero_point_Temperature, "Capacity": 10.0, "current_time": 0, "SEI_resistivity": 0.0022*1e6},
    ]

    # 保存每个电池的初始值以供估算后恢复
    initial_battery_states = [
        {
            "SOC": battery["SOC"],
            "SOH": battery["SOH"],
            "Temperature": battery["Temperature"]
        }
        for battery in original_batteries
    ]

    # 定义任务列表
    tasks = [
        {"id": 1, "power": 8, "time": 0.9, "weight": 5},
        {"id": 2, "power": 5, "time": 0.5, "weight": 4},
        {"id": 3, "power": 6, "time": 0.6, "weight": 4},
        {"id": 4, "power": 4, "time": 0.7, "weight": 3},
        {"id": 5, "power": 5, "time": 1.2, "weight": 3},
        {"id": 6, "power": 4, "time": 0.4, "weight": 3},
        {"id": 7, "power": 3, "time": 1.0, "weight": 2},
        {"id": 8, "power": 3, "time": 0.5, "weight": 2},
        {"id": 9, "power": 3, "time": 0.3, "weight": 1}
    ]

    print("Initial Battery States:")
    for i, battery in enumerate(original_batteries):
        print(f"Battery {i + 1}: {battery}")

    try:
        # 1. 分配任务到电池
        print("\nStep 1: Assigning tasks...")
        assigned_tasks = assign_tasks_to_batteries(original_batteries, tasks) # 预估算电池用量，分配任务
        # print_assignment_results(assigned_tasks)

        # 2. 生成甘特图
        print("\nStep 2: Generating Gantt Chart...")
        plot_gantt_chart(assigned_tasks,zero_point_Temperature)

        # 3. 仿真并汇总结果
        print("\nStep 3: Running simulations with initial battery states:")
        all_results = []
        for i, battery in enumerate(original_batteries):
            battery.update(initial_battery_states[i]) # 恢复电池的初始状态
            battery_tasks = [task for task in assigned_tasks if task["battery"] == i + 1] # 分配任务
            print(f"\nSimulating Battery {i + 1} with Tasks: {battery_tasks}") 
            results = simulate_battery(battery, battery_tasks) # 仿真
            print(f"Results for Battery {i + 1}: {results}")
            all_results.append(results) # 提取结果

        # 4. 绘制仿真结果曲线
        print("\nStep 4: Plotting results with task markers...")
        plot_results(all_results, assigned_tasks) 
        # 5. 保存仿真结果为 CSV
        save_results_as_csv(all_results, save_dir="simulation_data")


    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
