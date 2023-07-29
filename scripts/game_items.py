from scripts.utils.output_file import output_file
from scripts.utils.read_gde import read_gde
from scripts.utils.read_i2 import read_i2
import collections

def game_items():
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
    with open(output_file("game_items_output.txt"), "w", encoding="utf8") as output:
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

if __name__ == "__main__":
    game_items()