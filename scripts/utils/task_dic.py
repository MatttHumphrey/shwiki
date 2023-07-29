from read_gde import read_gde

def task_dict():
    taskdict = {}
    data = read_gde()
    for line in data:
        if data[line].get("1071") == "Quest":
            area = data[line].get("20", "")
            if area and area not in taskdict:
                taskdict[area] = []
            task_ids = [data[line].get("36"), data[line].get("38")]
            taskdict[area].extend(task_id for task_id in task_ids if task_id) 
    return taskdict