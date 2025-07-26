class State:
    def __init__(self, batch_info, prev_batch=[]):
        self.remaining_games = list(batch_info[1]) 
        self.seen_games = list(batch_info[2]) 
        self.batch = list(batch_info[0]) 
        self.final_pick = None
        if prev_batch:
            for game in prev_batch:
                if game.is_selected:
                    game.is_selected = False
                    self.seen_games.append(game)
        if len(self.batch) == 1:
            self.final_pick = self.batch[0]