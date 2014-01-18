#!/usr/bin/env python

import os
import sys
import requests
import re
from bot import RandomBot

def get_new_game_state(server_host, key, mode='training', number_of_turns = '20'):
    """Get a JSON from the server containing the current state of the game"""

    if(mode=='training'):
        params = { 'key': key, 'turns': number_of_turns}
        r = requests.post(server_host + '/api/training', params)

        if(r.status_code == 200):
            return r.json()
        else:
            print("Error when creating the game")
            print(r.text)
    elif(mode=='arena'):
        params = { 'key': key}
        r = requests.post(server_host + '/api/arena', params)

        if(r.status_code == 200):
            return r.json()
        else:
            print("Error when creating the game")
            print(r.text)

def move(url, direction):
    """Send a move to the server
    
    Moves can be one of: 'Stay', 'North', 'South', 'East', 'West' 
    """

    r = requests.post(url, {'dir': direction})
    return r.json()

def start(server_host, key, mode, bot, number_of_games = 20):
    """Starts a game with all the required parameters"""

    def play(state, games_played = 0):
        """Main game loop"""

        if (state['game']['finished']):
            games_played += 1
            print('Game finished: %d/%d' % (games_played, number_of_games))

            if(games_played < number_of_games):
                print('asking a new game')
                state = get_new_game_state(server_host, key)
                play(state, games_played)
        else:
            url = state['playUrl']
            direction = bot.move(state)
            new_state = move(url, direction)

            print("Playing turn %d with direction %s" % (state['game']['turn'], direction))
            play(new_state, games_played)

    state = get_new_game_state(server_host, key, mode)
    print("Start: " + state['viewUrl'])
    play(state)

if __name__ == "__main__":
    if (len(sys.argv) > 4):
        start(sys.argv[1], sys.argv[2], sys.argv[3], RandomBot(), int(sys.argv[4]))
    else:
        print("Usage: %s <server> <key> <[training|arena]> <number-of-games-to-play>" % (sys.argv[0]))
        print('Example: %s http://vindinium.jousse.org mySecretKey training 20' % (sys.argv[0]))
