from BeautifulSoup import BeautifulSoup
import urllib2
import winsound, sys
import time
import threading

tollerence = 3
servers = [['Desertion','http://freedom001.game.wurmonline.com:8080/mrtg/wurm.html'],['Serenity','http://freedom002.game.wurmonline.com:8080/mrtg/wurm.html'],['Affliction','http://freedom002.game.wurmonline.com:8080/mrtg/wurm.html'],['Elevation','http://wild001.game.wurmonline.com:8080/mrtg/wurm.html']]

v = [42, 58, 58, 32]
v2 = [52, 48, 58, 32]

def main():
    print '- Server Watch -'
    print 'Version 1.01'
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
    serverChange = [0,0,0]
    count = 0
    while(count < 3):
        serverChange[count] = serverCountNew[count]-serverCountOld[count]
        count += 1

    count = 0
    count2 = 0
    while(count < 3):
        while(count2 < 3):
            if abs(serverChange[count]) >= 3 and abs(serverChange[count2]) >= 3:
                if (abs(serverChange[count]-serverChange[count2])/2) >= tollerence:
                    report.append([serverChange.index(serverChange[count]), serverChange.index(serverChange[count2]), abs(serverChange[count]-serverChange[count2])/2])

            count2 += 1
        count += 1
        count2 = count

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
