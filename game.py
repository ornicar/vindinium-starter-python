
json = resp.json()
strTiles = json['game']['board']['tiles']
size = json['game']['board']['size']
tiles = [string[i:i+2] for i in range(0, len(string), 2)]

# board is a two dimension vector
board = [tiles[i:i+size] for i in range(0, len(tiles), size)]

TAVERN = 0
AIR = -1
WALL = -2
PLAYER1 = 10
PLAYER2 = 11
PLAYER3 = 12
PLAYER4 = 13

class Board:
    def parseTile(str):
        if (str == '  '):
            return AIR
        if (str == '##'):
            return WALL
        if (str == '[]'):
            return TAVERN

    def __init__(self, tiles):
        self.tiles = tiles


class Hero:
    def __init__(self, id, name, pos, life, gold):
        self.id = id
        self.name = name
        self.pos = pos
        self.life = life
        self.gold = gold


