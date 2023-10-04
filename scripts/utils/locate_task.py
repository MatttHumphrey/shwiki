def locate_task(key, task_dict):
    '''
    Returns the area that a specified task is found in using a task_dict.
    
    Keyword Arguments:
    key                 - Id of task to locate
    task_dict           - Dictionary of tasks from dialogue_task_dict.py

    Return Value:
    Area returned as a string if found, or None value otherwise.
    '''
    for area, task in task_dict.items():
        if key in task:
            return area
    return None
