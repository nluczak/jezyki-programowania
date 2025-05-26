from Position import Position
from Organisms.Plant import Plant
from Action import Action
from ActionEnum import ActionEnum


class World(object):

    def __init__(self, worldX, worldY):
        self.__worldX = worldX
        self.__worldY = worldY
        self.__turn = 0
        self.__organisms = []
        self.__newOrganisms = []
        self.__separator = '.'
        self.__plague_mode = False
        self.__plague_turns_remaining = 0
        self.__original_lifespans = {}

    @property
    def worldX(self):
        return self.__worldX

    @property
    def worldY(self):
        return self.__worldY

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, value):
        self.__turn = value

    @property
    def organisms(self):
        return self.__organisms

    @organisms.setter
    def organisms(self, value):
        self.__organisms = value

    @property
    def newOrganisms(self):
        return self.__newOrganisms

    @newOrganisms.setter
    def newOrganisms(self, value):
        self.__newOrganisms = value

    @property
    def separator(self):
        return self.__separator

    @property
    def plague_mode(self):
        return self.__plague_mode

    def activate_plague(self, turns=2):
        if not self.__plague_mode:
            self.__plague_mode = True
            self.__plague_turns_remaining = turns
            self.__original_lifespans = {}

            for org in self.organisms:
                self.__original_lifespans[id(org)] = org.liveLength
                org.liveLength = max(1, org.liveLength // 2)
            print("PLAGUE ACTIVATED FOR 2 TURNS!")

    def deactivate_plague(self):
        if self.__plague_mode:
            self.__plague_mode = False
            for org in self.organisms:
                if id(org) in self.__original_lifespans:
                    org.liveLength = self.__original_lifespans[id(org)]
            self.__original_lifespans.clear()
            print("PLAGUE DEACTIVATED!")

    def makeTurn(self):
        if self.__plague_mode:
            self.__plague_turns_remaining -= 1
            if self.__plague_turns_remaining <= 0:
                self.deactivate_plague()

        actions = []

        for org in self.organisms:
            if self.positionOnBoard(org.position):
                actions = org.move()
                for a in actions:
                    self.makeMove(a)
                actions = []
                if self.positionOnBoard(org.position):
                    actions = org.action()
                    for a in actions:
                        self.makeMove(a)
                    actions = []

        self.organisms = [o for o in self.organisms if self.positionOnBoard(o.position)]
        for o in self.organisms:
            o.liveLength -= 1
            o.power += 1
            if o.liveLength < 1:
                print(str(o.__class__.__name__) + ': died of old age at: ' + str(o.position))
        self.organisms = [o for o in self.organisms if o.liveLength > 0]

        self.newOrganisms = [o for o in self.newOrganisms if self.positionOnBoard(o.position)]
        self.organisms.extend(self.newOrganisms)
        self.organisms.sort(key=lambda o: o.initiative, reverse=True)
        self.newOrganisms = []

        self.turn += 1

    def makeMove(self, action):
        print(action)
        if action.action == ActionEnum.A_ADD:
            self.newOrganisms.append(action.organism)
        elif action.action == ActionEnum.A_INCREASEPOWER:
            action.organism.power += action.value
        elif action.action == ActionEnum.A_MOVE:
            action.organism.position = action.position
        elif action.action == ActionEnum.A_REMOVE:
            action.organism.position = Position(xPosition=-1, yPosition=-1)

    def addOrganism(self, newOrganism):
        newOrgPosition = Position(xPosition=newOrganism.position.x, yPosition=newOrganism.position.y)

        if self.positionOnBoard(newOrgPosition):
            self.organisms.append(newOrganism)
            self.organisms.sort(key=lambda org: org.initiative, reverse=True)
            return True
        return False

    def positionOnBoard(self, position):
        return position.x >= 0 and position.y >= 0 and position.x < self.__worldX and position.y < self.__worldY

    def getOrganismFromPosition(self, position):
        pomOrganism = None

        for org in self.organisms:
            if org.position == position:
                pomOrganism = org
                break
        if pomOrganism is None:
            for org in self.newOrganisms:
                if org.position == position:
                    pomOrganism = org
                    break
        return pomOrganism

    def getNeighboringPositions(self, position):
        result = []
        pomPosition = None

        for y in range(-1, 2):
            for x in range(-1, 2):
                pomPosition = Position(xPosition=position.x + x, yPosition=position.y + y)
                if self.positionOnBoard(pomPosition) and not (y == 0 and x == 0):
                    result.append(pomPosition)
        return result

    def filterFreePositions(self, fields):
        result = []

        for field in fields:
            if self.getOrganismFromPosition(field) is None:
                result.append(field)
        return result

    def filterPositionsWithoutAnimals(self, fields):
        result = []
        pomOrg = None

        for filed in fields:
            pomOrg = self.getOrganismFromPosition(filed)
            if pomOrg is None or isinstance(pomOrg, Plant):
                result.append(filed)
        return result

    def __str__(self):
        result = f"\nTurn: {self.__turn}\n"
        for y in range(self.__worldY):
            for x in range(self.__worldX):
                pos = Position(xPosition=x, yPosition=y)
                org = self.getOrganismFromPosition(pos)
                if org:
                    symbol = org.sign
                    color = None

                    if self.__plague_mode:
                        symbol += 'P'

                    if self.__plague_mode and id(org) in self.__original_lifespans:
                        color = '31'
                    elif symbol.startswith('S'):
                        color = '32'
                    elif symbol.startswith('A'):
                        color = '32'
                    elif symbol.startswith('R'):
                        color = '33'
                    elif symbol.startswith('G'):
                        color = '92'

                    if color:
                        result += colorize(symbol, color)
                    else:
                        result += symbol
                else:
                    result += colorize('·', '90')  # Grey dot for empty space
            result += '\n'
        return result

def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"
