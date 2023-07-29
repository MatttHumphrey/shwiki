import json
import pywikibot
import os.path as path
from convert import TOOL_CONVERT, REWARD_CONVERT, CHAR_CONVERT

i2_file = path.join(path.dirname(__file__),"i2subset_english.json")
gde_file = path.join(path.dirname(__file__),"gde_data.json")

def wiki_upload(pagename, text):
    site = pywikibot.Site('en', 'sunny-house')
    page = pywikibot.Page(site, 'User:WFrck/'+pagename)
    page.text = text
    page.save("Created area pages (automated)")

def read_i2():
    descriptions = {}
    with open(i2_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            descriptions[line.get("Term").lower()] = line.get("Languages")[0]
    return descriptions

def get_questdescs():
    descriptions = {}
    with open(i2_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            if line.get("Term").split("_")[0] == "DialogueTalk" or line.get("Term").split("_")[0] == "Dialogue/DialogueTalk":
                descriptions[line.get("Term")] = line.get("Languages")[0].replace("\n", " ").replace("\"", '"')
    return descriptions

def tasknumbers(loc, id):
    id_dict = {}
    n = 1
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest" and data[line].get("18") == loc:
                id_dict[data[line].get("2")] = f"{id}-{n}"
                n += 1
    return id_dict

def dialogue_task_dic():
    dic = {}
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest":
                area = data[line].get("20")
                if dic.get(area) == None:
                    dic[area] = []
                if data[line].get("36") != 0:
                    dic[area].append(data[line].get("36"))
                if data[line].get("38") != 0:
                        dic[area].append(data[line].get("38"))  
    return dic
dic = dialogue_task_dic()

def unlock_dic():
    dic = {}
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest":
                area = data[line].get("20")
                unlocks = data[line].get("5")
                if dic.get(area) == None:
                    dic[area] = []
                if unlocks == []:
                    continue
                for item in unlocks:
                    dic[area].append(item)              
    return dic

def task_dic():
    dic = {}
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest":
                area = data[line].get("20")
                tasks = data[line].get("2")
                if dic.get(area) == None:
                    dic[area] = []
                dic[area].append(tasks)              
    return dic

def locate_task(key):
    indicator = False
    while indicator == False:
        for area in dic.keys():
            if key in dic[area]:
                return area
        else:
            indicator = True

def main(loc, id):
    output = []
    descriptions = read_i2()
    task_nos = tasknumbers(loc, id)
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
    namekey = descriptions.get("questtitle_"+loc.lower()) if descriptions.get("questtitle_"+loc.lower()) != None else "Front Gate"
    output.append("\'''Note:\''' Due to the game's constant updates, the tasks on this page may not always be accurate. If you have any new information, feel free to go to the \""+namekey+"/Tasks\" page and edit accordingly.\n\n{| class=\"article-table\" style=\"font-size:15px;\"\n!style=\"width:100px\"|# \n!Name \n!style=\"width:100px\"|Opens \n!Items \n!Rewards \n")
    for line in data:
        if data[line].get("1071") != "Quest" or data[line].get("18") != loc:
            continue
        quest_key = data[line].get("2")
        desc_key = data[line].get("34").lower()
        unlock_list = []
        for item in data[line].get("5"):
            unlock_list.append(task_nos[item]) if item in task_nos.keys() else unlock_list.append(str(item))
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
                item_id = str(item_dict[item])+"x {{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}" if item_dict[item] != 1 else "{{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}"
                item_list.append(item_id)
        item_key = "<br>".join(item_list)
        reward_list = []
        for reward in data[line].get("16"):
            reward_name, reward_level = reward.split("_")
            reward_list.append("{{Item | "+REWARD_CONVERT[reward_name.lower()]+" | "+reward_level.lstrip("0")+"}}")
        reward_key = "<br>".join(reward_list)
        output.append(f"|-\n|{task_nos.get(quest_key)}\n|{descriptions.get(desc_key)}\n|{unlock_key}\n|{item_key}\n|{reward_key}\n") 
    output.append("|}\n[[Category:Tasks]]")
    text = "".join(output)
    wiki_upload(namekey+"/Tasks", text)
    output = [] 
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
    prev_quest = None
    prev_area = None
    counter = 0
    chars = []
    for line in data:
        if data[line].get("1071") == "Dialogue":
            current_quest = data[line].get("78")
            current_area = locate_task(current_quest)
            if current_area != loc:
                continue 
            quest_key = descriptions.get(data[line].get("88").lower())
            char_key = data[line].get("94")
            if char_key.lower() in CHAR_CONVERT.keys():
                char_key = CHAR_CONVERT.get(char_key.lower())
            if char_key == "":
                char_key = None
            if char_key != None and char_key not in chars:
                chars.append(char_key)
            if prev_quest != current_quest:
                if current_area == prev_area and current_area != None:
                    counter += 1
                else:
                    counter = 1
                prev_quest = current_quest
                prev_area = current_area
                if counter == 1:
                    output.append("''' Dialogue "+str(counter)+" '''\n<blockquote>")
                else:
                    output.append("</blockquote>\n\n''' Dialogue "+str(counter)+" '''\n<blockquote>")
                output.append("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")
            else:
                prev_quest = current_quest
                output.append("\n\n")
                output.append("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")    
    output.append("</blockquote>\n[[Category:Dialogue]]")        
    text = "".join(output)
    wiki_upload(namekey+"/Dialogue", text) 
    text = ""
    tasks = task_dic()
    unlocks = unlock_dic()
    output = []
    prev_areas = []
    for elem in tasks[loc]:
        for areas in unlocks.keys():
            if elem in unlocks[areas] and areas != loc:
                prev_areas.append(areas)
    for i in range(0,len(prev_areas)):
        prev_areas[i] = descriptions.get("questtitle_"+prev_areas[i].lower()) if descriptions.get("questtitle_"+prev_areas[i].lower()) != None else "Front Gate"
    output.append("{{DISPLAYTITLE:"+namekey+"}}\n{{Spoiler}}\n{{InfoboxArea\n|image=<gallery>\n</gallery>\n")
    output.append("|unlocksafter=")
    for elem in prev_areas:
        output.append("*[["+elem+"]]\n")
    output.append("|unlocks=-\n|cast=")
    for character in chars:
        output.append("*[["+character+"]]\n")
    output.append("|reward=}}\n\n")
    area_complete = descriptions.get("completedesckey_"+loc.lower()).replace("\n"," ")
    output.append("<small>''\""+area_complete+"\"''<br>\n-Sunny</small>\n\n")
    output.append("'''"+namekey+"''' is the xth area that Sunny renovates. It is unlocked after completing [[")
    format_prev_areas = "]] and [[".join(prev_areas)
    output.append(format_prev_areas+"]].\n\n")
    output.append("==Plot==\n?\n\n==Cast==\n<gallery>\n")
    for character in chars:
        output.append("File:Cast- "+character+".png|"+character+"\n")
    output.append("</gallery>\n\n")
    output.append("==Story==\n<div class=\"mw-collapsible mw-collapsed\">\nClick '''Expand''' to view dialogue\n<div class=\"mw-collapsible-content\">\n{{/Dialogue}}\n</div>\n</div>\n\n")
    output.append("==Tasks==\n{{/Tasks}}\n\n{{GameplayMenu}}\n[[Category:Areas]]\n__NOTOC__")
    text = "".join(output)
    wiki_upload(namekey, text)