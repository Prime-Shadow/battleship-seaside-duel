class Player:
    def __init__(self, name):
        self.name = name
        self.board = None  # Board instance assigned by App
        self.guesses = []  # List to track previous guesses
        self.ships = []  # not used directly (Board holds Ship objects)

    def place_ships(self):
        # convenience: tell player's board to place ships randomly
        if self.board is not None:
            return self.board.place_ships_randomly()
        return False

    def has_lost(self):
        if self.board is None:
            return False
        return self.board.all_ships_sunk()