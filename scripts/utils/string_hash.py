from .read_gde import read_gde

def string_hash():
    '''Creates a dictionary containing all the text keyname we use and the associated keynames in the game files.'''
    data = read_gde()
    my_dict = data["StringHash"]
    key_list = list(my_dict.keys())
    val_list = list(my_dict.values())
    values = ["_gdeSchema", "AreaGroupKey", "Id", "CompleteOpenQuest", "CompleteDialogue", "OpenDialogue",
              "ItemCategory", "CompleteAreaKey", "Group", "DescriptionKey", "Actor", "NeedItem", "NeedItemCount", 
              "StartDate", "EndDate", "BookDuringEventDescKey", "Key", "Name", "SaleGold", "UnlockJewel", "MergeSpawn1",
              "Desc", "Reward"]
    hash_dict = {item: key_list[val_list.index(item)] for item in values}
    return hash_dict