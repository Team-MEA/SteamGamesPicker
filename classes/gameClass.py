class Game:
    def __init__(self, app_id, name, genres, hours, is_selected=False):
        self.app_id = app_id
        self.name = name
        self.genres = genres
        self.hours = hours
        self.is_selected = is_selected

    def switch_selection(self):
        if self.is_selected:
            self.is_selected = False
        else:
            self.is_selected = True

    