import re

class Game:
    def __init__(self, state):
        self.state = state
        self.board = Board(state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]

class Board:
    def parseTile(self, str):
        if (str == '  '):
            return AIR
        if (str == '##'):
            return WALL
        if (str == '[]'):
            return TAVERN
        match = re.match('\$([-0-9])', str)
        if (match):
            return MineTile(match.group(1))
        match = re.match('\@([0-9])', str)
        if (match):
            return HeroTile(match.group(1))

    def parseTiles(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        vector2n = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]
        return [self.parseTile(c) for line in vector2n for c in line]

    def __init__(self, board):
        self.size = board['size']
        self.tiles = self.parseTiles(board['tiles'])

class Hero:
    def __init__(self, hero):
        self.name = hero['name']
        self.pos = hero['pos']
        self.life = hero['life']
        self.gold = hero['gold']



# tiles
class HeroTile:
    def __init__(self, id):
        self.id = id

class MineTile:
    def __init__(self, heroId = None):
        self.heroId = heroId

TAVERN = 0
AIR = -1
WALL = -2

