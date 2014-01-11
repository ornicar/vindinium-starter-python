import requests
import re


resp = requests.get('http://localhost:9000/api/training/alone')
json = resp.json()

strTiles = json['game']['board']['tiles']
size = json['game']['board']['size']
tiles = [string[i:i+2] for i in range(0, len(string), 2)]

TAVERN = 0
AIR = -1
WALL = -2

def parseTile(str):
    if ('  ' == str):
        return AIR
    if ('##' == str):
        return WALL
    if ('[]' == str):
        return TAVERN

