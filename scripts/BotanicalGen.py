import json
import sys
from modules import *

def main(name,filename):
    OUTPUT_FILE = get_output_file("plant_output.txt")
    descriptions = read_i2()
    with open(GDE_FILE, "r", encoding="utf8") as file:
        data = json.load(file)
    with open(OUTPUT_FILE, "w+", encoding="utf8") as output:
        for line in data:
            if data[line].get("1071") == "PeriodicalEvent" and data[line].get("663").lower() == "plant_"+name:
                start_date = convert_date_format(str(data[line].get("297")))
                end_date = convert_date_format(str(data[line].get("299")))
                desc = descriptions[data[line].get("679").lower()]
                plant_number = data[line].get("76").split("_")[1]
                plant_name = descriptions["categoryname_plant_"+name]
        for line in data:
            if data[line].get("1071") == "PeriodicalEvent" and data[line].get("76") == "Botanical_"+str(int(plant_number)-1):
                prev_plant = descriptions["categoryname_"+data[line].get("663").lower()]
        cost = {}
        item_name = {}
        bubble_gem = {}
        xp = {}
        xp["01"] = 0
        for line in data:
            item_key = str(data[line].get("158")).lower()
            if data[line].get("1071") == "Item" and name in item_key and "seedbox" not in item_key:
                level = item_key.split("_")[2]
                cost[level] = data[line].get("211")
                item_name[level] = descriptions["itemname_"+item_key.lower()]
                bubble_gem[level] = data[line].get("223")
                xp[str(int(level)+1).zfill(2)] = 1 if data[line].get("216") == "Item_61" else 0
        output.writelines(
            "{{InfoboxPlant\n|image = <gallery>\nPlant"+filename+"01.png | Level 1\nPlant"+filename+"12.png | Level 12\nPlant"+filename+"inBG.png | Planted\n</gallery>\n"
            "|type=Drop Item<br>Event Item\n|description=\n"+desc+"\n"
            "|source=[[File:"+filename+"SeedBox03.png|15x15px]][[Plant Seed Boxes#"+plant_name+" Seed Box|Plant Seed Box]]<br>[[File:"+filename+"RareSeedBox01.png|15x15px]][[Plant Seed Boxes#"+plant_name+" Seed Box|Rare Plant Seed Box]]"
            "\n|reward=[[File:Jewel.png|15x15px]] 35 [[Jewels]]\n|prev=''[["+prev_plant+"]]''\n|next=???\n}}\n\n"
            "'''"+plant_name+"''' is one of the plants that can be earned from the [[File:SaveThePlantIcon.png|21x21px]] [[Flower Garden (Board)#Save the Plant|Save the Plant]] event. A level 12 plant can be placed in the [[Botanical Garden]]. It was available from "+start_date+" to "+end_date+".\n\n"
            "It can be earned from [[File:"+filename+"SeedBox03.png|21x21px]][[Plant Seed Boxes#"+plant_name+" Seed Box|Plant Seed Boxes]] and [[File:"+filename+"RareSeedBox01.png|21x21px]][[Plant Seed Boxes#"+plant_name+" Seed Box|Rare Plant Seed Boxes]].\n\n"
            "'''Note:''' Due to the game's constant updates, the information displayed on this page may not always be up to date. If you have any new information, feel free to edit accordingly.\n\n"
            "==Story==\n<div class=\"mw-collapsible mw-collapsed\">\nClick '''Expand''' to view dialogue\n<div class=\"mw-collapsible-content\">\n{{/Dialogue}}\n</div>\n</div>\n\n"
            "==Statistics==\n=== Merge Stages ===\n{| class=\"article-table\"\n|+\n"+plant_name+"\n!Lvl\n!Image\n!Item\n!Sell Price\n!Drops*\n")
        for i in sorted(list(cost.keys())):
            output.writelines(f"|-\n|"+i.lstrip("0")+"\n|style=\"text-align:center;\" |[[File:Plant"+filename+str(i)+".png|65x65px]]\n|"+item_name[i]+"\n|[[File:Coin.png|16px|link=Coins]] "+str(cost[i])+"\n")
            output.writelines("| -\n" if xp[i] == 0 else f"|1 [[Experience Points (XP)|XP Star]]\n")
        output.writelines("|}\n<nowiki>*</nowiki>[[Experience Points (XP)|XP]] drops upon merge and does not repeat, item drops generate repeatedly unless parent item is destroyed or [[Coins|sold]].\n\n"
            "===Double Bubbles===\n{| class=\"article-table\"\n|+\n"+plant_name+": Double Bubbles**\n!Lvl\n!Image\n! Item\n![[Double Bubble]] Cost\n")
        for i in sorted(list(cost.keys())):
            if bubble_gem[i] != 0:
                output.writelines("|-\n|"+i.lstrip("0")+"\n|{{Bubble|Plant"+filename+str(i)+".png}}\n|"+item_name[i]+"\n|[[File:Jewel.png|16px|link=Jewels]] "+str(bubble_gem[i])+"\n")
        output.writelines("|}\n<nowiki>**</nowiki>[[Double Bubble|Double Bubbles]] only appear for Levels 2 or higher, as they are created by merging. If not popped, they vanish after 60 seconds.\n\n"
            "{{PlantEventMenu}}\n[[Category:Endangered Plants]]\n[[Category:Drops]]\n[[Category:Common Drops]]\n[[Category:Event Items]]\n__NOTOC__")
    print("Action completed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python WikiBotanicalGen.py gde_name image_name")
    else:
        gde_name, image_name = sys.argv[1].lower(), sys.argv[2]
        gde_name = match_plant(gde_name)
        main(gde_name, image_name)
