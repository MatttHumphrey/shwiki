from .utils.pywikibot_login import wiki_upload
from .utils.read_data import read_gde, read_i2
from .utils.convert_date import convert_date
from .utils.output_file import output_file
from .utils.string_hash import string_hash

def botanical_plant(plant_name, plant_filename, upload = False):
    '''
    Generates a formatted botanical plant page.
    Note: Minor edits may need to be made to the description in the Infobox.

    Keyword Arguments:
    plant_name          - The name of the plant we are generating the page for
    plant_filename      - The name of the images of the plant uploaded to the wiki (ie "Lotus" for "PlantLotus12.png")
    upload              - Optional trigger to upload the page automatically to the wiki
    '''
    gde_data = read_gde()
    i2_data = read_i2()
    stringhash = string_hash(gde_data)
    output = []
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "PeriodicalEvent" and gde_data[line].get(stringhash["ItemCategory"]).lower() == "plant_"+plant_name:
            start_date = convert_date(str(gde_data[line].get(stringhash["StartDate"])))
            end_date = convert_date(str(gde_data[line].get(stringhash["EndDate"])))
            desc = i2_data[gde_data[line].get(stringhash["BookDuringEventDescKey"]).lower()]
            plant_number = gde_data[line].get(stringhash["Key"]).split("_")[1]
            desc_plant_name = i2_data["categoryname_plant_"+plant_name]
    for line in gde_data:
        if gde_data[line].get(stringhash["_gdeSchema"]) == "PeriodicalEvent" and gde_data[line].get(stringhash["Key"]) == "Botanical_"+str(int(plant_number)-1):
            prev_plant = i2_data["categoryname_"+gde_data[line].get(stringhash["ItemCategory"]).lower()]
    cost = {}
    item_name = {}
    bubble_gem = {}
    xp_indicator = {"01": 0}
    for line in gde_data:
        item_key = str(gde_data[line].get(stringhash["Name"])).lower()
        if gde_data[line].get(stringhash["_gdeSchema"]) == "Item" and plant_name in item_key and "seedbox" not in item_key:
            level = item_key.split("_")[2]
            cost[level] = gde_data[line].get(stringhash["SaleGold"])
            item_name[level] = i2_data["itemname_"+item_key.lower()]
            bubble_gem[level] = gde_data[line].get(stringhash["UnlockJewel"])
            xp_indicator[str(int(level)+1).zfill(2)] = 1 if gde_data[line].get(stringhash["MergeSpawn1"]) == "Item_61" else 0
    output.append("{{InfoboxPlant\n|image = <gallery>\nPlant"+plant_filename+"01.png | Level 1\nPlant"+plant_filename+"12.png | Level 12\nPlant"+plant_filename+"inBG.png | Planted\n</gallery>\n")
    output.append("|type=Drop Item<br>Event Item\n|description=\n"+desc+"\n")
    output.append("|source=[[File:"+plant_filename+"SeedBox03.png|15x15px]][[Plant Seed Boxes#"+desc_plant_name+" Seed Box|Plant Seed Box]]<br>[[File:"+plant_filename+"RareSeedBox01.png|15x15px]][[Plant Seed Boxes#"+desc_plant_name+" Seed Box|Rare Plant Seed Box]]")
    output.append("\n|reward=[[File:Jewel.png|15x15px]] 35 [[Jewels]]\n|prev=''[["+prev_plant+"]]''\n|next=???\n}}\n\n")
    output.append("'''"+desc_plant_name+"''' is one of the plants that can be earned from the [[File:SaveThePlantIcon.png|21x21px]] [[Flower Garden (Board)#Save the Plant|Save the Plant]] event. A level 12 plant can be placed in the [[Botanical Garden]]. It was available from "+start_date+" to "+end_date+".\n\n")
    output.append("It can be earned from [[File:"+plant_filename+"SeedBox03.png|21x21px]][[Plant Seed Boxes#"+desc_plant_name+" Seed Box|Plant Seed Boxes]] and [[File:"+plant_filename+"RareSeedBox01.png|21x21px]][[Plant Seed Boxes#"+desc_plant_name+" Seed Box|Rare Plant Seed Boxes]].\n\n")
    output.append("'''Note:''' Due to the game's constant updates, the information displayed on this page may not always be up to date. If you have any new information, feel free to edit accordingly.\n\n")
    output.append("==Story==\n<div class=\"mw-collapsible mw-collapsed\">\nClick '''Expand''' to view dialogue\n<div class=\"mw-collapsible-content\">\n{{/Dialogue}}\n</div>\n</div>\n\n")
    output.append("==Statistics==\n=== Merge Stages ===\n{| class=\"article-table\"\n|+\n"+desc_plant_name+"\n!Lvl\n!Image\n!Item\n!Sell Price\n!Drops*\n")
    for i in sorted(list(cost.keys())):
        output.append("|-\n|"+i.lstrip("0")+"\n|style=\"text-align:center;\" |[[File:Plant"+plant_filename+str(i)+".png|65x65px]]\n|"+item_name[i]+"\n|[[File:Coin.png|16px|link=Coins]] "+str(cost[i])+"\n")
        output.append("| -\n" if xp_indicator[i] == 0 else "|1 [[Experience Points (XP)|XP Star]]\n")
    output.append("|}\n<nowiki>*</nowiki>[[Experience Points (XP)|XP]] drops upon merge and does not repeat, item drops generate repeatedly unless parent item is destroyed or [[Coins|sold]].\n\n")
    output.append("===Double Bubbles===\n{| class=\"article-table\"\n|+\n"+desc_plant_name+": Double Bubbles**\n!Lvl\n!Image\n! Item\n![[Double Bubble]] Cost\n")
    for i in sorted(list(cost.keys())):
        if bubble_gem[i] != 0:
            output.append("|-\n|"+i.lstrip("0")+"\n|{{Bubble|Plant"+plant_filename+str(i)+".png}}\n|"+item_name[i]+"\n|[[File:Jewel.png|16px|link=Jewels]] "+str(bubble_gem[i])+"\n")
    output.append("|}\n<nowiki>**</nowiki>[[Double Bubble|Double Bubbles]] only appear for Levels 2 or higher, as they are created by merging. If not popped, they vanish after 60 seconds.\n\n")
    output.append("{{PlantEventMenu}}\n[[Category:Endangered Plants]]\n[[Category:Drops]]\n[[Category:Common Drops]]\n[[Category:Event Items]]\n__NOTOC__")
    text = "".join(output)
    if upload is False:
        with open(output_file("plant_output.txt"), "w", encoding="utf8") as output:
            output.writelines(text)
    else:
        wiki_upload("User:WFrck/"+desc_plant_name, text)
    print("Action completed.")
