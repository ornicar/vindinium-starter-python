#!/usr/bin/env python

import os
import sys
import requests
import re
from bot import RandomBot

def get_new_game_state(serverHost, key, numberOfTurns = '20', mode='training'):
    if(mode=='training'):
        params = { 'key': key, 'turns': numberOfTurns}
        r = requests.post(serverHost + '/api/training', params)

        if(r.status_code == 200):
            return r.json()
        else:
            print("Error when creating the game")
            print(r.text)
    else:
        pass

def move(url, direction):
    r = requests.post(url, {'dir': direction})
    return r.json()

def start(serverHost, key, bot, numberOfGames = 20):

    def play(state, gamesPlayed = 0):
        if (state['game']['finished']):
            gamesPlayed += 1
            print('Game finished: %d/%d' % (gamesPlayed, numberOfGames))

            if(gamesPlayed < numberOfGames):
                print('asking a new game')
                state = get_new_game_state(serverHost, key)
                play(state, gamesPlayed)
        else:
            url = state['playUrl']
            direction = bot.move(state)
            newState = move(url, direction)

            print("Playing turn %d with direction %s" % (state['game']['turn'], direction))
            play(newState, gamesPlayed)

    state = get_new_game_state(serverHost, key)
    print("Start: " + state['viewUrl'])
    play(state)

if __name__ == "__main__":
    if (len(sys.argv) > 3):
        start(sys.argv[1], sys.argv[2], RandomBot(), int(sys.argv[3]))
    else:
        print("Usage: %s <server> <key> <number-of-games-to-play>" % (sys.argv[0]))
        print('Example: %s http://localhost:9000 mySecretKey 20' % (sys.argv[0]))
