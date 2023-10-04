from .utils.area_unlocks_dict import area_unlocks_dict
from .utils.area_tasks_dict import area_tasks_dict
from .utils.pywikibot_login import wiki_upload
from .utils.output_file import output_file
from .utils.read_i2 import read_i2

from .area_dialogue import area_dialogue
from .task_list import task_list

def area_page(location, loc_id, upload):
    '''
    Generates the fully formatted area page for a given area, along with the task list and dialogue.
    Note: The area numbering, profile picture unlocked, before/after pictures and the page emoji will need manually adding.

    Keyword Arguments:
    location            - The name of the area we are generating the task list for
    loc_id              - A short 2-3 letter code to name the tasks after
    upload              - Optional trigger to upload the page automatically to the wiki
    '''
    task_list(location, loc_id, upload)
    characters = area_dialogue(location, upload)
    descriptions = read_i2()
    output = []
    prev_areas = []
    task_dict = area_tasks_dict()
    unlocks_dict = area_unlocks_dict()
    namekey = descriptions.get("questtitle_"+location) if descriptions.get("questtitle_"+location) is not None else descriptions.get("namekey_"+location)
    output.append("{{DISPLAYTITLE:"+namekey+"}}\n{{Spoiler}}\n{{InfoboxArea\n|image=<gallery>\n</gallery>\n|unlocksafter=")
    for elem in task_dict[location]:
        for area, unlock_list in unlocks_dict.items():
            if elem in unlock_list and area != location and area:
                area = descriptions.get("questtitle_"+area) if descriptions.get("questtitle_"+area) is not None else descriptions.get("namekey_"+area)
                prev_areas.append(area)
    for elem in prev_areas:
        output.append("*[["+elem+"]]\n")
    output.append("|unlocks=-\n|cast=")
    for char in characters:
        output.append("*[["+char+"]]\n")
    output.append("|reward=}}\n\n")
    area_complete = descriptions.get("completedesckey_"+location)
    output.append("<small>''\""+area_complete+"\"''<br>\n-Sunny</small>\n\n")
    output.append("'''"+namekey+"''' is the xth area that Sunny renovates. It is unlocked after completing [[")
    format_prev_areas = "]] and [[".join(prev_areas)
    output.append(format_prev_areas+"]].\n\n")
    output.append("==Plot==\n?\n\n==Cast==\n<gallery>\n")
    for character in characters:
        output.append("File:Cast- "+character+".png|"+character+"\n")
    output.append("</gallery>\n\n")
    output.append("==Story==\n<div class=\"mw-collapsible mw-collapsed\">\nClick '''Expand''' to view dialogue\n<div class=\"mw-collapsible-content\">\n{{/Dialogue}}\n</div>\n</div>\n\n")
    output.append("==Tasks==\n{{/Tasks}}\n\n{{GameplayMenu}}\n[[Category:Areas]]\n__NOTOC__")
    text = "".join(output)
    if upload is False:
        with open(output_file("area_page_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/"+namekey, text)
    print("Action completed.")
