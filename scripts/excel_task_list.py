import pandas as pd

from .utils.read_data import read_gde, read_i2
from .utils.match_location import area_dict
from .utils.output_file import output_file
from .utils.string_hash import string_hash

def excel_task_list():
    '''Outputs a spreadsheet listing all tasks in the game, split into pages for each area.'''
    gde_data = read_gde()
    i2_data = read_i2()
    area_list = list(area_dict(gde_data, i2_data).keys())
    stringhash = string_hash(gde_data)
    task_dict = {}
    for area in area_list:
        task_dict[area] = []
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) != "Quest" or gde_data[line].get(stringhash["AreaGroupKey"]).lower() not in area_list:
            continue
        quest_no = gde_data[line].get(stringhash["Id"])
        unlock = list(map(str, gde_data[line].get(stringhash["CompleteOpenQuest"])))
        unlocks = ", ".join(unlock)
        area = gde_data[line].get(stringhash["AreaGroupKey"]).lower()
        item = gde_data[line].get(stringhash["NeedItem"])
        items = ", ".join(item)
        item_count = list(map(str, gde_data[line].get(stringhash["NeedItemCount"])))
        item_counts = ", ".join(item_count)
        reward = list(map(str, gde_data[line].get(stringhash["Reward"])))
        rewards = ", ".join(reward)
        desc_key = gde_data[line].get(stringhash["Desc"]).lower()
        descs = i2_data.get(desc_key)
        task_dict[area].append([quest_no, unlocks, items, item_counts, rewards, descs])
    with pd.ExcelWriter(output_file('tasks.xlsx')) as writer:
        for area, tasks in task_dict.items():
            task_data = pd.DataFrame(tasks, columns = ["Task", "Unlocks", "Item", "Count", "Reward", "Desc"])
            task_data.to_excel(writer, sheet_name = i2_data.get("questtitle_"+area), index = False)
    print("Action completed.")
