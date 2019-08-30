# sample draw link: https://www.atptour.com/en/scores/current/us-open/560/draws

from bs4 import BeautifulSoup
from database import *
import os.path
import math

workspace_dir = os.path.dirname(os.path.realpath(__file__))

# inputFName: html input
# outputFName: db output
def html_to_db(inputFName, outputFName):
    soup = BeautifulSoup(open(inputFName), "html.parser")

    # parsing outputs
    seedDict = {} # key : player, value : seed
    countryDict = {}  # key : player, value : country_image
    numWinsDict = {} # key : player, value: numWins
    round1_players = []
    win_players = []

    for box in soup.find_all('div', {'class': 'scores-draw-entry-box'}):
        table_tags = box.find_all('table')
        if len(table_tags) > 0:  # round 1 entry
            tr_tags = box.find_all('tr')
            for tr_tag in tr_tags:
                span_tags = tr_tag.find_all('span')
                a_tags = tr_tag.find_all('a')
                if len(a_tags) > 0: # player info exists
                    playerName = a_tags[0]['data-ga-label']
                    img_tags = tr_tag.find_all('img')
                    if len(img_tags) > 0:
                        playerCountry = img_tags[0]['src']
                        countryDict[playerName] = playerCountry
                    round1_players.append(playerName)
                else:
                    playerName = "bye"
                    playerCountry = ""
                    countryDict[playerName] = playerCountry
                    round1_players.append(playerName)
                if len(span_tags) > 0:
                    seed = span_tags[0]
                    if seed:
                        seed_str = str(seed).strip()
                        seed_str = seed_str.replace('\n', '')
                        seed_str = seed_str.replace('\t', '')
                        seed_str = seed_str.replace('<', '')
                        seed_str = seed_str.replace('>', '')
                        seed_str = seed_str.replace('span', '')
                        seed_str = seed_str.replace('\\', '')
                        seed_str = seed_str.replace('/', '')
                        seed_str = seed_str.replace('(', '')
                        seed_str = seed_str.replace(')', '')
                        seedDict[playerName] = seed_str
        else:  # round 2, 3, ..., entry
            a_tags = box.find_all('a')
            if len(a_tags) > 0: # only true if match has happened
                playerName = a_tags[0]['data-ga-label']
                win_players.append(playerName)
            else:
                playerName = "unknown"
                win_players.append(playerName)

    drawSize = len(round1_players)
    assert(drawSize is 32 or drawSize is 64 or drawSize is 128)
    numRounds = int(math.log(drawSize)/math.log(2)) + 1
    rounds = [[] for i in range(numRounds)]

    # round1
    for i in range(0, drawSize, 2):
        rounds[0].append((round1_players[i], round1_players[i+1]))

    # (fill numWinsDict)
    for player in round1_players:
        numWinsDict[player] = win_players.count(player)

    # round2, ...
    num_players_last_round = drawSize
    for roundNum in range(1, numRounds, 1):
        num_players_this_round = int(num_players_last_round / 2)
        # fill round[roundNum]
        if num_players_this_round > 1:
            for i in range(0, num_players_this_round, 2):
                pair1 = rounds[roundNum-1][i] # from prev_round
                pair2 = rounds[roundNum-1][i+1] # from prev_round
                # determine winning player from pair 1
                player1 = pair1[0]
                player2 = pair1[1]
                num_wins1 = 0 if player1 not in numWinsDict else numWinsDict[player1]
                num_wins2 = 0 if player2 not in numWinsDict else numWinsDict[player2]
                winning_player1 = player1 if num_wins1 >= roundNum else player2 if num_wins2 >= roundNum else "unknown"
                # determine winning player from pair 2
                player1 = pair2[0]
                player2 = pair2[1]
                num_wins1 = 0 if player1 not in numWinsDict else numWinsDict[player1]
                num_wins2 = 0 if player2 not in numWinsDict else numWinsDict[player2]
                winning_player2 = player1 if num_wins1 >= roundNum else player2 if num_wins2 >= roundNum else "unknown"
                rounds[roundNum].append((winning_player1, winning_player2))
        else: # last round
            pair = rounds[roundNum-1][0]
            player1 = pair[0]
            player2 = pair[1]
            num_wins1 = 0 if player1 not in numWinsDict else numWinsDict[player1]
            num_wins2 = 0 if player2 not in numWinsDict else numWinsDict[player2]
            winning_player = player1 if num_wins1 >= roundNum else player2 if num_wins2 >= roundNum else "unknown"
            rounds[roundNum].append((winning_player))
        # endfill
        num_players_last_round = num_players_this_round

    db = TennisDatabase()

    drawRowList = []
    for roundNum in range(0, numRounds, 1):
        if roundNum != (numRounds - 1):
            for i in range(0, len(rounds[roundNum]), 1):
                drawRowList.append([roundNum+1, rounds[roundNum][i][0], rounds[roundNum][i][1]])
        else: # final round
            drawRowList.append([roundNum+1, rounds[roundNum][0], ""])
        
    playerRowList = []

    for player in round1_players:
        seed = 0 if player not in seedDict else seedDict[player]
        country = "" if player not in countryDict else countryDict[player]
        playerRowList.append([player, seed, country]) # country is similar to url, parsed later

    tennisData = TennisData(drawRowList, playerRowList)
    db.SaveToDb(outputFName, tennisData)

if __name__ == "__main__":
    #html_to_db(workspace_dir + "/html_data/us_open_draw.html", workspace_dir + "/data/usopen.db")
    html_to_db(workspace_dir + "/html_data/rogers_cup_draw.html", workspace_dir + "/data/rogers_cup_draw.db")