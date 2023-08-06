import pywikibot

def login():
    site = pywikibot.Site(code = "en", fam="sunnyhouse")
    site.login()
    return site

def wiki_upload(pagename, text):
    site = login()
    page = pywikibot.Page(site, pagename)
    page.text = text
    page.save("Created/Updated pages (automated)")