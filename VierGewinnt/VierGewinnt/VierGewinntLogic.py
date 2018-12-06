import random

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
            return True

        #spieler wechseln
        if self.current_player_id == 1:
            self.current_player_id = 2
        else:
            self.current_player_id = 1

        if self.use_ki and self.current_player_id == 2:
            self.compute_ki(columm_index)
            self.reset_all_probes()
            if self.winner_player_id == 0:
                self.current_player_id = 1

        return True 

    def compute_ki(self, last_column_index):
        #prüfen ob ein gewinn durch einen einwurf möglich ist
        for i in range(0, 6):
            destination_hole = None
            destination_vertical_index = -1

            for hole in self.holes[i]:
                if not hole.get_is_used():
                    destination_hole = hole
                    destination_vertical_index += 1

            if destination_hole != None:
                destination_hole.set_probe(2)

                if self.check_win_by(2, i, destination_vertical_index):
                    destination_hole.set_used(2)
                    self.winner_player_id = self.current_player_id
                    return

            self.reset_all_probes()

        #prüfen ob gegner durch den nächsten einwurf gewinnen kann und ggf. diese möglichkeit entfernen
        for i in range(0, 6):
            destination_hole = None
            destination_vertical_index = -1

            for hole in self.holes[i]:
                if not hole.get_is_used():
                    destination_hole = hole
                    destination_vertical_index += 1

            if destination_hole != None:
                destination_hole.set_probe(1)

                if self.check_win_by(1, i, destination_vertical_index):
                    destination_hole.set_used(2)
                    return

            self.reset_all_probes()

        #dort einwerfen wo zuletzt der user eingeworfenhat
        destination_hole = None
        destination_vertical_index = -1

        for hole in self.holes[last_column_index]:
            if not hole.get_is_used():
                destination_hole = hole
                destination_vertical_index += 1

        if destination_hole != None:
            destination_hole.set_used(2)
            return

        #ansonsten random setzen
        for i in range(0, 200):
            x = random.randint(0, 6)
            destination_hole = None
            destination_vertical_index = -1
            for hole in self.holes[x]:
                if not hole.get_is_used():
                    destination_hole = hole
                    destination_vertical_index += 1

            if destination_hole != None:
                destination_hole.set_used(2)
                return
        
        return


    def reset_all_probes(self):
        for column in self.holes:
            for hole in column:
                if hole.get_is_probe():
                    hole.clear_use()

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
        matches_vertical = 0
        matches_horizontal = 0
        matches_q1 = 0
        matches_q2 = 0

        #horizintal
        for h in range (0, 7):
            if self.holes[h][vertical_index].get_is_used_by() == player_id:
                matches_horizontal += 1
            else:
                matches_horizontal = 0

            if matches_horizontal >= 4:
                return True

        #vertical
        for v in range (0, 6):
            if self.holes[horizontal_index][v].get_is_used_by() == player_id:
                matches_vertical += 1
            else:
                matches_vertical = 0

            if matches_vertical >= 4:
                return True

        #quer
        q1_start_offset = 0
        q1_end_offset = 0
        q2_start_offset = 0
        q2_end_offset = 0
        for i in range(1, 6):
            #links oben -> rechts unten
            if vertical_index - i >= 0 and horizontal_index - i >= 0:
                q1_start_offset = i
            if vertical_index + i <= 6 and horizontal_index + i <= 7:
                q1_end_offset = i
            #links unten -> rechts oben
            if vertical_index + i <= 5 and horizontal_index - i >= 0:
                q2_start_offset = i
            if vertical_index - i >= 0 and horizontal_index + i <= 7:
                q2_end_offset = i

        for i in range(q1_start_offset * -1, q1_end_offset):
            if self.holes[horizontal_index + i][vertical_index + i].get_is_used_by() == player_id:
                matches_q1 += 1
            else:
                matches_q1 = 0

            if matches_q1 >= 4:
                return True

        for i in range(q2_start_offset * -1, q2_end_offset):
            if self.holes[horizontal_index + i][vertical_index - i].get_is_used_by() == player_id:
                matches_q2 += 1
            else:
                matches_q2 = 0

            if matches_q2 >= 4:
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
        self.probe = True

    def clear_use(self):
        self.used_by = 0
        self.probe = False

    def get_is_used(self):
        return self.used_by > 0 and not self.probe

    def get_is_probe(self):
        return self.used_by > 0 and self.probe

    def get_is_used_by(self):
        return self.used_by

        