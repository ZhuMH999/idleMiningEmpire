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
            self.win.blit(thing.image, (thing.posx, thing.posy - self.model.camy))

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)

class MovingObject:
    def __init__(self, image, x, y, posx, posy, vel, direction_switch_condition, template_stops, stop_side, manager=False, moving_condition=True):
        self.image = image
        self.image_rect = self.image.get_rect(topleft=(posx, posy))

        self.xdir = x
        self.ydir = y
        self.posx = posx
        self.posy = posy
        self.vel = vel

        self.direction_switch_condition = direction_switch_condition
        self.template_stops = template_stops
        self.stops_left = copy.deepcopy(self.template_stops)
        self.stop_side = stop_side
        self.manager = manager
        self.moving_condition = moving_condition
        self.moving = False
        self.stop_timer = 0

    def handle_movement(self):
        if self.moving:
            if self.stop_timer == 0:
                if ((self.xdir and self.posx in self.stops_left) or (self.ydir and self.posy in self.stops_left)) and self.stop_side(self.vel):
                    if self.xdir:
                        self.stops_left.remove(self.posx)
                    elif self.ydir:
                        self.stops_left.remove(self.posy)

                    self.stop_timer = 60

                elif self.direction_switch_condition(self.posx, self.posy):
                    if not self.manager:
                        self.moving = False

                    self.vel *= -1

                    if self.xdir:
                        self.posx += self.vel
                    elif self.ydir:
                        self.posy += self.vel

                elif len(self.stops_left) == 0:
                    self.stops_left = copy.deepcopy(self.template_stops)
                    self.vel *= -1

                else:
                    if self.xdir:
                        self.posx += self.vel
                    elif self.ydir:
                        self.posy += self.vel

            else:
                self.stop_timer -= 1

class Model:
    def __init__(self):
        self.run = True
        self.camy = 0

        self.moving_things = [MovingObject(elevator, False, True, 70, 320, 2, lambda x, y: y < 320, [int(300 + 200 * (i+1) + 30) for i in range(9)], lambda vel: vel > 0),
                              MovingObject(cart, True, False, 500, 258, -2, lambda x, y: x > 500, [184], lambda vel: vel < 0)]

    def handle_keypress(self, key):
        if key == 0 and self.camy != 0:
            self.camy -= 10
            if self.camy < 0:
                self.camy = 0
        elif key == 1:
            self.camy += 10

    def handle_mouseclick(self, x, y):
        for i in range(len(self.moving_things)):
            if self.moving_things[i].image_rect.collidepoint((x, y)) and not self.moving_things[i].moving:
                self.moving_things[i].moving = True

    def handle_movement(self):
        for thing in self.moving_things:
            thing.handle_movement()

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
