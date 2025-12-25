class Ship:
    def __init__(self, name, size, coordinates, symbol):
        self.name = name
        self.size = size
        self.coordinates = list(coordinates)  # list of (x,y)
        self.hits = set()
        self.symbol = symbol

    def hit(self, coordinate):
        if coordinate in self.coordinates and coordinate not in self.hits:
            self.hits.add(coordinate)
            return True
        return False

    def is_sunk(self):
        return len(self.hits) >= self.size

    def get_coordinates(self):
        return list(self.coordinates)

    def __str__(self):
        return f"Ship(name={self.name}, size={self.size}, coordinates={self.coordinates}, hits={list(self.hits)})"