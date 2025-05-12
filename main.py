import pygame
import copy
from idleMiningEmpire.constants import WIDTH, HEIGHT, STAGES, BUILDINGS, ELEVATOR_SHAFT_FONT, elevatorShaftScale, elevatorScaleFactor, elevator, cart, elevatorScale, cartScale, cartScaleFactor

class View:
    def __init__(self, model, win):
        self.model = model
        self.win = win

    def draw(self):
        self.win.fill((100, 100, 100))

        for stage in STAGES:
            pygame.draw.rect(self.win, stage[2], (0, stage[1] - self.model.camy, WIDTH, stage[0]))

        for building in BUILDINGS:
            self.win.blit(building[0], (building[1], building[2] - self.model.camy))

            if len(building) == 4:
                pygame.draw.rect(self.win, (80, 80, 80), (building[1] + (elevatorShaftScale[0]*elevatorScaleFactor/2) - 15, building[2] + (elevatorShaftScale[1]*elevatorScaleFactor/2) - 15 - self.model.camy, 30, 30))
                self.get_text_widget_and_center((0, 0, 0), building[1] + (elevatorShaftScale[0]*elevatorScaleFactor/2), building[2] + (elevatorShaftScale[1]*elevatorScaleFactor/2) - self.model.camy, ELEVATOR_SHAFT_FONT, str(building[3]))

        for thing in self.model.moving_things:
            self.win.blit(thing[0], (thing[3], thing[4] - self.model.camy))

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)

class Model:
    def __init__(self):
        self.run = True
        self.camy = 0

        # thing, xdir, ydir, posx, posy, vel(x or y), return true if switch direction (x or y), waiting time, stops left in cycle, template stops, only stop which side, unlocked manager, moving, moving condition (do later)
        self.moving_things = [[elevator, False, True, 70, 320, 2, lambda x, y: y < 320, 0, [int(300 + 200 * (i+1) + 30) for i in range(9)], [int(300 + 200 * (i+1) + 30) for i in range(9)], lambda vel: vel > 0, False, False],
                              [cart, True, False, 500, 258, -2, lambda x, y: x > 500, 0, [184], [184], lambda vel: vel < 0, False, False]]

    def handle_keypress(self, key):
        if key == 0 and self.camy != 0:
            self.camy -= 10
            if self.camy < 0:
                self.camy = 0
        elif key == 1:
            self.camy += 10

    def handle_mouseclick(self, x, y):
        for i in range(len(self.moving_things)):
            if not self.moving_things[i][11]:
                if i == 0:
                    if elevator.get_rect(center=(self.moving_things[0][3] + (elevatorScale[0] * elevatorScaleFactor) / 2, self.moving_things[0][4] + (elevatorScale[1] * elevatorScaleFactor) / 2 - self.camy)).collidepoint((x, y)) and not self.moving_things[i][12]:
                        self.moving_things[i][12] = True
                elif i == 1:
                    if cart.get_rect(center=(self.moving_things[1][3] + (cartScale[0] * cartScaleFactor) / 2, self.moving_things[1][4] + (cartScale[1] * cartScaleFactor) / 2 - self.camy)).collidepoint((x, y)) and not self.moving_things[i][12]:
                        self.moving_things[i][12] = True

    def handle_movement(self):
        for thing in self.moving_things:
            if thing[12]:
                if thing[7] == 0:
                    if ((thing[1] and thing[3] in thing[8]) or (thing[2] and thing[4] in thing[8])) and thing[10](thing[5]):
                        if thing[1]:
                            thing[8].remove(thing[3])
                        elif thing[2]:
                            thing[8].remove(thing[4])
                        thing[7] = 60

                    elif thing[6](thing[3], thing[4]):
                        if not thing[11]:
                            thing[12] = False

                        thing[5] *= -1
                        if thing[1]:
                            thing[3] += thing[5]
                        elif thing[2]:
                            thing[4] += thing[5]

                    elif len(thing[8]) == 0:
                        thing[8] = copy.deepcopy(thing[9])
                        thing[5] *= -1
                        if thing[1]:
                            thing[3] += thing[5]
                        elif thing[2]:
                            thing[4] += thing[5]

                    else:
                        if thing[1]:
                            thing[3] += thing[5]
                        elif thing[2]:
                            thing[4] += thing[5]

                else:
                    thing[7] -= 1

class Controller:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.model = Model()
        self.view = View(self.model, self.win)

        pygame.display.set_caption('Idle Mining Empire')

    def run(self):
        clock = pygame.time.Clock()

        while self.model.run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.model.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        self.model.handle_mouseclick(x, y)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.model.handle_keypress(0)
            elif keys[pygame.K_DOWN]:
                self.model.handle_keypress(1)

            self.model.handle_movement()
            self.view.draw()

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    c = Controller()
    c.run()
