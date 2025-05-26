from .Animal import Animal
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Position import Position


class Antelope(Animal):

    def __init__(self, antelope=None, position=None, world=None):
        super(Antelope, self).__init__(antelope, position, world)

    def clone(self):
        return Antelope(self, None, None)

    def initParams(self):
        self.power = 4
        self.initiative = 3
        self.liveLength = 11
        self.powerToReproduce = 5
        self.sign = 'A'

    def getNeighboringPosition(self):
        """ Checking if the Lynx is nearby """
        neighboring_positions = self.world.getNeighboringPositions(self.position)
        free_positions = self.world.filterPositionsWithoutAnimals(neighboring_positions)

        lynx_positions = []
        for pos in neighboring_positions:
            animal = self.world.getOrganismFromPosition(pos)
            if animal and animal.sign == 'R':
                lynx_positions.append(pos)

        if lynx_positions:
            escape_directions = []
            for lynx_pos in lynx_positions:

                dx = self.position.x - lynx_pos.x
                dy = self.position.y - lynx_pos.y

                escape_pos1 = Position(
                    xPosition=self.position.x + dx,
                    yPosition=self.position.y + dy
                )
                escape_pos2 = Position(
                    xPosition=escape_pos1.x + dx,
                    yPosition=escape_pos1.y + dy
                )

                if (self.world.positionOnBoard(escape_pos2) and
                        not self.world.getOrganismFromPosition(escape_pos2)):
                    return [escape_pos2]
                elif (self.world.positionOnBoard(escape_pos1) and
                      not self.world.getOrganismFromPosition(escape_pos1)):
                    return [escape_pos1]

            return []

        return free_positions

    def collision(self, attacker):
        """" If attacked by lynx, try to escape first """
        if attacker.sign == 'R':
            possible_escape_positions = self.getNeighboringPosition()
            if possible_escape_positions:
                self.world.makeMove(Action(
                    action=ActionEnum.A_MOVE,
                    organism=self,
                    position=possible_escape_positions[0]
                ))
                return False

        return super().collision(attacker)