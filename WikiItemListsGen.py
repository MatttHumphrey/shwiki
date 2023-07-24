import json
import collections
import os.path as path
from convert import TOOL_CONVERT

gde_file = path.join(path.dirname(__file__),"gde_data.json")

def get_arealist():
    output_file = path.join(path.dirname(__file__),"area_output.txt")
    area_list = []
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest":
                if data[line].get("20") not in area_list:
                    area_list.append(data[line].get("20"))
    remove_list = ['',"WinterFair2022_Shack","WinterFair2022_IceRink","WinterFair2022_Sledding","WinterFair2022_FerrisWheel","WinterFair2022_Train"]
    with open(output_file, "w", encoding="utf8") as output:
        for elem in area_list:
            if elem not in remove_list:
                output.writelines(f"{elem}\n")

def get_game_items():
    item_totals = {}
    output_file = path.join(path.dirname(__file__),"game_items_output.txt")
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data:
            if data[line].get("1071") == "Quest":
                items = data[line].get("23")
                counts = data[line].get("26")
                for i in range(0,len(items)):
                    if items[i].lower() != "lobbyeventpoint":
                        if items[i].lower() not in item_totals.keys():
                            item_totals[items[i].lower()] = 0
                        item_totals[items[i].lower()] += counts[i]
    item_totals = collections.OrderedDict(sorted(item_totals.items()))
    with open(output_file, "w", encoding="utf8") as output:
        output.writelines("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|-\n")
        for id in item_totals.keys():
            if id == "eventcoin":
                output.writelines("|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
                output.writelines(f"|{item_totals.get(id)}\n|-\n")
            else:
                item_name, item_level = id.split("_")
                output.writelines("|{{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}\n")
                output.writelines(f"|{item_totals.get(id)}\n|-\n")

def get_area_items():
    output_file = path.join(path.dirname(__file__),"area_items_output.txt")
    area_file = path.join(path.dirname(__file__),"area_output.txt")
    with open(gde_file, "r", encoding="utf8") as file, open(area_file, "r", encoding="utf8") as areas, open(output_file, "w", encoding="utf8") as output:
        data = json.load(file)
        for place in areas:
            area_total = {}
            loc = place.strip()
            for line in data:
                if data[line].get("1071") == "Quest" and data[line].get("20") == place.strip():
                    items = data[line].get("23")
                    counts = data[line].get("26")
                    for i in range(0,len(items)):
                        if items[i].lower() != "lobbyeventpoint":
                            if items[i].lower() not in area_total.keys():
                                area_total[items[i].lower()] = 0
                            area_total[items[i].lower()] += counts[i]
            sorted_totals = collections.OrderedDict(sorted(area_total.items()))
            output.writelines("}\n\n== "+loc+" ==\n")
            output.writelines("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
            for id in sorted_totals.keys():
                if id == "eventcoin":
                    output.writelines("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
                    output.writelines(f"|{sorted_totals.get(id)}\n|")
                else:
                    item_name, item_level = id.split("_")
                    output.writelines("-\n|{{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}\n")
                    output.writelines(f"|{sorted_totals.get(id)}\n|")
   
def get_hard_items():
    output_file = path.join(path.dirname(__file__),"hard_items_output.txt")
    area_file = path.join(path.dirname(__file__),"area_output.txt")
    hard_items = ['bench_06', 'bench_07', 'bench_08', 'birds_01', 'birds_06', 'birds_07', 'birds_08', 'birds_09', 'birds_10', 'butterfly_04', 'butterfly_05', 'butterfly_06', 'cleaningtool_10', 'cleaningtool_12', 'cleansers_06', 'cleansers_07', 'eventcoin', 'gardentool_10', 'gardentool_11', 'gardentool_12', 'gardentool_13', 'gardentool_14', 'gardentool_15', 'lemonbag_01', 'lemonbag_02', 'lemonbag_03', 'lemonbag_04', 'lemonbag_06', 'lemonbag_07', 'screws_04', 'screws_05', 'sketchtool_10', 'sketchtool_11', 'sketchtool_12', 'sketchtool_13', 'sketchtool_14', 'sketchtool_15', 'statue_08', 'statue_09', 'statue_11', 'statue_12', 'statue_13', 'stonebasket_05', 'tools_09', 'tools_10', 'tools_11', 'tree_05', 'tree_06', 'tree_07', 'tree_08', 'vase_06', 'vase_07']
    with open(gde_file, "r", encoding="utf8") as file, open(area_file, "r", encoding="utf8") as areas, open(output_file, "w", encoding="utf8") as output:
        data = json.load(file)
        for place in areas:
            area_total = {}
            loc = place.strip()
            for line in data:
                if data[line].get("1071") == "Quest" and data[line].get("20") == place.strip():
                    items = data[line].get("23")
                    counts = data[line].get("26")
                    for i in range(0,len(items)):
                        if items[i].lower() != "lobbyeventpoint":
                            if items[i].lower() not in area_total.keys():
                                area_total[items[i].lower()] = 0
                            area_total[items[i].lower()] += counts[i]
            sorted_totals = collections.OrderedDict(sorted(area_total.items()))
            output.writelines("}\n\n== "+loc+" ==\n")
            output.writelines("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
            for id in sorted_totals.keys():
                if id.lower() in hard_items:
                    if id == "eventcoin":
                        output.writelines("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
                        output.writelines(f"|{sorted_totals.get(id)}\n|")
                    else:
                        item_name, item_level = id.split("_")
                        output.writelines("-\n|{{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}\n")
                        output.writelines(f"|{sorted_totals.get(id)}\n|")

def custom_hard_items(area):
    output_file = path.join(path.dirname(__file__),"custom_hard_items_output.txt")
    area_file = path.join(path.dirname(__file__),area)
    with open(gde_file, "r", encoding="utf8") as file, open(area_file, "r", encoding="utf8") as areas, open(output_file, "w", encoding="utf8") as output:
        data = json.load(file)
        area_total = {}
        for place in areas:
            for line in data:
                if data[line].get("1071") == "Quest" and data[line].get("20") == place.strip():
                    items = data[line].get("23")
                    counts = data[line].get("26")
                    for i in range(0,len(items)):
                        if items[i].lower() != "lobbyeventpoint":
                            if items[i].lower() not in area_total.keys():
                                area_total[items[i].lower()] = 0
                            area_total[items[i].lower()] += counts[i]
        sorted_totals = collections.OrderedDict(sorted(area_total.items()))
        output.writelines("{| class=\"article-table sortable\"\n!class=\"unsortable\"|Item\n!Count\n|")
        for id in sorted_totals.keys():
            if id == "eventcoin":
                output.writelines("-\n|[[File:LemonMoney.png|30px]] [[Lemon Event|Money]]\n")
                output.writelines(f"|{sorted_totals.get(id)}\n|")
            else:
                item_name, item_level = id.split("_")
                output.writelines("-\n|{{Item | "+TOOL_CONVERT[item_name.lower()]+" | "+item_level.lstrip("0")+"}}\n")
                output.writelines(f"|{sorted_totals.get(id)}\n|")
