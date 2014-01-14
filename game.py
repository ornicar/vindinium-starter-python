import re

TAVERN = 0
AIR = -1
WALL = -2

PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

AIM = {'North': (-1, 0),
       'East': (0, 1),
       'South': (1, 0),
       'West': (0, -1)}

class HeroTile:
    def __init__(self, id):
        self.id = id

class MineTile:
    def __init__(self, heroId = None):
        self.heroId = heroId

class Game:
    def __init__(self, state):
        self.state = state
        self.board = Board(state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]
        self.mines_locs = {}
        self.heroes_locs = {}
        self.taverns_locs = set([])
        for row in range(len(self.board.tiles)):
            for col in range(len(self.board.tiles[row])):
                obj = self.board.tiles[row][col]
                if isinstance(obj, MineTile):
                    self.mines_locs[(row, col)] = obj.heroId
                elif isinstance(obj, HeroTile):
                    self.heroes_locs[(row, col)] = obj.id
                elif (obj == TAVERN):
                    self.taverns_locs.add((row, col))



class Board:
    def __parseTile(self, str):
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

    def __parseTiles(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]

        return [[self.__parseTile(x) for x in xs] for xs in matrix]

    def __init__(self, board):
        self.size = board['size']
        self.tiles = self.__parseTiles(board['tiles'])

    def passable(self, loc):
        'true if can not walk through'
        x, y = loc
        pos = self.tiles[x][y]
        return (pos != WALL) and (pos != TAVERN) and not isinstance(pos, MineTile)

    def to(self, loc, direction):
        'calculate a new location given the direction'
        row, col = loc
        d_row, d_col = AIM[direction]
        n_row = row + d_row
        if (n_row < 0): n_row = 0
        if (n_row > self.size): n_row = self.size
        n_col = col + d_col
        if (n_col < 0): n_col = 0
        if (n_col > self.size): n_col = self.size

        return (n_row, n_col)

    def bfs(self, start):
        ' Breadth first search generator function '
        queue, visited = deque([(None, None, start)]), set([start])
        while queue:
            parent, direction, loc = queue.popleft()
            yield parent, direction, loc
            adjs = [(direction, self.to(loc, direction)) for direction in AIM.keys()]
            for direction, adj_loc in adjs:
                if self.passable(adj_loc) and adj_loc not in visited:
                    visited.add(adj_loc)
                    queue.append((loc, direction, adj_loc))

    def find_closest(self, start, locs_set, depth=10000):
        ' find closest in a set of locations and return searched loc and path '
        paths = {None: []}
        explored = 0
        for parent, from_dir, child in self.bfs(start):
            paths[child] = paths[parent] + [from_dir]
            explored += 1
            if child in locs_set:
                return child, deque(paths[child][1:])
            if depth and explored > depth:
                return None, None
        return None, None

    def bfs_shortest_path(self, start, end, depth=10000):
        ' return one of a possible shortest path '
        paths = {None: []}
        explored = 0
        for parent, from_dir, child in self.bfs(start):
            paths[child] = paths[parent] + [from_dir]
            explored += 1
            if child == end:
                return deque(paths[child][1:])
            if depth and explored > depth:
                return None
        return None



class Hero:
    def __init__(self, hero):
        self.name = hero['name']
        self.pos = hero['pos']
        self.life = hero['life']
        self.gold = hero['gold']


def manhattan_distance(loc1, loc2):
    'calculate the closest manhattan distance between two locations'
    row1, col1 = loc1
    row2, col2 = loc2
    d_col = min(abs(col1 - col2), self.cols - abs(col1 - col2))
    d_row = min(abs(row1 - row2), self.rows - abs(row1 - row2))
    return d_row + d_col



