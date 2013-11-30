import urllib2

versionURL = 

def getCurrentVersion():
    page = urllib2.urlopen(versionURL)
    pageSource = page.read()
    
