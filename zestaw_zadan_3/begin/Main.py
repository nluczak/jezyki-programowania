from World import World
from Position import Position
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Organisms.Antelope import Antelope
from Organisms.Lynx import Lynx
import os

VALID_ORGANISMS = ["Sheep", "Grass", "Antelope", "Lynx"]

def is_valid_position(x, y, width=10, height=10):
    return 0 <= x < width and 0 <= y < height

def is_valid_organism_name(name):
    return name in VALID_ORGANISMS

WORLD_WIDTH = 10
WORLD_HEIGHT = 10

def is_valid_position(x, y):
    return 0 <= x < WORLD_WIDTH and 0 <= y < WORLD_HEIGHT

if __name__ == '__main__':
    pyWorld = World(WORLD_WIDTH, WORLD_HEIGHT)

    pyWorld.addOrganism(Grass(position=Position(xPosition=9, yPosition=9), world=pyWorld))
    pyWorld.addOrganism(Grass(position=Position(xPosition=1, yPosition=1), world=pyWorld))
    pyWorld.addOrganism(Sheep(position=Position(xPosition=2, yPosition=2), world=pyWorld))
    pyWorld.addOrganism(Antelope(position=Position(xPosition=4, yPosition=4), world=pyWorld))
    pyWorld.addOrganism(Lynx(position=Position(xPosition=6, yPosition=6), world=pyWorld))

    print(pyWorld)

    for i in range(0, 50):
        command = input("Enter = next turn\n"
                        "type 'plague' = activate plague\n"
                        "type 'add' = add new organism\n")
        os.system('cls')

        if command == "plague":
            pyWorld.activate_plague()

        elif command == "add":
            org_type = input("Enter organism type (Sheep, Grass, Antelope, Lynx): ")
            if org_type not in VALID_ORGANISMS:
                print("Unknown organism type!")
                input("Press Enter to continue...")
                continue

            try:
                x = int(input("Enter x (0-9): "))
                y = int(input("Enter y (0-9): "))
            except ValueError:
                print("Invalid input! Coordinates must be numbers.")
                input("Press Enter to continue...")
                continue

            if not is_valid_position(x, y):
                print("Invalid coordinates! Must be in range 0-9.")
                input("Press Enter to continue...")
                continue

            pos = Position(xPosition=x, yPosition=y)

            if pyWorld.getOrganismFromPosition(pos) is not None:
                print("This position is already occupied!")
                input("Press Enter to continue...")
                continue

            if org_type == "Sheep":
                newOrg = Sheep(position=pos, world=pyWorld)
            elif org_type == "Grass":
                newOrg = Grass(position=pos, world=pyWorld)
            elif org_type == "Antelope":
                newOrg = Antelope(position=pos, world=pyWorld)
            elif org_type == "Lynx":
                newOrg = Lynx(position=pos, world=pyWorld)

            pyWorld.addOrganism(newOrg)
            print(f"Added {org_type} at ({x}, {y})")
            input("Press Enter to continue...")

        else:
            pyWorld.makeTurn()

        print(pyWorld)
