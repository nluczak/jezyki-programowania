import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Organisms.Antelope import Antelope
from Position import Position
from Action import Action, ActionEnum

class MockPos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockWorld:
    def __init__(self):
        self.moves = []

    def getNeighboringPositions(self, pos): return []
    def filterPositionsWithoutAnimals(self, pos): return []
    def getOrganismFromPosition(self, pos): return None
    def positionOnBoard(self, pos): return True
    def makeMove(self, action): self.moves.append(action)

class TestAntelope(unittest.TestCase):
    def setUp(self):
        self.world = MockWorld()
        self.position = Position(MockPos(3, 3))
        self.antelope = Antelope(position=self.position, world=self.world)

    def test_initialization(self):
        self.assertEqual(self.antelope.sign, 'A')
        self.assertEqual(self.antelope.power, 4)

    def test_clone(self):
        clone = self.antelope.clone()
        self.assertIsInstance(clone, Antelope)
        self.assertEqual(clone.sign, 'A')

if __name__ == '__main__':
    unittest.main()
