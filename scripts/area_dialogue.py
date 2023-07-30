from .utils.dialogue_task_dict import dialogue_task_dict
from .utils.pywikibot_login import wiki_upload
from .utils.locate_task import locate_task
from .utils.output_file import output_file
from .utils.read_gde import read_gde
from .utils.read_i2 import read_i2

def area_dialogue(location, upload):
    descriptions = read_i2()
    data = read_gde()
    output = []
    chars, counter, prev_area, prev_quest = [], 0, None, None
    taskdict = dialogue_task_dict()
    for line in data:
        if data[line].get("1071") == "Dialogue":
            current_quest = data[line].get("78")
            quest_key = descriptions.get(data[line].get("88").lower())
            char_key = data[line].get("94")
            current_area = locate_task(current_quest,taskdict)
            if str(current_area).lower() != location:
                continue 
            if "cat" in char_key.lower():
                char_key = char_key.replace("Cat", "", 1)
            if char_key and char_key not in chars:
                chars.append(char_key)
            if prev_quest != current_quest:
                if current_area == prev_area and current_area != None:
                    counter += 1
                else:
                    counter = 1
                prev_quest = current_quest
                prev_area = current_area
                if counter > 1:
                    output.append("</blockquote>\n\n")
                output.append(f"''' Dialogue {str(counter)} '''\n<blockquote>")
                output.append(f"<small>'''{str(char_key)}'''  {str(quest_key)}</small>")
            else:
                prev_quest = current_quest
                output.append("\n\n")
                output.append(f"<small>'''{str(char_key)}'''  {str(quest_key)}</small>")    
    output.append("</blockquote>\n[[Category:Dialogue]]") 
    text = "".join(output)
    if upload == False:
        with open(output_file("area_dialogue_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        namekey = descriptions.get("questtitle_"+location) if descriptions.get("questtitle_"+location) != None else descriptions.get("namekey_"+location)
        wiki_upload("User:WFrck/"+namekey+"/Dialogue", text)
    print("Action completed.")
    return chars