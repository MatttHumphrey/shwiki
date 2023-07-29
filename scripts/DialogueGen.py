from utils.output_file import output_file
from utils.read_i2 import read_i2
from utils.read_gde import read_gde
from utils.task_dic import task_dict
from utils.locate_task import locate_task
from utils.match_location import match_location
import sys

def main(location):
    descriptions = read_i2()
    data = read_gde()
    with open(output_file("area_dialogue_output.txt"), "w", encoding="utf8") as output:
        chars, counter, prev_area, prev_quest = [], 0, None, None
        taskdict = task_dict()
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
                        output.writelines("</blockquote>\n\n")
                    output.writelines(f"''' Dialogue {str(counter)} '''\n<blockquote>")
                    output.writelines(f"<small>'''{str(char_key)}'''  {str(quest_key)}</small>")
                else:
                    prev_quest = current_quest
                    output.writelines("\n\n")
                    output.writelines(f"<small>'''{str(char_key)}'''  {str(quest_key)}</small>")    
        output.writelines("</blockquote>\n[[Category:Dialogue]]") 
    print("Action completed.")          

def full_dialogue():
    with open(output_file("dialogue_output.txt"), "w", encoding="utf8") as output:
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
    valid_functions = {
        "full_dialogue": (full_dialogue, 1, []),
        "main": (main, 2, ["location"])
    }
    if len(sys.argv) < 2 or sys.argv[1] not in valid_functions:
        print(f"Invalid function name. Available functions: {', '.join(valid_functions.keys())}")
    else:
        func, arg_count, args = valid_functions[sys.argv[1]]
        if len(sys.argv) != arg_count + 1:
            print(f"Usage: python WikiDialogueGen.py {sys.argv[1]} {' '.join(args)}")
        else:
            if args:
                location = sys.argv[2]
                location = match_location(location)
                func(location)
            else:
                func()
