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

def start(serverHost, bot):

    def play(state):
        if (state['game']['finished']):
            print('game finished')
        else:
            url = state['playUrl']
            direction = bot.move(state)
            newState = move(url, direction)

            print("Playing turn %d with direction %s" % (state['game']['turn'], direction))
            play(newState)

    state = get_new_game_state(serverHost)
    print("Start: " + state['viewUrl'])
    play(state)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        start(sys.argv[1], RandomBot())
    else:
        print('Specify the server, ex: "http://localhost:9000"')
