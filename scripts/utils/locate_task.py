def locate_task(key,dic):
    for area, task in dic.items():
        if key in task:
            return area
    return None