from .utils.output_file import output_file
from .utils.area_dict import area_dict

def area_list():
    '''Generates a list of all in file area names.'''
    area_list = list(area_dict().keys())
    with open(output_file("area_output.txt"), "w", encoding="utf8") as output:
        output.writelines("\n".join(area_list))
    print("Action completed.")