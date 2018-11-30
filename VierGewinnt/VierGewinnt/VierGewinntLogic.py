class MainLogic:
    def __init__(self):
        self.started = False
        self.use_ki = False
        self.playername1 = None
        self.playername2 = None
        self.current_player_id = 1
        self.holes = [[Hole() for _ in range(6)] for _ in range(7)]  

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

    def set_by_column(self, columm_index):
        if columm_index > (len(self.holes) - 1):
            raise ValueError("invalid column index")

        #iteration der vertikalen holes. unterstes hole herausfinden
        destination_hole = None
        for hole in self.holes[columm_index]:
            if not hole.get_is_used():
                destination_hole = hole

        #False zurückgeben wenn column schon voll ist
        if destination_hole == None:
            return False

        destination_hole.set_used(self.current_player_id)
        return True   

    def get_hole_is_used(self, column_index, vertical_index):
        return self.get_hole(column_index, vertical_index).get_is_used()

    def get_hole_is_used_by(self, column_index, vertical_index):
        hole = self.get_hole(column_index, vertical_index)

        #probe ignorieren
        if not hole.get_is_used():
            return 0

        return hole.get_is_used_by()

    def get_hole(self, column_index, vertical_index):
        if column_index > (len(self.holes) - 1):
            raise ValueError("invalid column index")

        column = self.holes[column_index]

        if vertical_index > (len(column) - 1):
            raise ValueError("invalid vertical index")

        return column[vertical_index]


class Hole:
    def __init__(self):
        self.used_by = 0
        self.probe = False

    def set_used(self, by):
        self.used_by = by
        self.probe = False

    def set_probe(self, by):
        self.used_by = by

    def clear_use(self):
        self.used_by = 0
        self.probe = False

    def get_is_used(self):
        return self.used_by > 0 and not self.probe

    def get_is_probe(self):
        return self.used_by > 0 and self.probe

    def get_is_used_by(self):
        return self.used_by

        