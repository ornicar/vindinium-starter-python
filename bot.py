from random import choice

class Bot:
    pass

class RandomBot(Bot):

    def move(state):
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)
