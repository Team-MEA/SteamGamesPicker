import random
from .stateClass import State
from ..constants import UPPER_LIMIT, UPPER_MAX_BATCH, LOWER_LIMIT, LOWER_MAX_BATCH, SCALING_FACTOR

class Session:
    def __init__(self, list_of_games):
        self.current_index = 0
        self.starter_list = list(list_of_games) 
        random.shuffle(self.starter_list) 
        self.current_batch_size = self.get_max_batch(self.starter_list)
        self.history_array = [State(self.generate_batch_info(self.starter_list))]
    
    @staticmethod
    def get_max_batch(games):
        length = len(games)
        if length > UPPER_LIMIT:
            return UPPER_MAX_BATCH
        elif length >= LOWER_LIMIT and length <= UPPER_LIMIT:
            return length//SCALING_FACTOR
        else:
            return LOWER_MAX_BATCH

    def generate_batch_info(self, games, seen_games=[]):
        length = len(games)
        if length < self.current_batch_size:
            if seen_games:
                games.extend(seen_games) 
                random.shuffle(games) 
                seen_games = [] 
                self.current_batch_size -= 1
                return self.generate_batch_info(games, seen_games)
            else:
                batch = list(games) 
                return (batch, games[:len(games)-len(batch)], seen_games)
        else:
            batch = games[length-self.current_batch_size:] 
            return (batch, games[:len(games)-len(batch)], seen_games)

    def __generate_next_state(self):
        current_state = self.history_array[self.current_index]
        batch_info = self.generate_batch_info(current_state.remaining_games, current_state.seen_games)
        return State(batch_info, current_state.batch)

    def reset(self):
        self.current_index = 0
        self.current_batch_size = self.get_max_batch(self.starter_list)
        random.shuffle(self.starter_list)
        self.history_array = [State(self.generate_batch_info(self.starter_list))]

    def confirm(self):
        current_state = self.history_array[self.current_index]
        selection_done = False
        for game in current_state.batch:
            if game.is_selected:
                selection_done = True
                break
        if selection_done:
            new_state = self.__generate_next_state()
            self.history_array.append(new_state)

    def undo(self):
        if self.current_index != 0:
            self.current_index -= 1

    def redo(self):
        length = len(self.history_array)
        if self.current_index < length-1:
            self.current_index += 1
    
