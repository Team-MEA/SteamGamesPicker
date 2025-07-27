import random
from classes.stateClass import State
from classes.gameClass import Game
from constants import UPPER_LIMIT, UPPER_MAX_BATCH, LOWER_LIMIT, LOWER_MAX_BATCH, SCALING_FACTOR

class Session:
    """
    Manages the overall game selection process, including historical states
    and the generation of game batches.
    """
    def __init__(self, list_of_games: list[Game]) -> None:
        """
        Initializes a new game selection session.
        Args:
            list_of_games (list): The initial list of all games available for selection.
        """
        if not isinstance(list_of_games, list):
            raise TypeError("Input 'list_of_games' in Session class must be a list.")
        if not list_of_games:
            raise ValueError("The 'list_of_games' cannot be empty. Please re-check your selections.")
        for i, game in enumerate(list_of_games):
            if not isinstance(game, Game):
                raise TypeError(f"All elements in 'list_of_games' in Session class must be instances of the Game class. "
                                f"Found non-Game element at index {i}: {type(game)}")

        self.current_index = 0
        self.starter_list = list(list_of_games) 
        random.shuffle(self.starter_list) 
        self.current_batch_size = self.get_max_batch(self.starter_list)
        self.history_array = [State(self.generate_batch_info(self.starter_list))]
    
    @staticmethod
    def get_max_batch(games: list[Game]):
        """
        Determines the maximum batch size based on the total number of games.
        Args:
            games (list): The list of games to consider for batch size calculation.
        Returns:
            int: The calculated maximum batch size.
        """
        length = len(games)
        if length > UPPER_LIMIT:
            return UPPER_MAX_BATCH
        elif length >= LOWER_LIMIT and length <= UPPER_LIMIT:
            return length//SCALING_FACTOR
        else:
            return LOWER_MAX_BATCH

    def generate_batch_info(self, games: list[Game], seen_games: list[Game] = []):
        """
        Recursively generates information for the next batch of games.
        This method manages the core logic of shrinking the batch size,
        replenishing the remaining games from seen games,
        and shuffling after replenishing.
        It is called from __generate_next_state.
        Args:
            games (list): The list of games currently considered 'remaining'.
            seen_games (list, optional): Games that have been seen/processed.
                                         Defaults to None.
        Returns:
            tuple: A tuple containing (batch, remaining_games, seen_games) for the next state.
        """
        length = len(games)
        if hasattr(self, "history_array"): # Checks if history_array exists and is not empty, important for the Session class initialization, which does not create this field at this point yet.
            prev_state = self.history_array[self.current_index] # Index not yet incremented, so current_index is fine
            prev_batch = prev_state.batch
            if prev_batch:
                for game in prev_batch:
                    if game.is_selected:
                        game.is_selected = False
                        seen_games.append(game)
        if length < self.current_batch_size:
            if seen_games:
                games.extend(seen_games) 
                random.shuffle(games) 
                seen_games = [] 
                self.current_batch_size -= 1
                return self.generate_batch_info(games, seen_games) # Recursive call with modified games and decremented batch size
            else:
                batch = list(games) 
                return (batch, games[:len(games)-len(batch)], seen_games)
        else:
            batch = games[length-self.current_batch_size:] 
            return (batch, games[:len(games)-len(batch)], seen_games)

    def __generate_next_state(self):
        """
        Internal method to compute and create the next State object.
        It processes the current state's remaining and seen games to
        determine the content of the next batch and updates the state
        based on user selections from the current batch.
        Returns:
            State: A newly generated State object representing the next step
                   in the game selection process.
        """
        current_state = self.history_array[self.current_index]
        batch_info = self.generate_batch_info(current_state.remaining_games, current_state.seen_games)
        return State(batch_info)

    def reset(self):    # called by a GUI Button
        """
        Resets the session to its initial state.
        This clears the entire history, re-shuffles the original game list,
        and recalculates the initial batch size, effectively starting a new game.
        """
        self.current_index = 0
        self.current_batch_size = self.get_max_batch(self.starter_list)
        random.shuffle(self.starter_list)
        self.history_array = [State(self.generate_batch_info(self.starter_list))]

    def confirm(self):  # called by a GUI Button
        """
        Confirms the user's selections in the current batch and advances the session.
        If at least one game is selected in the current batch:
        - It generates the next State.
        - Appends the new State to the history.
        - Increments the current_index to point to the new State.
        If no selection is made, the session state does not change.
        """
        current_state = self.history_array[self.current_index]
        selection_done = False
        for game in current_state.batch:
            if game.is_selected:
                selection_done = True
                break # Optimization note: no need to check further if one is found
        if selection_done:
            new_state = self.__generate_next_state()
            self.history_array.append(new_state)
            self.current_index += 1

    def undo(self): # called by a GUI Button
        """
        Reverts the session to the previous state in its history.
        Decrements the current_index, effectively going back in time.
        Cannot undo if already at the very first state (index 0).
        """
        if self.current_index != 0:
            self.current_index -= 1

    def redo(self): # called by a GUI Button
        """
        Advances the session to a future state in its history, if available.
        Increments the current_index, effectively redoing a previously undone action.
        Cannot redo if already at the latest state in history.
        """
        length = len(self.history_array)
        if self.current_index < length-1:
            self.current_index += 1
    
