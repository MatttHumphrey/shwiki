from .string_hash import string_hash

def task_numbers(location, loc_id, gde_data):
    '''Assigns a task number to every task in an area.
    
    Keyword Arguments:
    location            - The name of the area we are creating the dictionary for
    loc_id              - A short 2-3 letter code to name the tasks after

    Return Value:
    A dictionary containing the task's in file id and the new task identifier.
    '''
    id_dict = {}
    count = 1
    stringhash = string_hash(gde_data)
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Quest" and gde_data[line].get(stringhash["CompleteAreaKey"]).lower() == location:
            id_dict[gde_data[line].get(stringhash["Id"])] = f"{loc_id.upper()}-{count}"
            count += 1
    return id_dict
