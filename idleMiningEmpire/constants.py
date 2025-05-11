import pygame

WIDTH, HEIGHT = 600, 800

STAGES = [[300, 0, (100, 100, 255)],
          [200, 300, (100, 0, 0)]]

elevatorLevelD = [20, 41]
elevatorDock = [31, 34]
scaleFactor = 5

BUILDINGS = [[pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevatorLevel.png'), (elevatorLevelD[0] * scaleFactor, elevatorLevelD[1] * scaleFactor)), 60, 300],
             [pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevatorLevel.png'), (elevatorLevelD[0] * scaleFactor, elevatorLevelD[1] * scaleFactor)), 60, 500],
             [pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevatorLevel.png'), (elevatorLevelD[0] * scaleFactor, elevatorLevelD[1] * scaleFactor)), 60, 700],
             [pygame.transform.scale(pygame.image.load('idleMiningEmpire/assets/elevatorDock.png'), (elevatorDock[0] * scaleFactor, elevatorDock[1] * scaleFactor)), 60, STAGES[1][0] - (elevatorDock[0]-1) * scaleFactor]]