from scripts.utils.match_location import match_location
from scripts.utils.output_file import output_file
from scripts.utils.hard_items import HARD_ITEMS
from scripts.utils.read_gde import read_gde
from scripts.utils.read_i2 import read_i2
import collections
import sys

def hard_items(area):
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
    with open(output_file("hard_items_output.txt"), "w", encoding="utf8") as output:
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
    if len(sys.argv) != 2:
        print("Usage: python area_items.py location")
        sys.exit(1)
    else:
        location = sys.argv[1].lower()
        location = match_location(location)
        hard_items(location)