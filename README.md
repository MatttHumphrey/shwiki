# shwiki
shwiki is a command-line utility written in Python to assist with maintenance of the [Sunny House Wiki](https://sunny-house.fandom.com/). Capabilities include creation of "Area", "Botanical Plant" and a collection of "Area/Game Item" pages, plus spreadsheet export functionality.

## Installation
```console
# clone the repo
$ git clone https://github.com/MatttHumphrey/shwiki

# change the working directory to shwiki
$ cd shwiki

# install the requirements
$ pip install -r requirements.txt
```

## Data
This tool requires two files to run. These are `gde_data.json` and `i2subset_english.json`, and they can be extracted from the game using [AssetRipper](https://github.com/AssetRipper/AssetRipper) or [AssetStudio](https://github.com/Perfare/AssetStudio).

## Usage
```console
$ python shwiki.py -h
usage: python shwiki.py subcommand arguments [options]

Sunny House wiki utility program. Used primarily to generate wiki pages ready for upload.

options:
  -h, --help            Shows this help message.

subcommands:
  {area_dialogue,area_items,area_list,botanical_plant,full_dialogue,game_items,hard_items,task_list,area_page,excel_task_list}
    area_dialogue       Outputs the dialogue spoken in a given location.
    area_items          Outputs a list of all items needed for a given location.
    area_list           Outputs a list of filenames for all locations in game.
    botanical_plant     Outputs an Endangered Plant wiki page.
    full_dialogue       Outputs the dialogue spoken across the whole game.
    game_items          Outputs a list of all items needed across the whole game.
    hard_items          Outputs a list of hard items needed for all areas in the game. Uses scripts/utils/hard_items.py to determine which items to include.
    task_list           Outputs a list of tasks for a given location, with tasks named after the loc_id provided.
    area_page           Outputs the dialogue, task list and area page for a given location.
    excel_task_list     Outputs a spreadsheet containing all tasks across the game.
```

## Pywikibot installation
Some of the subcommands can take an optional `-u` argument that allows the files to be directly uploaded to the wiki. By default these are uploaded to the "User" namespace, but this can be edited in the python scripts.

1. For pywikibot to run, the three files stored in the `pywikibot_setup` folder must be used. The `user_config.py` and `user-password.py` files can be filled in according to the instructions at Fandom's [Pywikibot Help](https://community.fandom.com/wiki/Help:Pywikibot), and placed in the main directory. 

2. The `sunnyhouse_family.py` file needs to be placed in `families` folder of the pywikibot installation.

See the [Pywikibot Docs](https://www.mediawiki.org/wiki/Manual:Pywikibot) for further information.