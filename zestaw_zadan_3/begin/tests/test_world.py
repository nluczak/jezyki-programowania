import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from World import World
from Position import Position

class MockPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockOrganism:
    def __init__(self, position, sign='M', initiative=0, power=0, liveLength=10):
        pos_obj = MockPosition(position[0], position[1])
        self.position = Position(pos_obj)
        self.sign = sign
        self.initiative = initiative
        self.power = power
        self.liveLength = liveLength

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.world = World(10, 10)
        self.organism = MockOrganism((1, 1), 'A', 4, 5, 10)
        self.plant = MockOrganism((2, 2), 'P', 0, 0, 20)

    def test_initialization(self):
        self.assertEqual(self.world.worldX, 10)
        self.assertEqual(self.world.worldY, 10)
        self.assertEqual(self.world.turn, 0)
        self.assertEqual(len(self.world.organisms), 0)

    def test_add_organism(self):
        result = self.world.addOrganism(self.organism)
        self.assertTrue(result)
        self.assertEqual(len(self.world.organisms), 1)

    def test_position_on_board(self):
        pos_obj = MockPosition(0, 0)
        position = Position(pos_obj)
        self.assertTrue(self.world.positionOnBoard(position))

    def test_get_organism_from_position(self):
        self.world.addOrganism(self.organism)
        pos_obj = MockPosition(1, 1)
        position = Position(pos_obj)
        org = self.world.getOrganismFromPosition(position)
        self.assertEqual(org.sign, 'A')

if __name__ == '__main__':
    unittest.main()