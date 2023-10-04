import collections

from .utils.pywikibot_login import wiki_upload
from .utils.output_file import output_file
from .utils.string_hash import string_hash
from .utils.read_gde import read_gde
from .utils.read_i2 import read_i2

def area_items(location, upload = False):
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
            for index, item in enumerate(items):
                if item.lower() != "lobbyeventpoint":
                    if item.lower() not in area_total.keys():
                        area_total[item.lower()] = 0
                    area_total[item.lower()] += counts[index]
    sorted_totals = collections.OrderedDict(sorted(area_total.items()))
    output = []
    output.append("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
    for ids in sorted_totals.keys():
        if ids == "eventcoin":
            output.append("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
            output.append(f"|{sorted_totals.get(ids)}\n|")
        else:
            item_name, item_level = ids.split("_")
            output.append("-\n|{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
            output.append(f"|{sorted_totals.get(ids)}\n|")
    output.append("}")
    text = "".join(output)
    if upload is False:
        with open(output_file("area_items_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        namekey = descriptions.get("questtitle_"+location) if descriptions.get("questtitle_"+location) is not None else descriptions.get("namekey_"+location)
        wiki_upload("User:WFrck/Total_Area_Items/"+namekey, text)
    print("Action completed.")
