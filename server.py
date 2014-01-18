#!/usr/bin/env python

import os
import sys
import requests
import re
from bot import RandomBot

def get_new_game_state(server_host, key, number_of_turns = '20', mode='training'):
    if(mode=='training'):
        params = { 'key': key, 'turns': number_of_turns}
        r = requests.post(server_host + '/api/training', params)

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

def start(server_host, key, bot, number_of_games = 20):

    def play(state, games_played = 0):
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

    state = get_new_game_state(server_host, key)
    print("Start: " + state['viewUrl'])
    play(state)

if __name__ == "__main__":
    if (len(sys.argv) > 3):
        start(sys.argv[1], sys.argv[2], RandomBot(), int(sys.argv[3]))
    else:
        print("Usage: %s <server> <key> <number-of-games-to-play>" % (sys.argv[0]))
        print('Example: %s http://localhost:9000 mySecretKey 20' % (sys.argv[0]))
