#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import re
from bot import RandomBot, SlowBot

TIMEOUT=15

def get_new_game_state(server_host, key, mode='training', number_of_turns = '10'):
    """Get a JSON from the server containing the current state of the game"""

    if(mode=='training'):
        params = { 'key': key, 'turns': number_of_turns}
        r = requests.post(server_host + '/api/training', params, timeout=TIMEOUT)

        if(r.status_code == 200):
            return r.json()
        else:
            print("Error when creating the game")
            print(r.text)
    elif(mode=='arena'):
        params = { 'key': key}
        r = requests.post(server_host + '/api/arena', params, timeout=TIMEOUT)

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


def start(server_host, key, mode, bot):
    """Starts a game with all the required parameters"""

    def play(state, games_played = 0):
        """Main game loop"""

        if (not state['game']['finished']):
            url = state['playUrl']
            direction = bot.move(state)
            new_state = move(url, direction)

            print("Playing turn %d with direction %s" % (state['game']['turn'], direction))
            play(new_state, games_played)

    if(mode=='arena'):
        print(u'Connected and waiting for other players to join…')

    state = get_new_game_state(server_host, key, mode)
    print("Start: " + state['viewUrl'])
    play(state)

if __name__ == "__main__":
    if (len(sys.argv) > 4):
        number_of_games = int(sys.argv[4])
        for i in range(number_of_games):
            start(sys.argv[1], sys.argv[2], sys.argv[3], RandomBot())
            print("\nGame finished: %d/%d" % (i+1, number_of_games))
    else:
        print("Usage: %s <key> <[training|arena]> <number-of-games-to-play> [server-url]" % (sys.argv[0]))
        print('Example: %s http://vindinium.jousse.org mySecretKey training 20' % (sys.argv[0]))
