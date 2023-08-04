from .utils.pywikibot_login import wiki_upload
from .utils.convert_date import convert_date
from .utils.output_file import output_file
from .utils.read_gde import read_gde
from .utils.read_i2 import read_i2

def botanical_plant(plant_name, filename, upload):
    descriptions = read_i2()
    data = read_gde()
    output = []
    for line in data:
        if data[line].get("1071") == "PeriodicalEvent" and data[line].get("663").lower() == "plant_"+plant_name:
            start_date = convert_date(str(data[line].get("297")))
            end_date = convert_date(str(data[line].get("299")))
            desc = descriptions[data[line].get("679").lower()]
            plant_number = data[line].get("76").split("_")[1]
            desc_plant_name = descriptions["categoryname_plant_"+plant_name]
    for line in data:
        if data[line].get("1081") == "PeriodicalEvent" and data[line].get("76") == "Botanical_"+str(int(plant_number)-1):
            prev_plant = descriptions["categoryname_"+data[line].get("663").lower()]
    cost = {}
    item_name = {}
    bubble_gem = {}
    xp = {}
    xp["01"] = 0
    for line in data:
        item_key = str(data[line].get("158")).lower()
        if data[line].get("1081") == "Item" and plant_name in item_key and "seedbox" not in item_key:
            level = item_key.split("_")[2]
            cost[level] = data[line].get("211")
            item_name[level] = descriptions["itemname_"+item_key.lower()]
            bubble_gem[level] = data[line].get("223")
            xp[str(int(level)+1).zfill(2)] = 1 if data[line].get("216") == "Item_61" else 0
    output.append("{{InfoboxPlant\n|image = <gallery>\nPlant"+filename+"01.png | Level 1\nPlant"+filename+"12.png | Level 12\nPlant"+filename+"inBG.png | Planted\n</gallery>\n")
    output.append("|type=Drop Item<br>Event Item\n|description=\n"+desc+"\n")
    output.append("|source=[[File:"+filename+"SeedBox03.png|15x15px]][[Plant Seed Boxes#"+desc_plant_name+" Seed Box|Plant Seed Box]]<br>[[File:"+filename+"RareSeedBox01.png|15x15px]][[Plant Seed Boxes#"+desc_plant_name+" Seed Box|Rare Plant Seed Box]]")
    output.append("\n|reward=[[File:Jewel.png|15x15px]] 35 [[Jewels]]\n|prev=''[["+prev_plant+"]]''\n|next=???\n}}\n\n")
    output.append("'''"+desc_plant_name+"''' is one of the plants that can be earned from the [[File:SaveThePlantIcon.png|21x21px]] [[Flower Garden (Board)#Save the Plant|Save the Plant]] event. A level 12 plant can be placed in the [[Botanical Garden]]. It was available from "+start_date+" to "+end_date+".\n\n")
    output.append("It can be earned from [[File:"+filename+"SeedBox03.png|21x21px]][[Plant Seed Boxes#"+desc_plant_name+" Seed Box|Plant Seed Boxes]] and [[File:"+filename+"RareSeedBox01.png|21x21px]][[Plant Seed Boxes#"+desc_plant_name+" Seed Box|Rare Plant Seed Boxes]].\n\n")
    output.append("'''Note:''' Due to the game's constant updates, the information displayed on this page may not always be up to date. If you have any new information, feel free to edit accordingly.\n\n")
    output.append("==Story==\n<div class=\"mw-collapsible mw-collapsed\">\nClick '''Expand''' to view dialogue\n<div class=\"mw-collapsible-content\">\n{{/Dialogue}}\n</div>\n</div>\n\n")
    output.append("==Statistics==\n=== Merge Stages ===\n{| class=\"article-table\"\n|+\n"+desc_plant_name+"\n!Lvl\n!Image\n!Item\n!Sell Price\n!Drops*\n")
    for i in sorted(list(cost.keys())):
        output.append(f"|-\n|"+i.lstrip("0")+"\n|style=\"text-align:center;\" |[[File:Plant"+filename+str(i)+".png|65x65px]]\n|"+item_name[i]+"\n|[[File:Coin.png|16px|link=Coins]] "+str(cost[i])+"\n")
        output.append("| -\n" if xp[i] == 0 else f"|1 [[Experience Points (XP)|XP Star]]\n")
    output.append("|}\n<nowiki>*</nowiki>[[Experience Points (XP)|XP]] drops upon merge and does not repeat, item drops generate repeatedly unless parent item is destroyed or [[Coins|sold]].\n\n")
    output.append("===Double Bubbles===\n{| class=\"article-table\"\n|+\n"+desc_plant_name+": Double Bubbles**\n!Lvl\n!Image\n! Item\n![[Double Bubble]] Cost\n")
    for i in sorted(list(cost.keys())):
        if bubble_gem[i] != 0:
            output.append("|-\n|"+i.lstrip("0")+"\n|{{Bubble|Plant"+filename+str(i)+".png}}\n|"+item_name[i]+"\n|[[File:Jewel.png|16px|link=Jewels]] "+str(bubble_gem[i])+"\n")
    output.append("|}\n<nowiki>**</nowiki>[[Double Bubble|Double Bubbles]] only appear for Levels 2 or higher, as they are created by merging. If not popped, they vanish after 60 seconds.\n\n")
    output.append("{{PlantEventMenu}}\n[[Category:Endangered Plants]]\n[[Category:Drops]]\n[[Category:Common Drops]]\n[[Category:Event Items]]\n__NOTOC__")
    text = "".join(output)
    if upload == False:
        with open(output_file("plant_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/"+desc_plant_name, text)
    print("Action completed.")
