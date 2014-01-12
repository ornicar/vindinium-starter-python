import requests
import re

SERVER_HOST = 'http://localhost:9000'

TAVERN = 0
AIR = -1
WALL = -2

resp = requests.get(SERVER_HOST + '/api/training/alone')
json = resp.json()

strTiles = json['game']['board']['tiles']
size = json['game']['board']['size']
tiles = [string[i:i+2] for i in range(0, len(string), 2)]

# board is a two dimension vector
board = [tiles[i:i+size] for i in range(0, len(tiles), size)]


class Board:
    def __init__(self, tiles):
        self.tiles = tiles

