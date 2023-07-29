from utils.output_file import output_file
from utils.locate_task import locate_task
from utils.task_dic import task_dict
from utils.read_gde import read_gde
from utils.read_i2 import read_i2

def full_dialogue():
    with open(output_file("full_dialogue_output.txt"), "w", encoding="utf8") as output:
        descriptions = read_i2()
        data = read_gde()
        chars, counter, prev_area, prev_quest = [], 0, None, None
        taskdict = task_dict()
        for line in data:
            if data[line].get("1071") == "Dialogue":
                current_quest = data[line].get("78")
                quest_key = descriptions.get(data[line].get("88").lower())
                char_key = data[line].get("94")
                current_area = locate_task(current_quest,taskdict)
                if "cat" in char_key.lower():
                    char_key = char_key.replace("Cat", "", 1)
                if char_key == "":
                    char_key = None
                if char_key and char_key not in chars:
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
    print("Action completed.")

if __name__ == "__main__":
    full_dialogue()