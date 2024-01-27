from .utils.pywikibot_login import wiki_upload
from .utils.read_data import read_gde, read_i2
from .utils.task_numbers import task_numbers
from .utils.output_file import output_file
from .utils.string_hash import string_hash

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
    gde_data = read_gde()
    i2_data = read_i2()
    output = []
    stringhash = string_hash(gde_data)
    id_dict = task_numbers(location, loc_id, gde_data)
    namekey = i2_data.get("questtitle_"+location) if i2_data.get("questtitle_"+location) is not None else i2_data.get("namekey_"+location)
    output.append("\'''Note:\''' Due to the game's constant updates, the tasks on this page may not always be accurate. If you have any new information, feel free to go to the \""+namekey+"/Tasks\" page and edit accordingly.\n\n{| class=\"article-table\" style=\"font-size:15px;\"\n!style=\"width:100px\"|#\n!Name\n!style=\"width:100px\"|Opens\n!Items\n!Rewards\n")
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) != "Quest" or gde_data[line].get(stringhash["CompleteAreaKey"]).lower() != location:
            continue
        quest_key = gde_data[line].get(stringhash["Id"])
        desc_key = gde_data[line].get(stringhash["Desc"]).lower()
        unlock_list = []
        for item in gde_data[line].get(stringhash["CompleteOpenQuest"]):
            unlock_list.append(id_dict[item] if item in id_dict else f"UN-{str(item)}")
        unlock_list.sort(key = lambda x: int(x.split('-')[1]))
        unlock_key = "<br>".join(unlock_list)
        item_dict = {item: count for item, count in zip(gde_data[line].get(stringhash["NeedItem"]), gde_data[line].get(stringhash["NeedItemCount"]))}
        item_list = []
        for item in gde_data[line].get(stringhash["NeedItem"]):
            if item == "EventCoin":
                item_list.append(f"{item_dict[item]} [[File:LemonMoney.png|30px]] [[Lemon Event|Money]]")
            else:
                item_name, item_level = item.split("_")
                item_id = str(item_dict[item])+"x {{Item | "+i2_data.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}" if item_dict[item] != 1 else "{{Item | "+i2_data.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}"
                item_list.append(item_id)
        item_key = "<br>".join(item_list)
        reward_list = []
        for reward in gde_data[line].get(stringhash["Reward"]):
            if reward.split("_")[0] == "Flower" and len(reward.split("_")) ==4:
                plant = reward.split("_")[1].capitalize()
                if plant == "Pinkrose":
                    reward_list.append("[[File:PinkRoseSeedBag.png|21x21px]] [[Seed_Packets#Pink Rose Seed Packet|Pink Rose Seed Packet]]")
                    continue
                reward_list.append(f"[[File:{plant}SeedBag.png|21x21px]] [[Seed_Packets#{plant} Seed Packet|{plant} Seed Packet]]")
                continue
            reward_name, reward_level = reward.split("_")
            reward_list.append("{{Item | "+i2_data.get("categoryname_"+reward_name.lower())+" | "+reward_level.lstrip("0")+"}}")
        reward_key = "<br>".join(reward_list)
        output.append(f"|-\n|{id_dict.get(quest_key)}\n|{i2_data.get(desc_key)}\n|{unlock_key}\n|{item_key}\n|{reward_key}\n")
    output.append("|}\n[[Category:Tasks]]")
    text = "".join(output)
    if upload is False:
        with open(output_file("task_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/"+namekey+"/Tasks", text)
    print("Action completed.")
