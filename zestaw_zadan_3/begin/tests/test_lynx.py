import sys
import os
import unittest
from unittest.mock import Mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Organisms.Lynx import Lynx


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y


class TestLynx(unittest.TestCase):
    def setUp(self):
        self.world_mock = Mock()
        self.position = Position(5, 5)
        self.lynx = Lynx(position=self.position, world=self.world_mock)

        self.world_mock.getNeighboringPositions.return_value = [
            Position(4, 4), Position(5, 4), Position(6, 4),
            Position(4, 5), Position(6, 5),
            Position(4, 6), Position(5, 6), Position(6, 6)
        ]
        self.world_mock.filterPositionsWithoutAnimals.return_value = [
            Position(4, 5), Position(6, 5), Position(5, 6)
        ]

    def test_initialization(self):
        self.assertEqual(self.lynx.sign, 'R')
        self.assertEqual(self.lynx.power, 6)
        self.assertEqual(self.lynx.initiative, 5)
        self.assertEqual(self.lynx.liveLength, 18)
        self.assertEqual(self.lynx.powerToReproduce, 14)
        self.assertEqual(self.lynx.position.x, 5)
        self.assertEqual(self.lynx.position.y, 5)

    def test_clone(self):
        cloned = self.lynx.clone()
        self.assertIsInstance(cloned, Lynx)
        self.assertEqual(cloned.sign, 'R')
        self.assertEqual(cloned.power, 6)

        self.assertIsNotNone(cloned.position)
        self.assertEqual(cloned.position.x, self.position.x)
        self.assertEqual(cloned.position.y, self.position.y)

        self.assertIsNotNone(cloned.world)
        self.assertEqual(cloned.world, self.lynx.world)

    def test_getNeighboringPosition(self):
        result = self.lynx.getNeighboringPosition()
        self.world_mock.getNeighboringPositions.assert_called_once_with(self.position)
        self.world_mock.filterPositionsWithoutAnimals.assert_called_once()
        self.assertEqual(len(result), 3)

        self.world_mock.filterPositionsWithoutAnimals.return_value = []
        result = self.lynx.getNeighboringPosition()
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()