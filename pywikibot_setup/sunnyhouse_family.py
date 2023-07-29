"""
This family file was auto-generated by generate_family_file.py script.

Configuration parameters:
  url = https://sunny-house.fandom.com
  name = sunnyhouse

Please do not commit this to the Git repository!
"""
from pywikibot import family


class Family(family.Family):  # noqa: D101

    name = 'sunnyhouse'
    langs = {
        'en': 'sunny-house.fandom.com',
    }

    def scriptpath(self, code):
        return {
            'en': '',
        }[code]

    def protocol(self, code):
        return {
            'en': 'https',
        }[code]
