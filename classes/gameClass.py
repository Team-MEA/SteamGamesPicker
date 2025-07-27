class Game:
def __init__(self, app_id: str, name: str, tags: list[str] = None, hours: float = None, image: str = None, is_selected: bool = False) -> None:
        """
        Represents a single game within the Steam Games Picker application.

        This class encapsulates all relevant data for a game and provides methods
        for managing its selection state and enabling proper comparison and representation.
        """
        self.app_id = app_id
        self.name = name
        self.tags = tags
        self.hours = hours
        self.image = image
        self.is_selected = is_selected  # Will be continuously checked by the GUI to visualize the selection

    def switch_selection(self):
        """
        Toggles the 'is_selected' status of the game.
        If the game is selected, it becomes unselected, and vice-versa.
        """
        if self.is_selected:
            self.is_selected = False
        else:
            self.is_selected = True

    def __eq__(self, other_game):
        """
        Compares two Game objects for equality based on their 'app_id'.
        Two games are considered equal if they have the same app_id.
        """
        if not isinstance(other_game, Game):
            return NotImplemented # Python's convention for __eq__ when types are incompatible is to return NotImplemented singleton
        return self.app_id == other_game.app_id
    
    def __str__(self):
        """
        Returns a user-friendly string representation of the Game object, which is its name.
        """
        return self.name
    
    def __repr__(self):
        """
        Returns an unambiguous string representation of the Game object. By default, it uses the __str__ method.
        """
        return self.__str__()
    
    def __hash__(self):
        """
        Returns a hash value for the Game object, allowing it to be used in sets
        and as dictionary keys. Hashing is based on 'app_id' and 'name'.
        """
        return hash((self.app_id, self.name))
