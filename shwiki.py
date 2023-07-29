from scripts.area_dialogue import area_dialogue
from scripts.area_items import area_items
from scripts.area_list import area_list
from scripts.botanical_plant import botanical_plant
from scripts.full_dialogue import full_dialogue
from scripts.game_items import game_items
from scripts.hard_items import hard_items
from scripts.task_list import task_list

from scripts.utils.match_location import match_location
from scripts.utils.match_plant import match_plant

import argparse

functions = [
    (area_dialogue, [("location", str), ("upload", bool)], "Outputs the dialogue spoken in a given location."),
    (area_items, [("location", str), ("upload", bool)], "Outputs a list of all items needed for a given location."),
    (area_list, [], "Outputs a list of filenames for all locations in game."),
    (botanical_plant, [("name", str), ("filename", str), ("upload", bool)], "Outputs an Endangered Plant wiki page."),
    (full_dialogue, [], "Outputs the dialogue spoken across the whole game."),
    (game_items, [("upload", bool)], "Outputs a list of all items needed across the whole game."),
    (hard_items, [("location", str), ("upload", bool)], "Outputs a list of hard items needed for a given location. Uses scripts/utils/hard_items.py to determine which items to include."),
    (task_list, [("location", str), ("loc_id", str), ("upload", bool)], "Outputs a list of tasks for a given location, with tasks named after the loc_id provided."),
]

def create_parser():
    parser = argparse.ArgumentParser(description="Sunny House wiki utility program. Used primarily to generate wiki pages ready for upload.")
    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

    for func, args, help in functions:
        parser_func = subparsers.add_parser(func.__name__, help=help)
        parser_func.set_defaults(func=func)

        for arg, arg_type in args:
            if arg == "upload":
                parser_func.add_argument("-u", "--upload", action="store_true", help="Flag to upload page straight to wiki. Otherwise writes a text file to the output folder.")
            elif arg == "location":
                parser_func.add_argument(f"{arg}", type=arg_type, help=f"Location to run the function on. Accepts both in game and file names of areas.")
            elif arg == "loc_id":
                parser_func.add_argument(f"{arg}", type=arg_type, help=f"Key used to name tasks in task lists.")
            elif arg == "name":
                parser_func.add_argument(f"{arg}", type=arg_type, help=f"Endangered plant to run the function on. Accepts both in game and file names of plants.")
            elif arg == "filename":
                parser_func.add_argument(f"{arg}", type=arg_type, help=f"Wiki filename of endangered plant.")
            else:
                parser_func.add_argument(f"{arg}", type=arg_type, help=f"{func.__name__} help.")
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        return

    for func, argspec, help in functions:
        if args.subcommand == func.__name__:

            func_args = {}
            for arg, arg_type in argspec:
                value = getattr(args, arg)
                if arg == "location":
                    value = match_location(value)
                if arg == "name":
                    value = match_plant(value)
                func_args[arg] = value

            func(**func_args)
            return

    print(f"Invalid subcommand: {args.subcommand}. Use -h for help.")

if __name__ == "__main__":
    main()