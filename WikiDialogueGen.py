import json
import os.path as path
from convert import CHAR_CONVERT

i2_file = path.join(path.dirname(__file__),"i2subset_english.json")
output_file = path.join(path.dirname(__file__),"dialogue_output.txt")
gde_file = path.join(path.dirname(__file__),"gde_data.json")

def get_questdescs():
    descriptions = {}
    with open(i2_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            if line.get("Term").split("_")[0] == "DialogueTalk" or line.get("Term").split("_")[0] == "Dialogue/DialogueTalk":
                descriptions[line.get("Term")] = line.get("Languages")[0].replace("\n", " ").replace("\"", '"')
    return descriptions

def task_dic():
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
dic = task_dic() 

def locate_task(key):
    indicator = False
    while indicator == False:
        for area in dic.keys():
            if key in dic[area]:
                return area
        else:
            indicator = True

def main(loc):
    with open(gde_file, "r", encoding="utf8") as file, open(output_file, "w", encoding="utf8") as output:
        descriptions = get_questdescs()
        data = json.load(file)
        prev_quest = None
        prev_area = None
        counter = 0
        chars = []
        for line in data:
            if data[line].get("1071") == "Dialogue":
                current_quest = data[line].get("78")
                quest_key = descriptions.get(data[line].get("88"))
                char_key = data[line].get("94")
                current_area = locate_task(current_quest)
                if current_area != loc:
                    continue 
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
                        output.writelines("''' Dialogue "+str(counter)+" '''\n<blockquote>")
                    else:
                        output.writelines("</blockquote>\n\n''' Dialogue "+str(counter)+" '''\n<blockquote>")
                    output.writelines("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")
                else:
                    prev_quest = current_quest
                    output.writelines("\n\n")
                    output.writelines("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")    
        output.writelines("</blockquote>\n[[Category:Dialogue]]")           

def full_dialogue():
    with open(gde_file, "r", encoding="utf8") as file, open(output_file, "w", encoding="utf8") as output:
        descriptions = get_questdescs()
        data = json.load(file)
        prev_quest = None
        prev_area = None
        counter = 0
        chars = []
        for line in data:
            if data[line].get("1071") == "Dialogue":
                current_quest = data[line].get("78")
                quest_key = descriptions.get(data[line].get("88"))
                char_key = data[line].get("94")
                current_area = locate_task(current_quest)
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
                    output.writelines("</blockquote>\n\n''' Dialogue "+str(counter)+" '''\n<blockquote>")
                    output.writelines("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")
                else:
                    prev_quest = current_quest
                    output.writelines("\n\n")
                    output.writelines("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")    
        output.writelines("</blockquote>\n[[Category:Dialogue]]")