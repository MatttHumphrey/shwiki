from .read_gde import read_gde

def dialogue_task_dict():
    task_dict = {}
    data = read_gde()
    for line in data:
        if data[line].get("1071") == "Quest":
            area = data[line].get("20", "")
            if area not in task_dict:
                task_dict[area] = []
            dialogue_ids = [data[line].get("36"), data[line].get("38")]
            task_dict[area].extend(task_id for task_id in dialogue_ids if task_id) 
    return task_dict