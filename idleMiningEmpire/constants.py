import pygame

pygame.font.init()

WIDTH, HEIGHT = 600, 800

STAGES = [[300, 0, (100, 100, 255)],
          [200, 300, (100, 0, 0)]]

elevatorShaftScale = [20, 41]
elevatorBuildingScale = [37, 39]
scaleFactor = 5

elevatorShaft = pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevatorShaft.png'), (elevatorShaftScale[0] * scaleFactor, elevatorShaftScale[1] * scaleFactor))
elevatorBuilding = pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevatorBuilding.png'), (elevatorBuildingScale[0] * scaleFactor, elevatorBuildingScale[1] * scaleFactor))

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
             [elevatorBuilding, 60, STAGES[0][0] - (elevatorBuildingScale[1]-4) * scaleFactor]]