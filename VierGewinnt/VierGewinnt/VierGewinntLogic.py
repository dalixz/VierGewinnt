class MainLogic:
    def __init__(self):
        self.started = False
        self.use_ki = False
        self.playername1 = None
        self.playername2 = None
        self.current_player_id = 1
        self.holes = [[Hole() for _ in range(6)] for _ in range(7)]  
        self.winner_player_id = 0

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

        #Prüfen, ob schon jemand gewonnen hat
        if self.winner_player_id > 0:
            raise Exception("Spiel ist bereits beendet")

        #iteration der vertikalen holes. unterstes hole herausfinden
        destination_hole = None
        destination_vertical_index = 0
        for hole in self.holes[columm_index]:
            if not hole.get_is_used():
                destination_hole = hole
                destination_vertical_index += 1

        destination_vertical_index -= 1

        #False zurückgeben wenn column schon voll ist
        if destination_hole == None:
            return False

        destination_hole.set_used(self.current_player_id)

        #prüfen ob jemand gewonnen hat
        if self.check_win_by(self.current_player_id, columm_index, destination_vertical_index):
            self.winner_player_id = self.current_player_id

        #spieler wechseln
        if self.current_player_id == 1:
            self.current_player_id = 2
        else:
            self.current_player_id = 1

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

    def check_win_by(self, player_id, horizontal_index, vertical_index):
        matches = 0

        vertical_matches = 0
        horizontal_matches = 0

        #horizintal
        for h in range (0, 7):
            if self.holes[h][vertical_index].get_is_used_by() == player_id or ((len(self.holes[h]) - 1 >= (vertical_index - h)) and self.holes[h][vertical_index - h].get_is_used_by() == player_id) or ((len(self.holes[h]) + 1 >= (vertical_index + h)) and self.holes[h][vertical_index + h].get_is_used_by() == player_id):
                horizontal_matches += 1
                if horizontal_matches >= 4:
                    matches += 1
            else:
                horizontal_matches = 0
                if horizontal_matches >= 4:
                    matches += 1

        #vertical
        for v in range (0, 6):
            if self.holes[horizontal_index][v].get_is_used_by() == player_id:
                vertical_matches += 1
                if vertical_matches >= 4:
                    matches += 1
            else:
                vertical_matches = 0
                if vertical_matches >= 4:
                    matches += 1

        #quer durchn garten
        print(str(matches))

        if matches >= 1:
            return True

        return False
        




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

        