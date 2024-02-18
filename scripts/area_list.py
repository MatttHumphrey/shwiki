from .utils.read_data import read_gde, read_i2
from .utils.match_location import area_dict
from .utils.output_file import output_file

def area_list():
    '''Generates a list of all in file area names.'''
    gde_data = read_gde()
    i2_data = read_i2()
    area_lists = list(area_dict(gde_data, i2_data).keys())
    with open(output_file("area_output.txt"), "w", encoding="utf8") as output:
        output.writelines("\n".join(area_lists))
    print("Action completed.")