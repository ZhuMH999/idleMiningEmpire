import pygame
from idleMiningEmpire.constants import WIDTH, HEIGHT, STAGES, BUILDINGS, ELEVATOR_SHAFT_FONT, elevatorShaftScale, elevatorScaleFactor, elevator, cart

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

        self.win.blit(elevator, (70, 320 + self.model.elevator[0] - self.model.camy))
        self.win.blit(cart, (185, 300 - 14 * 3 - self.model.camy))

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)

class Model:
    def __init__(self):
        self.run = True
        self.camy = 0

        self.miners = []

        self.elevator = [0, -2, 0, [int(200 * (i+1)) for i in range(9)]]  # y, vel, wait, stops

    def handle_keypress(self, key):
        if key == 0 and self.camy != 0:
            self.camy -= 10
            if self.camy < 0:
                self.camy = 0
        elif key == 1:
            self.camy += 10

    def handle_movement(self):
        self.handle_elevator_movement()

    def handle_elevator_movement(self):
        if self.elevator[2] == 0:
            if self.elevator[0] in self.elevator[3] and self.elevator[1] > 0:
                self.elevator[3].remove(self.elevator[0])
                self.elevator[2] = 60

            elif self.elevator[0] < 1:
                self.elevator[1] *= -1
                self.elevator[0] += self.elevator[1]

            elif len(self.elevator[3]) == 0:
                self.elevator[3] = [int(200 * (i + 1)) for i in range(9)]
                self.elevator[1] *= -1
                self.elevator[0] += self.elevator[1]

            else:
                self.elevator[0] += self.elevator[1]

        else:
            self.elevator[2] -= 1

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
