import json
import sys
import os.path as path
import difflib
from convert import TOOL_CONVERT, REWARD_CONVERT
from modules import GDE_FILE, read_i2, get_arealist, tasknumbers, match_location

def main(loc, id):
    OUTPUT_FILE = path.join(path.dirname(__file__),"task_output.txt")
    descriptions = read_i2()
    task_nos = tasknumbers(loc, id)
    with open(GDE_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
    with open(OUTPUT_FILE, "w+", encoding="utf8") as output:
        namekey = descriptions.get("questtitle_"+loc, "N/A")
        output.writelines("\'''Note:\''' Due to the game's constant updates, the tasks on this page may not always be accurate. If you have any new information, feel free to go to the \""+namekey+"/Tasks\" page and edit accordingly.\n\n{| class=\"article-table\" style=\"font-size:15px;\"\n!style=\"width:100px\"|# \n!Name \n!style=\"width:100px\"|Opens \n!Items \n!Rewards \n")
        for line in data:
            if data[line].get("1071") != "Quest" or data[line].get("18").lower() != loc:
                continue
            quest_key = data[line].get("2")
            desc_key = data[line].get("34").lower()
            unlock_list = []
            for item in data[line].get("5"):
                unlock_list.append(task_nos[item]) if item in task_nos.keys() else unlock_list.append(str(item))
            unlock_key = "<br>".join(unlock_list)
            item_dict = {item: count for item, count in zip(data[line].get("23"), data[line].get("26"))}
            item_list = []
            for item in data[line].get("23"):
                if item == "EventCoin":
                    item_list.append(f"{item_dict[item]} [[File:LemonMoney.png|30px]] [[Lemon Event|Money]]")
                else:
                    item_name, item_level = item.split("_")
                    item_id = str(item_dict[item])+"x {{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}" if item_dict[item] != 1 else "{{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}"
                    item_list.append(item_id)
            item_key = "<br>".join(item_list)
            reward_list = []
            for reward in data[line].get("16"):
                reward_name, reward_level = reward.split("_")
                reward_list.append("{{Item | "+REWARD_CONVERT[reward_name.lower()]+" | "+reward_level.lstrip("0")+"}}")
            reward_key = "<br>".join(reward_list)
            output.writelines(f"|-\n|{task_nos.get(quest_key)}\n|{descriptions.get(desc_key)}\n|{unlock_key}\n|{item_key}\n|{reward_key}\n") 
        output.writelines("|}")
    print("Action completed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python WikiTaskListGen.py location loc_id")
        sys.exit(1)
    else:
        location, loc_id = sys.argv[1].lower(), sys.argv[2]
        location = match_location(location)
        main(location, loc_id)