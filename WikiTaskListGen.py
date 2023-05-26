import json

TOOL_CONVERT = {"gardentool":"Garden Tools", 
               "seedpouch":"Seed Pouch",
               "tree":"Tree of Lights",
               "gardengloves":"Garden Gloves",
               "cleaningtool":"Cleaning Tools",
               "tools":"Tools",
               "flower":"Yellow Lily",
               "anemone":"Anemone",
               "butterfly":"Butterfly",
               "bench":"Bench",
               "sketchtool":"Designing Tools",
               "tile":"Tile",
               "fond":"Pond",
               "brick":"Brick",
               "lemonbag":"Lemon Bag",
               "paint":"Paints",
               "vase":"Vase",
               "light":"Light",
               "statue":"Statue",
               "screws":"Nails",
               "birds":"Bird Statue",
               "logs":"Logs",
               "cleansers":"Cleansers",
               "xp":"Experience Points (XP)",
               "eventcoin":"EventCoin",
               "stonebasket":"Stone Basket",
               "terrarium":"Terrarium"} 

REWARD_CONVERT = {"birdcage":"Golden Cage",
                 "bluechest":"Granma's Chest",
                 "brownchest":"Mystery Box",
                 "cleaningtoolbox":"Cleaning Tool Box",
                 "cleaningpack":"Old Cleaning Box",
                 "flowerpot":"Flowerpot",
                 "tree":"Tree of Lights",
                 "gardeningpack":"Old Gardening Tool Box",
                 "gardentool":"Garden Tools",
                 "gold":"Coins",
                 "seedpack":"Old Seed Box",
                 "sketchpack":"Old Design Tool Box",
                 "toolpack":"Old Tool Box",
                 "xp":"Experience Points (XP)",
                 "goldchest":"Gold Pocket",
                 "jewel":"Jewels",
                 "magictimer":"Magic Timer",
                 "sketchtoolbox":"Workbench",
                 "timeskip":"Hourglass"}

i2_file = "C:\\Users\\Matth\\Documents\\DataExtr\\Working_Code\\i2subset_english.json"
gde_file = "C:\\Users\\Matth\\Documents\\DataExtr\\Working_Code\\gde_data.json"
output_file = "C:\\Users\\Matth\\Documents\\DataExtr\\Working_Code\\task_output.txt"

def get_questdescs():
    descriptions = {}
    with open(i2_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            if line.get("Term").split("_", 1)[0] == "QuestDesc":
                descriptions[line.get("Term").lower()] = line.get("Languages")[0]
    return descriptions

def tasknumbers(loc, id):
    id_dict = {}
    n = 1
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1070") == "Quest" and data[line].get("18") == loc:
                id_dict[data[line].get("2")] = f"{id}-{n}"
                n += 1
    return id_dict

def main(loc, id):
    descriptions = get_questdescs()
    task_nos = tasknumbers(loc, id)
    with open(gde_file, "r", encoding="utf8") as file, \
         open(output_file, "w", encoding="utf8") as output:
        output.writelines("\'''Note:\''' Due to the game's constant updates, the tasks on this page may not always be accurate. If you have any new information, feel free to go to the \"Front Gate/Tasks\" page and edit accordingly.\n\n{| class=\"article-table\" style=\"font-size:15px;\"\n!style=\"width:100px\"|# \n!Name \n!style=\"width:100px\"|Opens \n!Items \n!Rewards \n|-\n")
        data = json.load(file)
        for line in data:
            if data[line].get("1070") == "Quest" and data[line].get("18") == loc:
                quest_key = data[line].get("2")
                desc_key = data[line].get("34").lower()
                unlock_list = []
                for item in data[line].get("5"):
                    unlock_list.append(task_nos[item])
                unlock_key = "<br>".join(unlock_list)
                item_dict = {}
                for i in range(0,len(data[line].get("23"))):
                    item_dict[data[line].get("23")[i]] = data[line].get("26")[i]
                item_list = []
                for item in data[line].get("23"):
                    if item == "EventCoin":
                        item_list.append(f"{item_dict[item]} [[File:LemonMoney.png|30px]] [[Lemon Event|Money]]")
                    else:
                        item_name, item_level = item.split("_")
                        if item_dict[item] == 1:
                            item_list.append("{{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}")
                        else:
                            item_list.append(str(item_dict[item])+"x {{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}")
                item_key = "<br>".join(item_list)
                reward_list = []
                for reward in data[line].get("16"):
                    reward_name, reward_level = reward.split("_")
                    reward_list.append("{{Item | "+REWARD_CONVERT[reward_name.lower()]+" | "+reward_level.lstrip("0")+"}}")
                reward_key = "<br>".join(reward_list)
                output.writelines(f"|{task_nos.get(quest_key)}\n|{descriptions.get(desc_key)}\n|{unlock_key}\n|{item_key}\n|{reward_key}\n|-\n") 

numbers = main("Lighthouse","LGT")
