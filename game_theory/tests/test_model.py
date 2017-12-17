import unittest
from game_theory.model import game
from game_theory.example_payoffs import BoS1, BoS2, chicken, coordinate_side, \
        coordinate, prisoners_dilemma


class TestModels(unittest.TestCase):

    def setUp(self):
        self.BoS1 = game(name="Battle of The Sexes 1", payoffs=BoS1)
        self.BoS2 = game(name="Battle of The Sexes 2", payoffs=BoS2)
        self.chicken = game(name="Chicken", payoffs=chicken)
        self.coordinate_side = game(name="Coordination Side",
                                    payoffs=coordinate_side)
        self.coordinate = game(name='Coordinate', payoffs=coordinate)
        self.prisoners_dilemma = game(name="Prisoner's Dilemma",
                                      payoffs=prisoners_dilemma)

    def test_nash_location(self):
        assert(self.BoS1.nash_location == [[0, 0], [1, 1]] and
               self.BoS2.nash_location == [[0, 0], [1, 1]] and
               self.chicken.nash_location == [[0, 1], [1, 0]] and
               self.coordinate_side.nash_location == [[0, 0], [1, 1]] and
               self.coordinate.nash_location == [[0, 0], [1, 1]] and
               self.prisoners_dilemma.nash_location == [[1, 1]])


if __name__ == "__main__":
    unittest.main()
