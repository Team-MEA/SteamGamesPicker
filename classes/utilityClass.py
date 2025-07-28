from classes.userClass import User
from classes.gameClass import Game
from constants import STEAM_ID_LINK, STEAM_PROFILE_SIGNATURE_IMG_LINK, STEAM_PROFILE_URL_FOR_PARSE
import random
import requests
from bs4 import BeautifulSoup

headers = {         # scraper does not work without this, this was the auto-complete but it seems to work
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

class Utility:    
    
    @staticmethod
    def find_common_games(main_user: User, selected_friends: list[User]) -> list[Game]:
        """
        Takes primary user, and a group of selected friends (not all friends). Returns a list of games they have in common.
        """
        if main_user is None:
            raise ValueError("'main_user not found.")
        if not isinstance(main_user, User):
                raise TypeError(f"Input 'main_user' in Utility.find_common_games must be an instance of the User class.")        
        if not isinstance(selected_friends, list):
            raise TypeError("Input 'selected_friends' in Utility.find_common_games must be a list.")
        if not selected_friends:
            raise ValueError("Seems like no friends were selected.")
        for i, friend in enumerate(selected_friends):
            if not isinstance(friend, User):
                raise TypeError(f"All elements in 'selected_friends' in Utility.find_common_games must be instances of the User class. "
                                f"Found non-User element at index {i}: {type(friend)}")

        games_shared_with_friends = set(main_user.game_list) # It's more efficient keeping it as set for the whole loop duration
        for x in range(0, len(selected_friends)):
            if selected_friends[x].is_account_private or len(selected_friends[x].game_list) == 0:
                continue
            print(f"games_shared is now: {games_shared_with_friends}")
            games_shared_with_friends = games_shared_with_friends.intersection(selected_friends[x].game_list)
            if not games_shared_with_friends:
                break # Exits the loop early for efficiency
        return list(games_shared_with_friends) # Don't forget to prepare for empty list scenario when using this method
        
    @staticmethod
    def reduce_games_list_from_tags(filtering_tags: list[str], list_of_games: list[Game]) -> list[Game]:
        """
        Filters a list of Game objects, returning a new list containing only unique games that possess ALL of the specified filtering tags.
        """
        if not isinstance(list_of_games, list):
            raise TypeError("Input 'list_of_games' in Utility.reduce_games_list_from_tags must be a list.")
        if not list_of_games:
            raise ValueError("The 'list_of_games' is empty.")
        for i, game in enumerate(list_of_games):
            if not isinstance(game, Game):
                raise TypeError(f"All elements in 'list_of_games' in Utility.reduce_games_list_from_tags must be instances of the Game class. "
                                f"Found non-Game element at index {i}: {type(game)}")
        if not isinstance(filtering_tags, list):
            raise TypeError("Input 'filtering_tags' in Utility.reduce_games_list_from_tags must be a list.")        
        if not filtering_tags:
            return list_of_games
        for i, tag in enumerate(filtering_tags):
            if not isinstance(tag, str):
                raise TypeError(f"All elements in 'filtering_tags' in Utility.reduce_games_list_from_tags must be strings. "
                                f"Found non-string element at index {i}: {type(tag)}")
        reduced_list = []
        for game in list_of_games:
            if all(tag in game.tags for tag in filtering_tags):
                if game not in reduced_list:
                    reduced_list.append(game)
        return reduced_list

    @staticmethod
    def reduce_games_list_from_hours(hours: float, list_of_games: list[Game]) -> list[Game]:
        """
        Filters a list of Game objects, returning a new list containing games with playtimes less than or equal to the specified hours threshold.
        """
        if not isinstance(list_of_games, list):
            raise TypeError("Input 'list_of_games' in Utility.reduce_games_list_from_hours must be a list.")
        if not list_of_games:
            raise ValueError("The 'list_of_games' is empty.")
        for i, game in enumerate(list_of_games):
            if not isinstance(game, Game):
                raise TypeError(f"All elements in 'list_of_games' in Utility.reduce_games_list_from_hours must be instances of the Game class. "
                                f"Found non-Game element at index {i}: {type(game)}")
        if hours is None:
            return list_of_games
        if isinstance(hours, bool): # Somehow easily confused for int
            raise TypeError(f"Input 'hours' in Utility.reduce_games_list_from_hours must be a float, but instead it's a {type(hours)}.")
        if isinstance(hours, int):
            hours = float(hours)
        if not isinstance(hours, float):
            raise TypeError(f"Input 'hours' in Utility.reduce_games_list_from_hours must be a float, but instead it's a {type(hours)}.")
        reduced_list = []
        for game in list_of_games:
            if game.hours <= hours:
                reduced_list.append(game)
        return reduced_list
   
    @staticmethod
    def get_all_tags_from_games_list(list_of_games: list[Game]) -> list[str]:
        """
        Extracts all unique tags from a list of Game objects and returns them in alphabetical order.
        """
        if not isinstance(list_of_games, list):
            raise TypeError("Input 'list_of_games' in Utility.get_all_tags_from_games_list must be a list.")
        if not list_of_games:
            raise ValueError("The 'list_of_games' is empty.")
        for i, game in enumerate(list_of_games):
            if not isinstance(game, Game):
                raise TypeError(f"All elements in 'list_of_games' in Utility.get_all_tags_from_games_list must be instances of the Game class. "
                                f"Found non-Game element at index {i}: {type(game)}")
        tags_set = set()
        for game in list_of_games:
            if game.tags: # if not None or empty
                tags_set = tags_set | set(game.tags)
        sorted_tags = sorted(list(tags_set), key=str.lower)
        return sorted_tags

    @staticmethod
    def get_random_selection(list_of_games: list[Game]) -> Game:
        random_selection = random.randint(0, len(list_of_games) - 1)
        return list_of_games[random_selection]
    
    @staticmethod
    def get_user_info(user_id): # check to see the privacy status of the user profile
        user_id_link = STEAM_ID_LINK + user_id
        is_account_private = True
        username = ""
        signature = STEAM_PROFILE_SIGNATURE_IMG_LINK + user_id + ".png"

        response = requests.get(user_id_link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')    #soup is the whole webpage
        info_table = soup.find("table", id = "profile-info")
        if info_table is None:
            raise Exception("lookup failed, invalid ID")
        search_string = "profile state"

        table_rows = info_table.find_all("tr")
        for child in table_rows:
            if search_string in child.get_text(strip=True).lower():
                if "public" in child.get_text(strip=True).lower():
                    is_account_private = False   # if both are correct, the profile is public
                    break
                if "private" in child.get_text(strip=True).lower():
                    break # for optimization
    
        for row in table_rows:
            row_text = row.get_text(strip=True).lower()
            if row_text.startswith("name"):
                username = row_text.split("name")[1].strip()
                break

        return (user_id, username, is_account_private, signature)
    
    @staticmethod
    def create_main_user(user_id):       # GUI will call this one to create the MainUser
        from classes.mainUserClass import MainUser
        user_info = Utility.get_user_info(user_id)
        id = user_info[0]
        username = user_info[1]
        is_private = user_info[2]
        signature = user_info[3]
        if is_private:
            raise PermissionError("The user account is private, please set it to public and retry. The account status may not update instantly.") 
        return MainUser(id, username, None, is_private, signature)
        
    @staticmethod
    def create_full_users_from_list(list_of_users):        # GUI will call this one to create a list of selected friend Users
        list_of_full_users = []            
        for user in list_of_users:
            user_info = Utility.get_user_info(user.user_id)
            user.is_private = user_info[2]
            list_of_full_users.append(user)
        return list_of_full_users

    @staticmethod
    def create_user_simple(user_id, name):          # Used when generating a friend list
        signature = STEAM_PROFILE_SIGNATURE_IMG_LINK + user_id + ".png"
        return User(user_id, name, None, True, signature)
    
    @staticmethod
    def get_steamid_from_url(steam_url:str) -> str:
        steamid = steam_url
        steamid = steamid.replace(STEAM_PROFILE_URL_FOR_PARSE, "")
        return steamid