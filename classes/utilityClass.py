from userClass import User
from gameClass import Game
from constants import UPPER_LIMIT, LOWER_LIMIT, UPPER_MAX_BATCH, LOWER_MAX_BATCH, SCALING_FACTOR

class Utility:    

    '''takes primary user, and a group of selected friends (not all friends). return a list of games they have in common'''
    def find_common_games(main_user: User, selected_friends: list[User]) -> list[Game]:
        if main_user == None:
            return None
        games_shared_with_friends = selected_friends[0].game_list
        for x in range(0, len(selected_friends)):
            if selected_friends[x].is_account_private or len(selected_friends[x].game_list) == 0:
                continue
            games_shared_with_friends = list(set(games_shared_with_friends).intersection(selected_friends[x].game_list))
        return games_shared_with_friends
        

    def reduce_games_list_from_genre(filtering_genre, list_of_games):
        pass

    def reduce_games_list_from_hours(hours, list_of_games):
        pass

    def get_all_tags_from_games_list(list_of_games):
        pass

    def get_max_batch(filtered_games):
        length = len(filtered_games)
        if length > UPPER_LIMIT:
            return UPPER_MAX_BATCH
        elif length >= LOWER_LIMIT and length <= UPPER_LIMIT:
            return length//SCALING_FACTOR
        else:
            return LOWER_MAX_BATCH

    def get_batch_from_list(list_of_games, batch_size):
        length = len(list_of_games)
        if length <= batch_size:
            return list_of_games
        else:
            return list_of_games[length-batch_size:]
        
    