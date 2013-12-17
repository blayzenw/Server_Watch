from BeautifulSoup import BeautifulSoup
import urllib2
import winsound, sys
import time
import threading
import update

tollerence = 3
jumpTollerence = 3
servers = [['Desertion','http://freedom001.game.wurmonline.com:8080/mrtg/wurm.html'],['Serenity','http://freedom002.game.wurmonline.com:8080/mrtg/wurm.html'],['Affliction','http://freedom003.game.wurmonline.com:8080/mrtg/wurm.html'],['Elevation','http://wild001.game.wurmonline.com:8080/mrtg/wurm.html']]

v = [42, 58, 58, 32]
v2 = [52, 48, 58, 32]

def main():
    update.checkForUpdate()
    print '- Server Watch -'
    print 'Version 1.08'
    print
    print 'Commands:'
    print 'playerCounts() - Prints out how many people are on each server'
    print
    serverCheck = threading.Thread(target=checkServers)
    serverCheck.start()

def playerCounts():
    players = buildCountList()
    print 'Current time - ' + str(time.localtime()[3]) + ':' + str(time.localtime()[4])
    print servers[0][0] + ' - ' + str(players[0])
    print servers[1][0] + ' - ' + str(players[1])
    print servers[2][0] + ' - ' + str(players[2])
    print servers[3][0] + ' - ' + str(players[3])

def playerChanges(old, new):
    print servers[0][0] + ' -  ' + str(old[0]) + ' to ' + str(new[0])
    print servers[1][0] + ' -    ' + str(old[1]) + ' to ' + str(new[1])
    print servers[2][0] + ' - ' + str(old[2]) + ' to ' + str(new[2])
    print servers[3][0] + ' -  ' + str(old[3]) + ' to ' + str(new[3])
    

def playSound(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
    
def grabPlayers(url):
    #Grab page and parse it
    page = urllib2.urlopen(url)
    pageSource = page.read()
    soup = BeautifulSoup(pageSource)

    #The player count should be under <tr class="out">
    players = soup.findAll('td')[2]

    #Put it into a string so we can work with it
    playerStr = str(players)

    #Format the string so we only have the number of players
    playerStr = playerStr[4:len(playerStr)]
    count = 0
    while(playerStr[count] != ' '):
        count += 1
    playerStr = playerStr[0:count]
    #Convert it to an int
    playerInt = int(playerStr)
    return playerInt
    
def buildCountList():
    serverCount = []
    serverCount.append(grabPlayers(servers[0][1]))
    serverCount.append(grabPlayers(servers[1][1]))
    serverCount.append(grabPlayers(servers[2][1]))
    serverCount.append(grabPlayers(servers[3][1]))
    return serverCount

def checkServers():
    print '--Background server watch initiated--'
    lastServerCount = buildCountList()
    serverCount = lastServerCount
    while(True):
        time.sleep(30)
        lastServerCount = serverCount
        serverCount = buildCountList()

        dif = checkDif(serverCount,lastServerCount)
        alertChange(dif)
        

def checkDif(serverCountOld, serverCountNew):
    report = []
    serverChange = [0,0,0,0]
    count = 0
    while(count < 4):
        serverChange[count] = serverCountNew[count]-serverCountOld[count]
        count += 1
    print serverChange
    dts = (abs(serverChange[0]-serverChange[3]))/2
    sts = (abs(serverChange[1]-serverChange[3]))/2
    ats = (abs(serverChange[2]-serverChange[3]))/2
    
    if dts >= tollerence:
        if abs(serverChange[0]) >= jumpTollerence and abs(serverChange[3]) >= jumpTollerence:
            if serverChange[0]-serverChange[3] > 0:
                report.append([0,3,dts])
            else:
                report.append([3,0,dts])
        
    if dts >= tollerence:
        if abs(serverChange[1]) >= jumpTollerence and abs(serverChange[3]) >= jumpTollerence:
            if serverChange[0]-serverChange[3] > 0:
                report.append([1,3,dts])
            else:
                report.append([3,1,dts])
        
    if dts >= tollerence:
        if abs(serverChange[2]) >= jumpTollerence and abs(serverChange[3]) >= jumpTollerence:
            if serverChange[0]-serverChange[3] > 0:
                report.append([2,3,dts])
            else:
                report.append([3,2,dts])
        
    return report


def alertChange(reports):
    if(reports == []):
        return
    
    for report in reports:
        server1 = servers[report[0]][0]
        server2 = servers[report[1]][0]
        playerChange = report[2]

        print str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ' - ' + 'There was a change of ' + str(playerChange) + ' players from ' + str(server2) + ' to ' + str(server1)
        
        
    playSound('beep')

main()
