import random
from types import SimpleNamespace
from game.ship import Ship

class Board:
    def __init__(self):
        self.size = 10
        # grid stores symbol or ' ' for empty
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []            # list[Ship]
        self.hits = set()          # set of (x,y)
        self.misses = set()        # set of (x,y)

    def is_within_bounds(self, coord):
        x, y = coord
        return 0 <= x < self.size and 0 <= y < self.size

    def is_valid_guess(self, row, col):
        return self.is_within_bounds((row, col)) and (row, col) not in self.hits and (row, col) not in self.misses

    def place_ship(self, ship: Ship, start, orientation):
        # start is (x,y)
        coords = []
        x0, y0 = start
        for i in range(ship.size):
            x = x0 + (i if orientation == 'V' else 0)
            y = y0 + (i if orientation == 'H' else 0)
            coords.append((x, y))

        # check bounds and emptiness
        for (x, y) in coords:
            if not self.is_within_bounds((x, y)) or self.grid[x][y] != ' ':
                return False

        # disallow ships touching each other (3x3 neighborhood)
        if not self._can_place_without_touching(start, orientation, ship.size):
            return False

        # place
        for (x, y) in coords:
            self.grid[x][y] = ship.symbol
        # attach coordinates to ship and store
        ship.coordinates = coords
        self.ships.append(ship)
        return True

    def receive_shot(self, coordinates):
        """
        coordinates: (row, col)
        returns tuple: (result, ship_name_or_None)
          result in {'miss', 'hit', 'sunk'}
        """
        x, y = coordinates
        if not self.is_within_bounds((x, y)):
            raise ValueError("Shot out of bounds")

        # If already shot here, treat as miss (caller should check is_valid_guess before calling)
        if (x, y) in self.hits or (x, y) in self.misses:
            return ("miss", None)

        # check ships
        for ship in self.ships:
            if (x, y) in ship.coordinates:
                ship.hit((x, y))
                self.hits.add((x, y))
                if ship.is_sunk():
                    return ("sunk", ship.name)
                else:
                    return ("hit", ship.name)

        # miss
        self.misses.add((x, y))
        return ("miss", None)

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def display(self, reveal=False):
        for r in range(self.size):
            row = []
            for c in range(self.size):
                val = self.grid[r][c]
                if val == ' ':
                    row.append('.')
                else:
                    row.append(val if reveal else '.')
            print(' '.join(row))
        print("Hits:", sorted(self.hits))
        print("Misses:", sorted(self.misses))

    def reset(self):
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []
        self.hits = set()
        self.misses = set()

    def _can_place_without_touching(self, start, orientation, size):
        x0, y0 = start
        for i in range(size):
            x = x0 + (i if orientation == 'V' else 0)
            y = y0 + (i if orientation == 'H' else 0)
            # check 3x3 neighborhood around each ship cell
            for nx in range(x - 1, x + 2):
                for ny in range(y - 1, y + 2):
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if self.grid[nx][ny] != ' ':
                            return False
        return True

    def place_ships_randomly(self):
        """
        Place the standard five ships randomly on the board ensuring ships do not touch.
        Uses Ship class instances.
        """
        ship_specs = [
            ("Carrier", 5, "C"),
            ("Battleship", 4, "B"),
            ("Cruiser", 3, "R"),
            ("Submarine", 3, "S"),
            ("Destroyer", 2, "D"),
        ]

        for name, size, symbol in ship_specs:
            placed = False
            attempts = 0
            while not placed and attempts < 2000:
                attempts += 1
                orientation = random.choice(['H', 'V'])
                if orientation == 'H':
                    x = random.randrange(0, self.size)
                    y = random.randrange(0, self.size - size + 1)
                else:
                    x = random.randrange(0, self.size - size + 1)
                    y = random.randrange(0, self.size)

                if not self._can_place_without_touching((x, y), orientation, size):
                    continue

                ship = Ship(name, size, [], symbol)
                if self.place_ship(ship, (x, y), orientation):
                    placed = True

            if not placed:
                raise RuntimeError(f"Failed to place ship {name} after many attempts")

        return True