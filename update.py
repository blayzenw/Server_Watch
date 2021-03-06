import urllib2
import zipfile

versionURL = 'https://raw.github.com/blayzenw/Server_Watch/master/server%20watch.info'
paylaodURL = 'https://github.com/blayzenw/Server_Watch/raw/master/Server%20Watch.zip'

def checkForUpdate():
    page = urllib2.urlopen(versionURL)
    pageSource = page.read()
    newVersion = parseVersion(pageSource)

    versionFile = open('server watch.info')
    cv = versionFile.read()
    currentVersion = parseVersion(cv)

    if(newVersion != currentVersion):
        print 'Updating...'
        downloadNewVersion()
        extractPayload()
        return True
    return False

def parseVersion(text):
    return float(text.split('=')[1])

def downloadNewVersion():
    page = urllib2.urlopen(paylaodURL)
    sw = open('Server Watch.zip', 'wb')
    sw.write(page.read())
    sw.close()

def extractPayload():
    swZip = open('Server Watch.zip', 'rb')
    z = zipfile.ZipFile(swZip)
    z.extractall()
    swZip.close()
    
