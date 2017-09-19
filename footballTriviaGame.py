# Architecture taken from Kenny's pokeGame example

import urllib.request  # request library

import json  # json parsing

import random

# import pprint  # pretty print library, useful for printing jsons

BASE_API_ADDRESS = "http://api.football-data.org/v1/"

GET_ROUTE_COMP = "competitions/"

GET_ROUTE_TEAM = "teams/"


def getJSON(param, route):
    # urllib.request.Request makes a request object to prepare a get request
    requestParam = urllib.request.Request(BASE_API_ADDRESS + route + param)

    # print("URI for request:" + requestParam);
    # add our header hack
    # requestParam.add_header('User-Agent', HEADER_HACK)

    # gives a byte endoed string
    dataBytes = urllib.request.urlopen(requestParam).read()

    # we decode that in preparation for json parsing
    # techically  not necessary (since json has a way to decode) but we did this for debugging
    dataParam = str(dataBytes, 'utf-8')

    # turns a jsonString into a dictionary
    result = json.loads(dataParam)

    # print(str(result))

    return result


def getTeamJSON(teamName):
    teamSearchParam = "?name=" + teamName
    teamJ = getJSON(teamSearchParam, GET_ROUTE_TEAM)
    teamID = teamJ["teams"][0]["id"]
    return teamID


def getPlayerList(teamID):
    param = "%s/players" % teamID
    playerList = getJSON(param, GET_ROUTE_TEAM)["players"]
    playerNumberList = list()
    for playerDict in playerList:
        playerName, playerNumber = playerDict["name"], playerDict["jerseyNumber"]
        playerNumberList.append((playerName, playerNumber))
    playerNumberList.sort(key=lambda num: num[1])
    return playerNumberList


def main():

    active = True

    print("Hi! This is a game where you test your knowledge of players of different teams")

    teamName = (input(
        "name of Team you want to get quizzed on? (type quit or Ctrl_C to quit)\n")).lower()

    # did it just in case someone presses an arrow key and can't take it back

    teamName = teamName.strip()
    # teamName = teamName.replace(" ", "-")

    teamName = teamName.replace(" ", "%20")

    teamID = getTeamJSON(teamName)

    playerNumberList = getPlayerList(teamID)

    while (active):

        try:

            rand = random.randint(0, len(playerNumberList) - 1)

            randPlayer = playerNumberList[rand]

            guess = int(input("What is %s's jersey Number?" % randPlayer[0]))

            if (guess == randPlayer[1]):
                print("Nice you got it!")
            else:
                print("nope you were wrong!")

            playerNumberList.remove(randPlayer)
            if (len(playerNumberList) == 0):
                break
        except urllib.error.HTTPError:
            print("OOPS probably misspelled something, try again!")


main()
