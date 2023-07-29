from utils.hard_items import HARD_ITEMS
from utils.output_file import output_file
from utils.read_i2 import read_i2
from utils.read_gde import read_gde
from utils.match_location import match_location
import collections
import sys


def get_arealist():
    area_list = []
    data = read_gde()
    for line in data:
        if data[line].get("1071") == "Quest":
            area_name = data[line].get("20")
            if area_name not in area_list:
                area_list.append(area_name)
    remove_list = ['',"WinterFair2022_Shack","WinterFair2022_IceRink","WinterFair2022_Sledding","WinterFair2022_FerrisWheel","WinterFair2022_Train"]
    area_list = [area for area in area_list if area not in remove_list]
    with open(output_file("area_output.txt"), "w", encoding="utf8") as output:
        output.writelines("\n".join(area_list))
    print("Action completed.")

def get_game_items():
    item_totals = {}
    descriptions = read_i2()
    data = read_gde()
    for line in data:
        if data[line].get("1071") == "Quest":
            items = data[line].get("23")
            counts = data[line].get("26")
            for item, count in zip(items, counts):
                if item.lower() != "lobbyeventpoint":
                    item_totals[item.lower()] = item_totals.get(item.lower(), 0) + count
    item_totals = collections.OrderedDict(sorted(item_totals.items()))
    with open(output("game_items_output.txt"), "w", encoding="utf8") as output:
        output.writelines("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|-\n")
        for id, count in item_totals.items():
            if id == "eventcoin":
                output.writelines("|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
                output.writelines(f"|{count}\n|-\n")
            else:
                item_name, item_level = id.split("_")
                output.writelines("|{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
                output.writelines(f"|{count}\n|-\n")
    print("Action completed.")

def get_area_items(area):
    descriptions = read_i2()
    data = read_gde()
    area_total = {}
    for line in data:
        if data[line].get("1071") == "Quest" and data[line].get("20").lower() == area:
            items = data[line].get("23")
            counts = data[line].get("26")
            for i in range(0,len(items)):
                if items[i].lower() != "lobbyeventpoint":
                    if items[i].lower() not in area_total.keys():
                        area_total[items[i].lower()] = 0
                    area_total[items[i].lower()] += counts[i]
    sorted_totals = collections.OrderedDict(sorted(area_total.items()))
    with open(output("area_items_output.txt"), "w", encoding="utf8") as output:
        output.writelines("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
        for id in sorted_totals.keys():
            if id == "eventcoin":
                output.writelines("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
                output.writelines(f"|{sorted_totals.get(id)}\n|")
            else:
                item_name, item_level = id.split("_")
                output.writelines("-\n|{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
                output.writelines(f"|{sorted_totals.get(id)}\n|")
        output.writelines("|}")
   
def get_hard_items(area):
    descriptions = read_i2()
    data = read_gde()
    area_total = {item: 0 for item in HARD_ITEMS}
    for line in data:
        if data[line].get("1071") == "Quest" and data[line].get("20").lower() == area:
            items = data[line].get("23")
            counts = data[line].get("26")
            for item, count in zip(items, counts):
                if item.lower() in HARD_ITEMS:
                    area_total[item.lower()] = area_total.get(item.lower(), 0) + count
    sorted_totals = collections.OrderedDict(sorted(area_total.items()))
    sorted_totals = {key: value for key, value in sorted_totals.items() if value != 0}
    with open(output("hard_items_output.txt"), "w", encoding="utf8") as output:
        output.writelines("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
        for id in sorted_totals.keys():
            if id == "eventcoin":
                output.writelines("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
            else:
                item_name, item_level = id.split("_")
                output.writelines("-\n|{{Item | "+descriptions.get("categoryname_"+item_name.lower())+" | "+item_level.lstrip("0")+"}}\n")
            output.writelines(f"|{sorted_totals.get(id)}\n|")
        output.writelines("}")
    print("Action completed.")

if __name__ == "__main__":
    if sys.argv[1] == "get_arealist":
        if len(sys.argv) != 2:
            print("Usage: python WikiItemListsGen.py get_arealist")
        else:
            get_arealist()

    elif sys.argv[1] == "get_game_items":
        if len(sys.argv) != 2:
            print("Usage: python WikiItemListsGen.py get_game_items")
        else:
            get_game_items()

    elif sys.argv[1] == "get_area_items":
        if len(sys.argv) != 3:
            print("Usage: python WikiItemListsGen.py get_area_items area")
        else:
            area = sys.argv[2]
            get_area_items(match_location(area))

    elif sys.argv[1] == "get_hard_items":
        if len(sys.argv) != 3:
            print("Usage: python WikiItemListsGen.py get_hard_items area")
        else:
            area = sys.argv[2]
            get_hard_items(match_location(area))
            
    else:
        print("Invalid function name. Available functions: get_arealist, get_area_items, get_game_items, get_hard_items")
