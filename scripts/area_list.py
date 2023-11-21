from .utils.match_location import area_dict
from .utils.output_file import output_file

def area_list():
    '''Generates a list of all in file area names.'''
    area_lists = list(area_dict().keys())
    with open(output_file("area_output.txt"), "w", encoding="utf8") as output:
        output.writelines("\n".join(area_lists))
    print("Action completed.")
