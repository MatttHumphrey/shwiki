from .utils.task_dicts import dialogue_task_dict, locate_task
from .utils.read_data import read_gde, read_i2
from .utils.output_file import output_file
from .utils.string_hash import string_hash

def full_dialogue():
    '''
    Generates all the dialogue spoken throughout the game
    Useful for getting dialogue for events, since they do not have a specific area tag.
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
            if "cat" in char_key.lower():
                char_key = char_key.replace("Cat", "", 1)
            if char_key == "":
                char_key = None
            if char_key and char_key not in characters:
                characters.append(char_key)
            if prev_quest != current_quest:
                if current_area == prev_area and current_area is not None:
                    counter += 1
                else:
                    counter = 1
                prev_quest = current_quest
                prev_area = current_area
                output.append("</blockquote>\n\n''' Dialogue "+str(counter)+" '''\n<blockquote>")
                output.append("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")
            else:
                prev_quest = current_quest
                output.append("\n\n")
                output.append("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")
    output.append("</blockquote>\n[[Category:Dialogue]]")
    text = "".join(output)
    with open(output_file("full_dialogue_output.txt"), "w", encoding="utf8") as output:
        output.writelines(text)
    print("Action completed.")
