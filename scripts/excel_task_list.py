import pandas as pd

from .utils.match_location import area_dict
from .utils.output_file import output_file
from .utils.string_hash import string_hash
from .utils.read_gde import read_gde
from .utils.read_i2 import read_i2

def excel_task_list():
    '''Outputs a spreadsheet listing all tasks in the game, split into pages for each area.'''
    area_list = list(area_dict().keys())
    data = read_gde()
    descriptions = read_i2()
    stringhash = string_hash()
    task_dict = {}
    for area in area_list:
        task_dict[area] = []
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) != "Quest" or data[line].get(stringhash["AreaGroupKey"]).lower() not in area_list:
            continue
        quest_no = data[line].get(stringhash["Id"])
        unlock = list(map(str, data[line].get(stringhash["CompleteOpenQuest"])))
        unlocks = ", ".join(unlock)
        area = data[line].get(stringhash["AreaGroupKey"]).lower()
        item = data[line].get(stringhash["NeedItem"])
        items = ", ".join(item)
        item_count = list(map(str, data[line].get(stringhash["NeedItemCount"])))
        item_counts = ", ".join(item_count)
        reward = list(map(str, data[line].get(stringhash["Reward"])))
        rewards = ", ".join(reward)
        desc_key = data[line].get(stringhash["Desc"]).lower()
        descs = descriptions.get(desc_key)
        task_dict[area].append([quest_no, unlocks, items, item_counts, rewards, descs])
    with pd.ExcelWriter(output_file('tasks.xlsx')) as writer:
        for area, tasks in task_dict.items():
            task_data = pd.DataFrame(tasks, columns = ["Task", "Unlocks", "Item", "Count", "Reward", "Desc"])
            task_data.to_excel(writer, sheet_name = descriptions.get("questtitle_"+area), index = False)
    print("Action completed.")
