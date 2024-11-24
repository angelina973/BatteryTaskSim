def print_assignment_results(assigned_tasks):
    """
    打印任务分配结果。
    """
    print("\nTask Assignment Results:")
    for task in assigned_tasks:
        print(f"Task {task['id']} assigned to Battery {task['battery']} "
              f"from {task['start_time']}h to {task['end_time']}h")
