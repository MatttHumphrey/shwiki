from .string_hash import string_hash
from .read_gde import read_gde

def area_unlocks_dict():
    '''Returns a dictionary containing the names of every area and a list of all the tasks unlocked throughout that area.'''
    data = read_gde()
    stringhash = string_hash()
    unlocks_dict = {}
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            area = data[line].get(stringhash["AreaGroupKey"]).lower()
            unlocks = data[line].get(stringhash["CompleteOpenQuest"])
            if unlocks_dict.get(area) is None:
                unlocks_dict[area] = []
            for item in unlocks:
                unlocks_dict[area].append(item)
    return unlocks_dict
