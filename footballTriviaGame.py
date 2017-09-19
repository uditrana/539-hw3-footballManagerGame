# Architecture taken from Kenny's pokeGame example

import urllib.request  # request library

import json  # json parsing

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
    teamJson = getJSON(teamSearchParam, GET_ROUTE_TEAM)
    teamID = teamJSON["ID"]


def main():

    active = True

    print("Hi! This is a game where you test your knowledge of players of different teams")

    while True:

        try:
            teamName = (input(
                "name of Team you want to get quizzed on? (type quit or Ctrl_C to quit)\n")).lower()

            # did it just in case someone presses an arrow key and can't take it back
            if (teamName.find("quit") != -1):
                break

            teamName = teamName.strip()
            # teamName = teamName.replace(" ", "-")

            teamName = teamName.replace(" ", "%20")

            teamJson = getTeamJSON(teamName)

            # userPokemon = input("what is the name of the pokemon you have?\n")

            # userPokemon = userPokemon.lower()

            # # did you know that no pokemon has the substring quit in their name?
            # if (userPokemon.find("quit") != -1):
            #     break

            # effectiveness = getTypeEffectiveness(teamName, userPokemon)

            # print(getEffectivenessMessage(effectiveness))

        except urllib.error.HTTPError:
            print("OOPS probably misspelled something, try again!")

    print("Shorts are confortable and easy to wear!!!")


main()
