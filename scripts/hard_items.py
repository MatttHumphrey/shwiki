from .utils.pywikibot_login import wiki_upload
from .utils.output_file import output_file
from .utils.string_hash import string_hash
from .utils.hard_items import HARD_ITEMS
from .utils.area_dict import area_dict
from .utils.read_gde import read_gde
from .utils.read_i2 import read_i2
import collections

def hard_items(upload):
    descriptions = read_i2()
    data = read_gde()
    area_list = area_dict().keys()
    stringhash = string_hash()
    output = []
    for location in area_list:
        namekey = descriptions.get("questtitle_"+location.lower()) if descriptions.get("questtitle_"+location.lower()) != None else descriptions.get("namekey_"+location.lower())
        output.append(f"=={namekey}==\n")
        area_total = {item: 0 for item in HARD_ITEMS}
        for line in data:
            if data[line].get(stringhash[0]) == "Quest" and data[line].get(stringhash[1]).lower() == location:
                items = data[line].get(stringhash[11])
                counts = data[line].get(stringhash[12])
                for item, count in zip(items, counts):
                    if item.lower() in HARD_ITEMS:
                        area_total[item.lower()] = area_total.get(item.lower(), 0) + count
        sorted_totals = collections.OrderedDict(sorted(area_total.items()))
        sorted_totals = {key: value for key, value in sorted_totals.items() if value != 0}
        output.append("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
        for id in sorted_totals.keys():
            if id == "eventcoin":
                output.append("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
            else:
                item_name, item_level = id.split("_")
                output.append("-\n|{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
            output.append(f"|{sorted_totals.get(id)}\n|")
        output.append("}\n\n")
    text = "".join(output)
    if upload == False:
        with open(output_file("hard_items_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/Hard_Items", text)
    print("Action completed.")