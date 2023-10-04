from .string_hash import string_hash
from .read_gde import read_gde

def task_numbers(location, loc_id):
    '''Assigns a task number to every task in an area.
    
    Keyword Arguments:
    location            - The name of the area we are creating the dictionary for
    loc_id              - A short 2-3 letter code to name the tasks after

    Return Value:
    A dictionary containing the task's in file id and the new task identifier.
    '''
    data = read_gde()
    id_dict = {}
    count = 1
    stringhash = string_hash()
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest" and data[line].get(stringhash["CompleteAreaKey"]).lower() == location:
            id_dict[data[line].get(stringhash["Id"])] = f"{loc_id.upper()}-{count}"
            count += 1
    return id_dict
