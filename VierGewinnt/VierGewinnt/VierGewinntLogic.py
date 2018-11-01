class MainLogic:
    def __init__(self):
        self.started = False
        self.use_ki = False

    def get_started(self):
        return self.started
    
    def start_game(self, use_ki):
        self.use_ki = use_ki
        self.started = True
