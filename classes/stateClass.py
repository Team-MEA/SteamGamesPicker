from gameClass import Game

class State:
    def __init__(self, remaining_games, seen_games, batch):
        self.remaining_games = remaining_games
        self.seen_games = seen_games
        self.batch = batch
