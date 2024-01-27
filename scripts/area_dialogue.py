from .utils.task_dicts import dialogue_task_dict, locate_task
from .utils.pywikibot_login import wiki_upload
from .utils.read_data import read_gde, read_i2
from .utils.string_hash import string_hash
from .utils.output_file import output_file

def area_dialogue(location, upload = False):
    '''
    Generates all the dialogue spoken in a given area.
    Note: Character name may show as "None" where one is not defined in the game's files.

    Keyword Arguments:
    location            - The name of the area we are generating the dialogue for
    upload              - Optional trigger to upload the page automatically to the wiki

    Return Value:
    A list of all characters who have spoken in the area, used only in area_page.py and unnecessary otherwise.
    '''
    gde_data = read_gde()
    i2_data = read_i2()
    stringhash = string_hash(gde_data)
    task_dict = dialogue_task_dict(gde_data)
    characters = []
    counter = 0
    output = []
    prev_area = None
    prev_quest = None
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Dialogue":
            current_quest = gde_data[line].get(stringhash["Group"])
            quest_key = i2_data.get(gde_data[line].get(stringhash["DescriptionKey"]).lower())
            char_key = gde_data[line].get(stringhash["Actor"])
            current_area = locate_task(current_quest, task_dict)
            if str(current_area).lower() != location:
                continue
            if "cat" in char_key.lower():
                char_key = char_key.replace("Cat", "", 1)
            if char_key and char_key not in characters:
                characters.append(char_key)
            if prev_quest != current_quest:
                if current_area == prev_area and current_area is not None:
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
    if upload is False:
        with open(output_file("area_dialogue_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        namekey = i2_data.get("questtitle_"+location) if i2_data.get("questtitle_"+location) is not None else i2_data.get("namekey_"+location)
        wiki_upload("User:WFrck/"+namekey+"/Dialogue", text)
    print("Action completed.")
    return characters
