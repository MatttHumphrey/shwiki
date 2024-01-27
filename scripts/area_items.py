import collections

from .utils.pywikibot_login import wiki_upload
from .utils.read_data import read_gde, read_i2
from .utils.output_file import output_file
from .utils.string_hash import string_hash

def area_items(location, upload = False):
    '''
    Generates a table listing all items needed for a specified area.

    Keyword Arguments:
    location            - The name of the area we are generating the table for
    upload              - Optional trigger to upload the page automatically to the wiki
    '''
    gde_data = read_gde()
    i2_data = read_i2()
    stringhash = string_hash(gde_data)
    area_total = {}
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Quest" and gde_data[line].get(stringhash["AreaGroupKey"]).lower() == location:
            items = gde_data[line].get(stringhash["NeedItem"])
            counts = gde_data[line].get(stringhash["NeedItemCount"])
            for index, item in enumerate(items):
                if item.lower() != "lobbyeventpoint":
                    if item.lower() not in area_total:
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
            output.append("-\n|{{Item | "+i2_data.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
            output.append(f"|{sorted_totals.get(ids)}\n|")
    output.append("}")
    text = "".join(output)
    if upload is False:
        with open(output_file("area_items_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        namekey = i2_data.get("questtitle_"+location) if i2_data.get("questtitle_"+location) is not None else i2_data.get("namekey_"+location)
        wiki_upload("User:WFrck/Total_Area_Items/"+namekey, text)
    print("Action completed.")
