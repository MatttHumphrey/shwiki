from .read_gde import read_gde

def area_tasks_dict():
    dic = {}
    data = read_gde()
    for line in data:
        if data[line].get("1071") == "Quest":
            area = data[line].get("20").lower()
            tasks = data[line].get("2")
            if dic.get(area) == None:
                dic[area] = []
            dic[area].append(tasks)              
    return dic