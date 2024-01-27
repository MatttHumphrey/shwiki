import collections

from .utils.pywikibot_login import wiki_upload
from .utils.read_data import read_gde, read_i2
from .utils.output_file import output_file
from .utils.string_hash import string_hash

def game_items(upload = False):
    '''
    Generates a table listing all items needed across the whole game.

    Keyword Arguments:
    upload              - Optional trigger to upload the page automatically to the wiki
    '''
    gde_data = read_gde()
    i2_data = read_i2()
    item_totals = {}
    output = []
    stringhash = string_hash(gde_data)
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Quest":
            items = gde_data[line].get(stringhash["NeedItem"])
            counts = gde_data[line].get(stringhash["NeedItemCount"])
            for item, count in zip(items, counts):
                if item.lower() != "lobbyeventpoint":
                    item_totals[item.lower()] = item_totals.get(item.lower(), 0) + count
    item_totals = collections.OrderedDict(sorted(item_totals.items()))
    output.append("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|-")
    for ids, count in item_totals.items():
        if ids == "eventcoin":
            output.append("\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
            output.append(f"|{count}\n|-")
        else:
            item_name, item_level = ids.split("_")
            output.append("\n|{{Item | "+i2_data.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
            output.append(f"|{count}\n|-")
    text_list = list("".join(output))
    text_list[-1] = "}"
    text = "".join(text_list)
    if upload is False:
        with open(output_file("game_items_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/Total_Game_Items", text)
    print("Action completed.")
