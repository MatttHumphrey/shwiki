import json
import sys
import os.path as path
from convert import CHAR_CONVERT
from modules import I2_FILE, GDE_FILE, read_i2, task_dic, locate_task

OUTPUT_FILE = path.join(path.dirname(__file__),"dialogue_output.txt")

def main(loc):
    with open(GDE_FILE, "r", encoding="utf8") as file, open(OUTPUT_FILE, "w", encoding="utf8") as output:
        descriptions = read_i2()
        data = json.load(file)
        prev_quest = None
        prev_area = None
        counter = 0
        chars = []
        dic = task_dic()
        for line in data:
            if data[line].get("1071") == "Dialogue":
                current_quest = data[line].get("78")
                quest_key = descriptions.get(data[line].get("88"))
                char_key = data[line].get("94")
                current_area = locate_task(current_quest,dic)
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
    with open(GDE_FILE, "r", encoding="utf8") as file, open(OUTPUT_FILE, "w", encoding="utf8") as output:
        descriptions = read_i2()
        data = json.load(file)
        prev_quest = None
        prev_area = None
        counter = 0
        chars = []
        dic = task_dic()
        for line in data:
            if data[line].get("1071") == "Dialogue":
                current_quest = data[line].get("78")
                quest_key = descriptions.get(data[line].get("88"))
                char_key = data[line].get("94")
                current_area = locate_task(current_quest,dic)
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

if __name__ == "__main__":
    if sys.argv[1] == "full_dialogue":
        if len(sys.argv) != 2:
            print("Usage: python WikiDialogueGen.py full_dialogue")
        else:
            full_dialogue()
    elif sys.argv[1] == "main":
        if len(sys.argv) != 3:
            print("Usage: python WikiDialogueGen.py full_dialogue location")
        else:
            location = sys.argv[2]
            main(location)
    else:
        print("Invalid function name. Available functions: main, full_dialogue")