import urllib2

versionURL = https://raw.github.com/blayzenw/Server_Watch/master/server%20watch.info

def getCurrentVersion():
    page = urllib2.urlopen(versionURL)
    pageSource = page.read()
    newVersion = parseVersion(pageSource)

    versionFile = open('server watch.info')
    cv = versionFile.read()
    currentVersion = parseVersion(cv)

    if(newVersion != currentVersion)

def parseVersion(text):
    return int(text.split('=')[1])
