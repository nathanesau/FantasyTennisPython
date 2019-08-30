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
    seedDict = {}  # key : player, value : seed
    countryDict = {}  # key : player, value : country_image
    numWinsDict = {}  # key : player, value: numWins
    round1_players = []
    win_players = []

    for box in soup.find_all('div', {'class': 'scores-draw-entry-box'}):
        table_tags = box.find_all('table')
        if len(table_tags) > 0:  # round 1 entry
            tr_tags = box.find_all('tr')
            for tr_tag in tr_tags:
                span_tags = tr_tag.find_all('span')
                a_tags = tr_tag.find_all('a')
                if len(a_tags) > 0:  # player info exists
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
                        for substr in ['\n', '\t', '<', '>', 'span', '\\', '/', '(', ')']:
                            seed_str = seed_str.replace(substr, '')
                        seedDict[playerName] = seed_str
        else:  # round 2, 3, ..., entry
            a_tags = box.find_all('a')
            if len(a_tags) > 0:  # only true if match has happened
                playerName = a_tags[0]['data-ga-label']
                win_players.append(playerName)
            else:
                playerName = "unknown"
                win_players.append(playerName)

    drawSize = len(round1_players)
    assert(drawSize is 32 or drawSize is 64 or drawSize is 128)
    numRounds = int(math.log(drawSize)/math.log(2)) + 1
    rounds = [[] for i in range(numRounds)]

    for i in range(0, drawSize, 2):  # round1
        rounds[0].append((round1_players[i], round1_players[i+1]))

    for player in round1_players:  # numWinsDict
        numWinsDict[player] = win_players.count(player)

    def get_winner(pair, roundNum, numWinsDict):
        player1 = pair[0]
        player2 = pair[1]
        num_wins1 = 0 if player1 not in numWinsDict else numWinsDict[player1]
        num_wins2 = 0 if player2 not in numWinsDict else numWinsDict[player2]
        return player1 if num_wins1 >= roundNum else player2 if num_wins2 >= roundNum else "unknown"

    num_players_this_round = drawSize
    for roundNum in range(1, numRounds, 1):  # round2, ...
        num_players_this_round = int(num_players_this_round / 2)
        if num_players_this_round > 1:
            for i in range(0, num_players_this_round, 2):
                w1 = get_winner(rounds[roundNum-1][i], roundNum, numWinsDict)
                w2 = get_winner(rounds[roundNum-1][i+1], roundNum, numWinsDict)
                rounds[roundNum].append((w1, w2))
        else:  # last round
            w = get_winner(rounds[roundNum-1][0], roundNum, numWinsDict)
            rounds[roundNum].append((w))

    db = TennisDatabase()

    drawRowList = []
    for roundNum in range(0, numRounds, 1):  # drawRowList
        if roundNum != (numRounds - 1):
            for i in range(0, len(rounds[roundNum]), 1):
                p1 = rounds[roundNum][i][0]
                p2 = rounds[roundNum][i][1]
                drawRowList.append([roundNum+1, p1, p2])
        else:  # final round
            p = rounds[roundNum][0]
            drawRowList.append([roundNum+1, p, ""])

    playerRowList = []
    for player in round1_players:
        seed = 0 if player not in seedDict else seedDict[player]
        country = "" if player not in countryDict else countryDict[player]
        playerRowList.append([player, seed, country])  # country parsed later

    tennisData = TennisData(drawRowList, playerRowList)
    db.SaveToDb(outputFName, tennisData)
