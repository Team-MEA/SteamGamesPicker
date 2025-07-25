class Game:
    def __init__(self, app_id, name, tags, hours, is_selected=False):
        self.app_id = app_id
        self.name = name
        self.tags = tags
        self.hours = hours
        self.is_selected = is_selected

    def switch_selection(self):
        if self.is_selected:
            self.is_selected = False
        else:
            self.is_selected = True

    def __eq__(self, other_game):
        if isinstance(other_game, Game):
            return self.app_id == other_game.app_id
        return NotImplementedError
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash((self.app_id, self.name))
