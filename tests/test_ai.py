import unittest
from src.game.ai import AI
from src.game.board import Board

class TestAI(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.ai = AI(self.board)

    def test_ai_makes_valid_guess(self):
        guess = self.ai.make_guess()
        self.assertIn(guess, self.board.get_available_coordinates())

    def test_ai_tracks_hits(self):
        self.board.place_ship("A1", "horizontal", 3)  # Place a ship for testing
        self.ai.make_guess()  # AI makes a guess
        hit = self.board.check_hit(guess)
        if hit:
            self.ai.track_hit(guess)
            self.assertIn(guess, self.ai.hit_coordinates)

    def test_ai_sinks_ship(self):
        self.board.place_ship("B2", "vertical", 2)  # Place a ship for testing
        self.ai.make_guess()  # AI makes a guess
        self.board.check_hit(guess)
        if self.board.is_sunk("B2"):
            self.assertIn("You sunk my ship at B2!", self.ai.messages)

if __name__ == '__main__':
    unittest.main()