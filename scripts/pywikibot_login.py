from pywikibot import Site
import pywikibot

def login():
    site = Site(code = "en", fam="sunnyhouse")
    site.login()
    return site

def wiki_upload(pagename, text):
    site = login()
    page = pywikibot.Page(site, 'User:WFrck/'+pagename)
    page.text = text
    page.save("Created area pages (automated)")