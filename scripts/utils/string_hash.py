VALUES = ["_gdeSchema", "AreaGroupKey", "Id", "CompleteOpenQuest", "CompleteDialogue",
              "OpenDialogue", "ItemCategory", "CompleteAreaKey", "Group", "DescriptionKey",
              "Actor", "NeedItem", "NeedItemCount", "StartDate", "EndDate",
              "BookDuringEventDescKey", "Key", "Name", "SaleGold", "UnlockJewel", "MergeSpawn1",
              "Desc", "Reward"]

def string_hash(gde_data):
    '''Creates a dictionary containing all the text keyname we use and the associated keynames in the game files.
    
    Keyword Arguments:
    gde_data            - The gde_data dictionary
    
    Return Value:
    A dictionary containing all gde_data keynames used in the program.'''
    my_dict = gde_data["StringHash"]
    key_list = list(my_dict.keys())
    val_list = list(my_dict.values())
    hash_dict = {item: key_list[val_list.index(item)] for item in VALUES}
    return hash_dict
