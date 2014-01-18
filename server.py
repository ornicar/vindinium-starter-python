#!/usr/bin/env python

import os
import sys
import requests
import re
from bot import RandomBot

SERVER_HOST = 'http://localhost:9000'

trainingState = requests.post(SERVER_HOST + '/api/training/alone').json()
state = trainingState

bot = RandomBot()

def move(url, direction):
    r = requests.post(url, {'dir': direction})
    return r.json()

def start(server_url):
    def play(state):
        if (state['game']['finished']):
            print('game finished')
        else:
            url = state['playUrl']
            direction = bot.move(state)
            newState = move(state['playUrl'], direction)

            print("Playing turn %d with direction %s" % (state['game']['turn'], direction))
            play(newState)

    print("Start: " + state['viewUrl'])
    play(state)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        SERVER_HOST = sys.argv[1]
        start(sys.argv[1])
    else:
        print('Specify the server, ex: "http://localhost:9000"')
