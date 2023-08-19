from .utils.area_unlocks_dict import area_unlocks_dict
from .utils.area_tasks_dict import area_tasks_dict
from .utils.pywikibot_login import wiki_upload
from .utils.output_file import output_file
from .utils.read_i2 import read_i2

from .area_dialogue import area_dialogue
from .task_list import task_list

def area_page(location, loc_id, upload):
    task_list(location, loc_id, upload)
    chars = area_dialogue(location, upload)
    descriptions = read_i2()
    output = []
    namekey = descriptions.get("questtitle_"+location) if descriptions.get("questtitle_"+location) != None else descriptions.get("namekey_"+location)
    output.append("{{DISPLAYTITLE:"+namekey+"}}\n{{Spoiler}}\n{{InfoboxArea\n|image=<gallery>\n</gallery>\n|unlocksafter=")
    prev_areas = []
    tasks = area_tasks_dict()
    unlocks = area_unlocks_dict()
    for elem in tasks[location]:
        for areas in unlocks.keys():
            if elem in unlocks[areas] and areas != location and areas:
                prev_areas.append(areas)
    for i in range(0,len(prev_areas)):
        prev_areas[i] = descriptions.get("questtitle_"+prev_areas[i]) if descriptions.get("questtitle_"+prev_areas[i]) != None else descriptions.get("namekey_"+prev_areas[i])
    for elem in prev_areas:
        output.append("*[["+elem+"]]\n")
    output.append("|unlocks=-\n|cast=")
    for character in chars:
        output.append("*[["+character+"]]\n")
    output.append("|reward=}}\n\n")
    area_complete = descriptions.get("completedesckey_"+location)
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
    if upload == False:
        with open(output_file("area_page_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/"+namekey, text)
    print("Action completed.")