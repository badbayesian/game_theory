import unittest
from game_theory.model import game
from game_theory import example_payoffs as ex


class TestModels(unittest.TestCase):

    def setUp(self):
        self.BoS1 = game(name="Battle of The Sexes 1", payoffs=ex.BoS1)
        self.BoS2 = game(name="Battle of The Sexes 2", payoffs=ex.BoS2)
        self.chicken = game(name="Chicken", payoffs=ex.chicken)
        self.coordinate_side = game(name="Coordination Side",
                                    payoffs=ex.coordinate_side)
        self.coordinate = game(name='Coordinate', payoffs=ex.coordinate)
        self.prisoners_dilemma = game(name="Prisoner's Dilemma",
                                      payoffs=ex.prisoners_dilemma)

    def test_correct_nash(self):
        assert(self.prisoners_dilemma.nash_location == [[1, 1]])


if __name__ == "__main__":
    unittest.main()
