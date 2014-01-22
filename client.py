#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import re
from bot import RandomBot, SlowBot

TIMEOUT=15

def get_new_game_state(server_url, key, mode='training', number_of_turns = '10'):
    """Get a JSON from the server containing the current state of the game"""

    if(mode=='training'):
        params = { 'key': key, 'turns': number_of_turns}
        r = requests.post(server_url + '/api/training', params, timeout=TIMEOUT)

        if(r.status_code == 200):
            return r.json()
        else:
            print("Error when creating the game")
            print(r.text)
    elif(mode=='arena'):
        params = { 'key': key}

        #Wait for 10 minutes
        r = requests.post(server_url + '/api/arena', params, timeout=10*60)

        if(r.status_code == 200):
            return r.json()
        else:
            print("Error when creating the game")
            print(r.text)

def move(url, direction):
    """Send a move to the server
    
    Moves can be one of: 'Stay', 'North', 'South', 'East', 'West' 
    """

    try:
        r = requests.post(url, {'dir': direction}, timeout=TIMEOUT)

        if(r.status_code == 200):
            return r.json()
        else:
            print("Error HTTP %d\n%s\n" % (r.status_code, r.text))
            return {'game': {'finished': True}}
    except requests.exceptions.RequestException as e:
        print(e)
        return {'game': {'finished': True}}


def is_finished(state):
    return state['game']['finished']

def start(server_url, key, mode, bot):
    """Starts a game with all the required parameters"""


    if(mode=='arena'):
        print(u'Connected and waiting for other players to join…')
    # Get the initial state
    state = get_new_game_state(server_url, key, mode)
    print("Playing at: " + state['viewUrl'])

    while not is_finished(state):
        # Some nice output ;)
        sys.stdout.write('.')
        sys.stdout.flush()

        # Move to some direction
        url = state['playUrl']
        direction = bot.move(state)
        state = move(url, direction)


if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print("Usage: %s <key> <[training|arena]> <number-of-games-to-play> [server-url]" % (sys.argv[0]))
        print('Example: %s mySecretKey training 20' % (sys.argv[0]))
    else:
        number_of_games = int(sys.argv[3])
        key = sys.argv[1]
        mode = sys.argv[2]

        if(len(sys.argv) == 5):
            server_url = sys.argv[4]
        else:
            server_url = "http://vindinium.jousse.org"

        for i in range(number_of_games):
            start(server_url, key, mode, RandomBot())
            print("\nGame finished: %d/%d" % (i+1, number_of_games))
