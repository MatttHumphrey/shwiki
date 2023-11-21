from .utils.pywikibot_login import wiki_upload
from .utils.task_numbers import task_numbers
from .utils.output_file import output_file
from .utils.string_hash import string_hash
from .utils.read_data import read_gde
from .utils.read_data import read_i2

def task_list(location, loc_id, upload = False):
    '''
    Generates the full list of tasks for a given area.
    Note: Tasks are listed in the order they appear in the game files. 
          For some areas, this will need adjusting manually to reorder.

    Keyword Arguments:
    location            - The name of the area we are generating the task list for
    loc_id              - A short 2-3 letter code to name the tasks after
    upload              - Optional trigger to upload the page automatically to the wiki
    '''
    data = read_gde()
    descriptions = read_i2()
    output = []
    stringhash = string_hash()
    id_dict = task_numbers(location, loc_id)
    namekey = descriptions.get("questtitle_"+location) if descriptions.get("questtitle_"+location) is not None else descriptions.get("namekey_"+location)
    output.append("\'''Note:\''' Due to the game's constant updates, the tasks on this page may not always be accurate. If you have any new information, feel free to go to the \""+namekey+"/Tasks\" page and edit accordingly.\n\n{| class=\"article-table\" style=\"font-size:15px;\"\n!style=\"width:100px\"|# \n!Name \n!style=\"width:100px\"|Opens \n!Items \n!Rewards \n")
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) != "Quest" or data[line].get(stringhash["CompleteAreaKey"]).lower() != location:
            continue
        quest_key = data[line].get(stringhash["Id"])
        desc_key = data[line].get(stringhash["Desc"]).lower()
        unlock_list = []
        for item in data[line].get(stringhash["CompleteOpenQuest"]):
            unlock_list.append(id_dict[item] if item in id_dict else f"UN-{str(item)}")
        unlock_key = "<br>".join(unlock_list)
        item_dict = {item: count for item, count in zip(data[line].get(stringhash["NeedItem"]), data[line].get(stringhash["NeedItemCount"]))}
        item_list = []
        for item in data[line].get(stringhash["NeedItem"]):
            if item == "EventCoin":
                item_list.append(f"{item_dict[item]} [[File:LemonMoney.png|30px]] [[Lemon Event|Money]]")
            else:
                item_name, item_level = item.split("_")
                item_id = str(item_dict[item])+"x {{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}" if item_dict[item] != 1 else "{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}"
                item_list.append(item_id)
        item_key = "<br>".join(item_list)
        reward_list = []
        for reward in data[line].get(stringhash["Reward"]):
            reward_name, reward_level = reward.split("_")
            reward_list.append("{{Item | "+descriptions.get("categoryname_"+reward_name.lower())+" | "+reward_level.lstrip("0")+"}}")
        reward_key = "<br>".join(reward_list)
        output.append(f"|-\n|{id_dict.get(quest_key)}\n|{descriptions.get(desc_key)}\n|{unlock_key}\n|{item_key}\n|{reward_key}\n")
    output.append("|}\n[[Category:Tasks]]")
    text = "".join(output)
    if upload is False:
        with open(output_file("task_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/"+namekey+"/Tasks", text)
    print("Action completed.")
