from .utils.pywikibot_login import wiki_upload
from .utils.output_file import output_file
from .utils.string_hash import string_hash
from .utils.read_gde import read_gde
from .utils.read_i2 import read_i2

import collections

def area_items(location, upload):
    '''
    Generates a table listing all items needed for a specified area.

    Keyword Arguments:
    location            - The name of the area we are generating the table for
    upload              - Optional trigger to upload the page automatically to the wiki
    '''
    area_total = {}
    data = read_gde()
    descriptions = read_i2()
    stringhash = string_hash()
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest" and data[line].get(stringhash["AreaGroupKey"]).lower() == location:
            items = data[line].get(stringhash["NeedItem"])
            counts = data[line].get(stringhash["NeedItemCount"])
            for i in range(0, len(items)):
                if items[i].lower() != "lobbyeventpoint":
                    if items[i].lower() not in area_total.keys():
                        area_total[items[i].lower()] = 0
                    area_total[items[i].lower()] += counts[i]
    sorted_totals = collections.OrderedDict(sorted(area_total.items()))
    output = []
    output.append("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
    for id in sorted_totals.keys():
        if id == "eventcoin":
            output.append("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
            output.append(f"|{sorted_totals.get(id)}\n|")
        else:
            item_name, item_level = id.split("_")
            output.append("-\n|{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
            output.append(f"|{sorted_totals.get(id)}\n|")
    output.append("}")
    text = "".join(output)
    if upload == False:
        with open(output_file("area_items_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        namekey = descriptions.get("questtitle_"+location) if descriptions.get("questtitle_"+location) != None else descriptions.get("namekey_"+location)
        wiki_upload("User:WFrck/Total_Area_Items/"+namekey, text)
    print("Action completed.")