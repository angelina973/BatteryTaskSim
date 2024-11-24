def sort_tasks_by_priority(tasks):
    """
    根据任务权重对任务列表排序。
    """
    return sorted(tasks, key=lambda x: -x["weight"])
