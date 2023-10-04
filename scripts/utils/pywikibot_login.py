import pywikibot

def login():
    '''Uses pywikibot to log into the wiki.'''
    site = pywikibot.Site(code = "en", fam="sunnyhouse")
    site.login()
    return site

def wiki_upload(pagename, text):
    '''
    Uses pywikibot to upload a page to the wiki.
    
    Keyword Arguments:
    pagename            - The name of the page the text is being uploaded to on the wiki
    text                - The contents of the page to be uploaded
    '''
    site = login()
    page = pywikibot.Page(site, pagename)
    page.text = text
    page.save("Created/Updated pages (automated)")
