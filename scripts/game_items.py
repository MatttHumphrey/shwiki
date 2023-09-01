from .utils.pywikibot_login import wiki_upload
from .utils.output_file import output_file
from .utils.string_hash import string_hash
from .utils.read_gde import read_gde
from .utils.read_i2 import read_i2

import collections

def game_items(upload):
    item_totals = {}
    descriptions = read_i2()
    data = read_gde()
    stringhash = string_hash()
    for line in data:
        if data[line].get(stringhash["_gdeSchema"]) == "Quest":
            items = data[line].get(stringhash["NeedItem"])
            counts = data[line].get(stringhash["NeedItemCount"])
            for item, count in zip(items, counts):
                if item.lower() != "lobbyeventpoint":
                    item_totals[item.lower()] = item_totals.get(item.lower(), 0) + count
    item_totals = collections.OrderedDict(sorted(item_totals.items()))
    output = []
    output.append("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|-")
    for id, count in item_totals.items():
        if id == "eventcoin":
            output.append("\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
            output.append(f"|{count}\n|-")
        else:
            item_name, item_level = id.split("_")
            output.append("\n|{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
            output.append(f"|{count}\n|-")
    text_list = list("".join(output))
    text_list[-1] = "}"
    text = "".join(text_list)
    if upload == False:
        with open(output_file("game_items_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/Total_Game_Items", text)
    print("Action completed.")