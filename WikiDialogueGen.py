import json

i2_file = "C:\\Users\\Matth\\Documents\\DataExtr\\Working_Code\\i2subset_english.json"
output_file = "C:\\Users\\Matth\\Documents\\DataExtr\\Working_Code\\dialogue_output.txt"
gde_file = "C:\\Users\\Matth\\Documents\\DataExtr\\Working_Code\\gde_data.json"

CHAR_CONVERT = {"catpepper": "Pepper",
                "catginger": "Ginger",
                "catace": "Ace"}

def get_questdescs():
    descriptions = {}
    with open(i2_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            if line.get("Term").split("_")[0] == "DialogueTalk" or line.get("Term").split("_")[0] == "Dialogue/DialogueTalk":
                descriptions[line.get("Term")] = line.get("Languages")[0].replace("\n", " ").replace("\"", '"')
    return descriptions

with open(gde_file, "r", encoding="utf8") as file, open(output_file, "w", encoding="utf8") as output:
    descriptions = get_questdescs()
    prev_quest = None
    data = json.load(file)
    for line in data:
        if data[line].get("1070") == "Dialogue":
            current_quest = data[line].get("78")
            quest_key = descriptions.get(data[line].get("88"))
            char_key = data[line].get("94")
            if char_key.lower() in CHAR_CONVERT.keys():
                char_key = CHAR_CONVERT.get(char_key.lower())
            if char_key == "":
                char_key = None
            if prev_quest != current_quest:
                prev_quest = current_quest
                output.writelines("</blockquote>\n\n''' Dialogue '''\n<blockquote>")
                output.writelines("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")
            else:
                prev_quest = current_quest
                output.writelines("\n\n")
                output.writelines("<small>'''"+str(char_key)+"'''  "+str(quest_key)+"</small>")            


