from datetime import datetime
import json
import pywikibot
import os.path as path

i2_file = path.join(path.dirname(__file__),"i2subset_english.json")
gde_file = path.join(path.dirname(__file__),"gde_data.json")
output_file = path.join(path.dirname(__file__),"plant_output.txt")

def wiki_upload(pagename, text):
    site = pywikibot.Site('en', 'sunny-house')
    page = pywikibot.Page(site, 'User:WFrck/'+pagename)
    page.text = text
    page.save("Created area pages (automated)")

def read_i2():
    descriptions = {}
    with open(i2_file, "r", encoding="utf8") as file:
        data = json.load(file)
        for line in data["mSource"]["mTerms"]:
            descriptions[line.get("Term").lower()] = line.get("Languages")[0]
    return descriptions

def convert_date_format(input_date):
    date_object = datetime.strptime(input_date, '%Y%m%d')
    formatted_date = date_object.strftime('%B %d, %Y')
    day = int(date_object.strftime('%d'))
    suffix = 'th' if 11 <= int(day) <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(int(day) % 10, 'th')
    return date_object.strftime('%B %d{}, %Y').format(suffix)

def main(name,filename):
    output = []
    descriptions = read_i2()
    with open(gde_file, "r", encoding="utf8") as file:
        data = json.load(file)
    for line in data:
        if data[line].get("1071") == "PeriodicalEvent" and data[line].get("663") == "Plant_"+name:
            start_date = convert_date_format(str(data[line].get("297")))
            end_date = convert_date_format(str(data[line].get("299")))
            desc = descriptions[data[line].get("679").lower()]
            plant_number = data[line].get("76").split("_")[1]
            plant_name = descriptions["categoryname_plant_"+name.lower()]
    for line in data:
        if data[line].get("1071") == "PeriodicalEvent" and data[line].get("76") == "Botanical_"+str(int(plant_number)-1):
            prev_plant = descriptions["categoryname_"+data[line].get("663").lower()]
    cost = {}
    item_name = {}
    bubble_gem = {}
    for line in data:
        item_key = data[line].get("158")
        if data[line].get("1071") == "Item" and name in item_key and "SeedBox" not in item_key:
            level = item_key.split("_")[2]
            cost[level] = data[line].get("211")
            item_name[level] = descriptions["itemname_"+item_key.lower()]
            bubble_gem[level] = data[line].get("223")
    output.append("{{InfoboxPlant\n|image = <gallery>\nPlant"+filename+"01.png | Level 1\nPlant"+filename+"12.png | Level 12\nPlant"+filename+"inBG.png | Planted\n</gallery>\n")
    output.append("|type=Drop Item<br>Event Item\n|description=\n"+desc+"\n")
    output.append("|source=[[File:"+filename+"SeedBox03.png|15x15px]][[Plant Seed Boxes#"+plant_name+" Seed Box|Plant Seed Box]]<br>[[File:"+filename+"RareSeedBox01.png|15x15px]][[Plant Seed Boxes#"+plant_name+" Seed Box|Rare Plant Seed Box]]")
    output.append("\n|reward=[[File:Jewel.png|15x15px]] 35 [[Jewels]]\n|prev=''[["+prev_plant+"]]''\n|next=???\n}}\n\n")
    output.append("'''"+plant_name+"''' is one of the plants that can be earned from the [[File:SaveThePlantIcon.png|21x21px]] [[Flower Garden (Board)#Save the Plant|Save the Plant]] event. A level 12 plant can be placed in the [[Botanical Garden]]. It was available from "+start_date+" to "+end_date+".\n\n")
    output.append("It can be earned from [[File:"+filename+"SeedBox03.png|21x21px]][[Plant Seed Boxes#"+plant_name+" Seed Box|Plant Seed Boxes]] and [[File:"+filename+"RareSeedBox01.png|21x21px]][[Plant Seed Boxes#"+plant_name+" Seed Box|Rare Plant Seed Boxes]].\n\n")
    output.append("'''Note:''' Due to the game's constant updates, the information displayed on this page may not always be up to date. If you have any new information, feel free to edit accordingly.\n\n")
    output.append("==Story==\n<div class=\"mw-collapsible mw-collapsed\">\nClick '''Expand''' to view dialogue\n<div class=\"mw-collapsible-content\">\n{{/Dialogue}}\n</div>\n</div>\n\n")
    output.append("==Statistics==\n=== Merge Stages ===\n{| class=\"article-table\"\n|+\n"+plant_name+"\n!Lvl\n!Image\n!Item\n!Sell Price\n!Drops*\n")
    for i in sorted(list(cost.keys())):
        output.append("|-\n|"+i.lstrip("0")+"\n|style=\"text-align:center;\" |[[File:Plant"+filename+str(i)+".png|65x65px]]\n|"+item_name[i]+"\n|[[File:Coin.png|16px|link=Coins]] "+str(cost[i])+"\n")
        if i in ["01","02","03"]:
            output.append("| -\n")
        else:
            output.append("|1 [[Experience Points (XP)|XP Star]]\n")
    output.append("|}\n<nowiki>*</nowiki>[[Experience Points (XP)|XP]] drops upon merge and does not repeat, item drops generate repeatedly unless parent item is destroyed or [[Coins|sold]].\n\n")
    output.append("===Double Bubbles===\n{| class=\"article-table\"\n|+\n"+plant_name+": Double Bubbles**\n!Lvl\n!Image\n! Item\n![[Double Bubble]] Cost\n")
    for i in sorted(list(cost.keys())):
        if bubble_gem[i] != 0:
            output.append("|-\n|"+i.lstrip("0")+"\n|{{Bubble|Plant"+filename+str(i)+".png}}\n|"+item_name[i]+"\n|[[File:Jewel.png|16px|link=Jewels]] "+str(bubble_gem[i])+"\n")
    output.append("|}\n<nowiki>**</nowiki>[[Double Bubble|Double Bubbles]] only appear for Levels 2 or higher, as they are created by merging. If not popped, they vanish after 60 seconds.\n\n")
    output.append("{{PlantEventMenu}}\n[[Category:Endangered Plants]]\n[[Category:Drops]]\n[[Category:Common Drops]]\n[[Category:Event Items]]\n__NOTOC__")
    text = "".join(output)
    wiki_upload(plant_name,text)