import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from Main import is_valid_position, is_valid_organism_name
from Position import Position
from World import World
from Organisms.Sheep import Sheep
from Organisms.Grass import Grass

def create_position(x, y):
    class DummyPos:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    return Position(DummyPos(x, y))

class TestMainFunctions(unittest.TestCase):

    def test_valid_position_check(self):
        self.assertTrue(is_valid_position(0, 0))
        self.assertTrue(is_valid_position(9, 9))
        self.assertFalse(is_valid_position(-1, 5))
        self.assertFalse(is_valid_position(10, 0))
        self.assertFalse(is_valid_position(3, 10))

    def test_valid_organism_name(self):
        self.assertTrue(is_valid_organism_name("Sheep"))
        self.assertFalse(is_valid_organism_name("Dragon"))
        self.assertFalse(is_valid_organism_name(""))

class TestPosition(unittest.TestCase):

    def test_position_equality(self):
        pos1 = create_position(2, 3)
        pos2 = create_position(2, 3)
        self.assertEqual(pos1, pos2)

    def test_position_inequality(self):
        pos1 = create_position(1, 1)
        pos2 = create_position(2, 2)
        self.assertNotEqual(pos1, pos2)

class TestWorld(unittest.TestCase):

    def setUp(self):
        self.world = World(10, 10)

    def test_add_and_get_organism(self):
        pos = create_position(4, 4)
        sheep = Sheep(position=pos, world=self.world)
        self.world.addOrganism(sheep)

        found = self.world.getOrganismFromPosition(pos)
        self.assertIsNotNone(found)
        self.assertEqual(found, sheep)

    def test_add_organism_to_taken_position(self):
        pos = create_position(2, 2)
        sheep = Sheep(position=pos, world=self.world)
        grass = Grass(position=pos, world=self.world)

        self.world.addOrganism(sheep)
        self.world.addOrganism(grass)

        found = self.world.getOrganismFromPosition(pos)
        self.assertIn(found.__class__.__name__, ["Sheep", "Grass"])
