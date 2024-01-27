from utils.pywikibot_login import wiki_upload
from utils.read_data import read_gde, read_i2
from utils.output_file import output_file
from utils.string_hash import string_hash
from utils.task_orders import TASK_ORDERS

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
    descriptions = read_i2()
    output = []
    stringhash = string_hash(gde_data)
    tasks = TASK_ORDERS.get(location)
    id_dict = task_numbers(location, loc_id, gde_data)
    namekey = descriptions.get("questtitle_"+location) if descriptions.get("questtitle_"+location) is not None else descriptions.get("namekey_"+location)
    output.append("\'''Note:\''' Due to the game's constant updates, the tasks on this page may not always be accurate. If you have any new information, feel free to go to the \""+str(namekey)+"/Tasks\" page and edit accordingly.\n\n{| class=\"article-table\" style=\"font-size:15px;\"\n!style=\"width:100px\"|#\n!Name\n!style=\"width:100px\"|Opens\n!Items\n!Rewards\n")
    for line in tasks:
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
                item_id = str(item_dict[item])+"x {{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}" if item_dict[item] != 1 else "{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}"
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
    tasks = TASK_ORDERS.get(location)
    stringhash = string_hash()
    for line in tasks:
        id_dict[gde_data[line].get(stringhash["Id"])] = f"{loc_id.upper()}-{count}"
        count += 1
    return id_dict

task_list("outbuilding", "GS", upload = False)
