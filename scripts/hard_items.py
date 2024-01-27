import collections

from .utils.pywikibot_login import wiki_upload
from .utils.read_data import read_gde, read_i2
from .utils.match_location import area_dict
from .utils.output_file import output_file
from .utils.string_hash import string_hash
from .utils.hard_items import HARD_ITEMS

def hard_items(upload = False):
    '''
    Generates a table listing the hard items needed for every area in the game.

    Keyword Arguments:
    upload              - Optional trigger to upload the page automatically to the wiki
    '''
    gde_data = read_gde()
    i2_data = read_i2()
    stringhash = string_hash(gde_data)
    area_list = list(area_dict(gde_data, i2_data).keys())
    output = []
    for location in area_list:
        namekey = i2_data.get("questtitle_"+location.lower()) if i2_data.get("questtitle_"+location.lower()) is not None else i2_data.get("namekey_"+location.lower())
        output.append(f"=={namekey}==\n")
        area_total = {item: 0 for item in HARD_ITEMS}
        for line in gde_data:
            if gde_data[line].get(stringhash["_gdeSchema"]) == "Quest" and gde_data[line].get(stringhash["AreaGroupKey"]).lower() == location:
                items = gde_data[line].get(stringhash["NeedItem"])
                counts = gde_data[line].get(stringhash["NeedItemCount"])
                for item, count in zip(items, counts):
                    if item.lower() in HARD_ITEMS:
                        area_total[item.lower()] = area_total.get(item.lower(), 0) + count
        sorted_totals = collections.OrderedDict(sorted(area_total.items()))
        sorted_totals = {key: value for key, value in sorted_totals.items() if value != 0}
        output.append("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
        for ids in sorted_totals.keys():
            if ids == "eventcoin":
                output.append("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
            else:
                item_name, item_level = ids.split("_")
                output.append("-\n|{{Item | "+i2_data.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
            output.append(f"|{sorted_totals.get(ids)}\n|")
        output.append("}\n\n")
    text = "".join(output)
    if upload is False:
        with open(output_file("hard_items_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/Hard_Items", text)
    print("Action completed.")
