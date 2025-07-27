from classes.userClass import User
from classes.gameClass import Game

class MainUser(User):
    """
    Represents the primary user of the application, inheriting from the User class.
    This class adds a friend_list and custom behavior for generating its game list.
    """
    def __init__(self, user_id: str, name: str, game_list: list[Game] = None, is_account_private: bool = True, profile_image: str = None) -> None:
        super().__init__(user_id = user_id,
                         name = name,
                         game_list = game_list, # Needed for Tests
                         is_account_private = is_account_private,
                         profile_image = profile_image)
        if game_list is None:
            self.game_list = self.get_game_list()
        self.friend_list = self.get_friend_list()

    def get_game_list(self) -> list[Game]:
        """
        Overrides the get_game_list method from the User class.
        Returns a list of Game objects with the following fields: app_id, name, tags, hours, image.
        """
        pass 

    def get_friend_list(self) -> list[User]:
        """
        Returns a list of User objects, aka friends, with the following fields: 
        """
        pass