#!/usr/bin/env python

import os
import sys
import requests
import re
from bot import RandomBot

def get_new_game_state(serverHost, mode='training'):
    if(mode=='training'):
        return requests.post(serverHost + '/api/training/alone').json()
    else:
        pass

def move(url, direction):
    r = requests.post(url, {'dir': direction})
    return r.json()

def start(serverHost, bot, numberOfGames = 20):

    def play(state, gamesPlayed = 0):
        if (state['game']['finished']):
            gamesPlayed += 1
            print('Game finished: %d/%d' % (gamesPlayed, numberOfGames))

            if(gamesPlayed < numberOfGames):
                print('asking a new game')
                state = get_new_game_state(serverHost)
                play(state, gamesPlayed)
        else:
            url = state['playUrl']
            direction = bot.move(state)
            newState = move(url, direction)

            print("Playing turn %d with direction %s" % (state['game']['turn'], direction))
            play(newState, gamesPlayed)

    state = get_new_game_state(serverHost)
    print("Start: " + state['viewUrl'])
    play(state)

if __name__ == "__main__":
    if (len(sys.argv) > 2):
        start(sys.argv[1], RandomBot(), int(sys.argv[2]))
    else:
        print("Usage: %s <server> <number-of-games>" % (sys.argv[0]))
        print('Example: %s http://localhost:9000 20' % (sys.argv[0]))
