class MainLogic:
    def __init__(self):
        self.started = False
        self.use_ki = False
        self.playername1 = None
        self.playername2 = None
        self.current_player_id = 1

    def get_started(self):
        return self.started
    
    def start_game(self, use_ki, playername1, playername2):
        self.use_ki = use_ki
        self.playername1 = playername1
        if use_ki:
            self.playername2 = "Computer"
        else:
            self.playername2 = playername2
        self.started = True

    def get_current_player_name(self):
        if self.current_player_id == 1:
            return self.playername1
        if self.current_player_id == 2:
            return self.playername2
