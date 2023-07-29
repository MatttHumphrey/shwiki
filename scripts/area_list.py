from utils.output_file import output_file
from utils.read_gde import read_gde

def area_list():
    area_list = []
    data = read_gde()
    for line in data:
        if data[line].get("1071") == "Quest":
            area_name = data[line].get("20")
            if area_name not in area_list:
                area_list.append(area_name)
    remove_list = ['',"WinterFair2022_Shack","WinterFair2022_IceRink","WinterFair2022_Sledding","WinterFair2022_FerrisWheel","WinterFair2022_Train"]
    area_list = [area for area in area_list if area not in remove_list]
    with open(output_file("area_output.txt"), "w", encoding="utf8") as output:
        output.writelines("\n".join(area_list))
    print("Action completed.")

if __name__ == "__main__":
    area_list()