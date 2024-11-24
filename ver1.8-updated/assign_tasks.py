import heapq
from sort_tasks import sort_tasks_by_priority
from update_battery_health import update_battery_health
from is_task_feasible import is_task_feasible
from scores import calculate_battery_score

def assign_tasks_to_batteries(batteries, tasks):
    tasks = sort_tasks_by_priority(tasks)
    battery_queue = [(0, i, battery) for i, battery in enumerate(batteries)]
    heapq.heapify(battery_queue)

    assigned_tasks = []
    for task in tasks:
        best_battery = None
        best_score = float('-inf')
        best_idx = None

        for _, idx, battery in battery_queue:
            if is_task_feasible(task, battery):
                score = calculate_battery_score(battery)
                if score > best_score:
                    best_battery = battery
                    best_score = score
                    best_idx = idx

        if best_battery:
            start_time = best_battery.get("current_time", 0)
            end_time = start_time + task["time"]
            task.update({"battery": best_idx + 1, "start_time": start_time, "end_time": end_time})
            assigned_tasks.append(task)
            update_battery_health(best_battery, task)
            best_battery["current_time"] = end_time
        else:
            print(f"Task {task['id']} could not be assigned.")
    return assigned_tasks
