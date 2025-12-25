import unittest
from src.game.board import Board
from src.game.ship import Ship

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_place_ship(self):
        ship = Ship(size=3)
        result = self.board.place_ship(ship, (0, 0), 'horizontal')
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][0], ship)
        self.assertEqual(self.board.grid[0][1], ship)
        self.assertEqual(self.board.grid[0][2], ship)

    def test_place_ship_out_of_bounds(self):
        ship = Ship(size=3)
        result = self.board.place_ship(ship, (0, 8), 'horizontal')
        self.assertFalse(result)

    def test_place_ship_vertical(self):
        ship = Ship(size=3)
        result = self.board.place_ship(ship, (0, 0), 'vertical')
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][0], ship)
        self.assertEqual(self.board.grid[1][0], ship)
        self.assertEqual(self.board.grid[2][0], ship)

    def test_hit_detection(self):
        ship = Ship(size=3)
        self.board.place_ship(ship, (0, 0), 'horizontal')
        hit_result = self.board.receive_shot((0, 1))
        self.assertTrue(hit_result)
        self.assertTrue(ship.is_hit((0, 1)))

    def test_miss_detection(self):
        ship = Ship(size=3)
        self.board.place_ship(ship, (0, 0), 'horizontal')
        miss_result = self.board.receive_shot((1, 1))
        self.assertFalse(miss_result)

    def test_sinking_ship(self):
        ship = Ship(size=3)
        self.board.place_ship(ship, (0, 0), 'horizontal')
        self.board.receive_shot((0, 0))
        self.board.receive_shot((0, 1))
        sunk = self.board.receive_shot((0, 2))
        self.assertTrue(sunk)
        self.assertTrue(ship.is_sunk())

if __name__ == '__main__':
    unittest.main()