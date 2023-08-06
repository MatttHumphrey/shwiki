from .read_gde import read_gde

def string_hash():
    lmao = read_gde()
    my_dict = lmao["StringHash"]
    key_list = list(my_dict.keys())
    val_list = list(my_dict.values())

    hash_list = []
    hash_list.append(key_list[val_list.index("_gdeSchema")]) #1081
    hash_list.append(key_list[val_list.index("AreaGroupKey")]) #20
    hash_list.append(key_list[val_list.index("Id")]) #2
    hash_list.append(key_list[val_list.index("CompleteOpenQuest")]) #5
    hash_list.append(key_list[val_list.index("CompleteDialogue")]) #36
    hash_list.append(key_list[val_list.index("OpenDialogue")]) #38
    hash_list.append(key_list[val_list.index("ItemCategory")]) #663
    hash_list.append(key_list[val_list.index("CompleteAreaKey")]) #18
    hash_list.append(key_list[val_list.index("Group")]) #78
    hash_list.append(key_list[val_list.index("DescriptionKey")]) #88
    hash_list.append(key_list[val_list.index("Actor")]) #94
    hash_list.append(key_list[val_list.index("NeedItem")]) #23
    hash_list.append(key_list[val_list.index("NeedItemCount")]) #26
    hash_list.append(key_list[val_list.index("StartDate")]) #297
    hash_list.append(key_list[val_list.index("EndDate")]) #299
    hash_list.append(key_list[val_list.index("BookDuringEventDescKey")]) #679
    hash_list.append(key_list[val_list.index("Key")]) #76
    hash_list.append(key_list[val_list.index("Name")]) #158
    hash_list.append(key_list[val_list.index("SaleGold")]) #211
    hash_list.append(key_list[val_list.index("UnlockJewel")]) #213
    hash_list.append(key_list[val_list.index("MergeSpawn1")]) #216
    hash_list.append(key_list[val_list.index("Desc")]) #34   
    hash_list.append(key_list[val_list.index("Reward")]) #16
    return hash_list