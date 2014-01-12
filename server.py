#!/usr/bin/env python

import os
import sys
import requests
import re
from bot import *

SERVER_HOST = 'http://localhost:9000'

trainingState = requests.post(SERVER_HOST + '/api/training/alone').json()

bot = RandomBot()

def move(url, direction):
    r = requests.post(url, {'dir': direction})
    return r.json()

def start(server_url):
    def play(state):
        if (state['game']['finished']):
            print('game finished')
        else:
            play(move(state['playUrl'], RandomBot.move(state)))

    print("Start: " + trainingState['viewUrl'])
    play(state)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        SERVER_HOST = sys.argv[1]
        start(sys.argv[1])
    else:
        print('Specify the server, ex: "http://localhost:9000"')
