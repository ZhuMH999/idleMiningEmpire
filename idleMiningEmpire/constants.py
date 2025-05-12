import pygame

pygame.font.init()

WIDTH, HEIGHT = 600, 800

STAGES = [[300, 0, (100, 100, 255)],
          [200, 300, (100, 0, 0)]]

elevatorShaftScale = [20, 41]
elevatorBuildingScale = [37, 39]
elevatorScale = [16, 29]
elevatorScaleFactor = 5

cartScale = [21, 14]
cartScaleFactor = 3

elevatorShaft = pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevatorShaft.png'), (elevatorShaftScale[0] * elevatorScaleFactor, elevatorShaftScale[1] * elevatorScaleFactor))
elevatorBuilding = pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevatorBuilding.png'), (elevatorBuildingScale[0] * elevatorScaleFactor, elevatorBuildingScale[1] * elevatorScaleFactor))
elevator = pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevator.png'), (elevatorScale[0] * elevatorScaleFactor, elevatorScale[1] * elevatorScaleFactor))
cart = pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/cart.png'), (cartScale[0] * cartScaleFactor, cartScale[1] * cartScaleFactor))

ELEVATOR_SHAFT_FONT = pygame.font.SysFont('Arial', 15)

BUILDINGS = [[elevatorShaft, 60, 300],
             [elevatorShaft, 60, 500, 1],
             [elevatorShaft, 60, 700, 2],
             [elevatorShaft, 60, 900, 3],
             [elevatorShaft, 60, 1100, 4],
             [elevatorShaft, 60, 1300, 5],
             [elevatorShaft, 60, 1500, 6],
             [elevatorShaft, 60, 1700, 7],
             [elevatorShaft, 60, 1900, 8],
             [elevatorShaft, 60, 2100, 9],
             [elevatorBuilding, 60, STAGES[0][0] - (elevatorBuildingScale[1]-4) * elevatorScaleFactor]]