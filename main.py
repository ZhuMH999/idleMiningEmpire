import pygame
from idleMiningEmpire.constants import WIDTH, HEIGHT, STAGES, BUILDINGS, ELEVATOR_SHAFT_FONT, elevatorShaftScale, elevatorScaleFactor, elevator, cart, button

class View:
    def __init__(self, model, win):
        self.model = model
        self.win = win

    def draw(self):
        self.win.fill((100, 100, 100))

        for stage in STAGES:
            if stage[3] in self.model.unlocked_stages:
                pygame.draw.rect(self.win, stage[2], (0, stage[1] - self.model.camy, WIDTH, stage[0]))

        for building in BUILDINGS:
            if building[3] in self.model.unlocked_stages:
                self.win.blit(building[0], (building[1], building[2] - self.model.camy))

                if building[3] != 0:
                    pygame.draw.rect(self.win, (80, 80, 80), (building[1] + (elevatorShaftScale[0]*elevatorScaleFactor/2) - 15, building[2] + (elevatorShaftScale[1]*elevatorScaleFactor/2) - 15 - self.model.camy, 30, 30))
                    self.get_text_widget_and_center((0, 0, 0), building[1] + (elevatorShaftScale[0]*elevatorScaleFactor/2), building[2] + (elevatorShaftScale[1]*elevatorScaleFactor/2) - self.model.camy, ELEVATOR_SHAFT_FONT, str(building[3]), 0)

        for thing in self.model.moving_things:
            if thing.stage in self.model.unlocked_stages:
                self.win.blit(thing.image, (thing.posx, thing.posy - self.model.camy))

        for thing in self.model.buttons:
            if thing.stage in self.model.unlocked_stages:
                self.win.blit(thing.image, (thing.x, thing.y - self.model.camy))

                for i in range(len(thing.text)):
                    self.get_text_widget_and_center((0, 0, 0), thing.x + 10, thing.y + 5 - self.model.camy + i*20, ELEVATOR_SHAFT_FONT, thing.text[i], 1)

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text, centerorleft):  # center = 0, left = 1
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        if centerorleft == 0:
            rect.center = (c_x, c_y)
        elif centerorleft == 1:
            rect.topleft = (c_x, c_y)

        self.win.blit(widget, rect)

class MovingObject:
    def __init__(self, image, x, y, posx, posy, vel, direction_switch_condition, template_stops, stop_side, stage, manager=False, moving_condition=True, affected_by_stages=False):
        self.image = image

        self.xdir = x
        self.ydir = y
        self.posx = posx
        self.posy = posy
        self.vel = vel

        self.stage = stage
        self.direction_switch_condition = direction_switch_condition
        self.template_stops = template_stops
        self.stops_left = []
        self.stop_side = stop_side
        self.manager = manager
        self.moving_condition = moving_condition
        self.affected_by_stages = affected_by_stages
        self.moving = False
        self.stop_timer = 0
        self.load = 0

    def handle_movement(self, unlocked_stages):
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
                    self.stops_left = self.handle_stops(unlocked_stages)

                    self.vel *= -1

                    if self.xdir:
                        self.posx += self.vel
                    elif self.ydir:
                        self.posy += self.vel

                elif len(self.stops_left) == 0:
                    self.stops_left = self.handle_stops(unlocked_stages)
                    self.vel *= -1

                else:
                    if self.xdir:
                        self.posx += self.vel
                    elif self.ydir:
                        self.posy += self.vel

            else:
                self.stop_timer -= 1

    def handle_stops(self, unlocked_stages):
        if self.affected_by_stages:
            new_stops = []
            for stop in self.template_stops:
                stage = int((stop - 330) / 200)
                if stage in unlocked_stages:
                    new_stops.append(stop)

            return new_stops
        else:
            return self.template_stops

    def handle_click(self, unlocked_stages, f_items, d_items):
        self.moving = True

class Elevator(MovingObject):
    def handle_click(self, unlocked_stages, f_items, d_items):
        for i in range(len(f_items)):
            if i in unlocked_stages and f_items[i] != 0:
                self.moving = True

class Cart(MovingObject):
    def handle_click(self, unlocked_stages, f_items, d_items):
        if d_items != 0:
            self.moving = True


class StaticObject:
    def __init__(self, image, x, y, stage, next_stage, cost, text, disappear=False):
        self.image = image
        self.x = x
        self.y = y
        self.stage = stage
        self.next_stage = next_stage
        self.cost = cost
        self.text = text
        self.disappear = disappear

    def handle_click(self, money):
        if money >= self.cost:
            return money - self.cost, self.next_stage
        else:
            return None, None

class Model:
    def __init__(self):
        self.run = True
        self.money = 0
        self.camy = 0
        self.unlocked_stages = [0]

        self.moving_things = [Elevator(elevator, False, True, 70, 320, -2, lambda x, y: y < 320, [int(300 + 200 * (i+1) + 30) for i in range(9)], lambda vel: vel > 0, 1, affected_by_stages=True),
                              Cart(cart, True, False, 500, 258, 2, lambda x, y: x > 500, [184], lambda vel: vel < 0, 0)]

        # image, x, y, stage, nextstage, cost, text, disappear
        self.buttons = [StaticObject(button, 370, 700, 0, 1, 0, ['Buy', 'Elevator: $0'], True),
                        StaticObject(button, 450, 600, 1, 2, 0, ['testing'], True)]

        self.f_items = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.d_items = 0

    def handle_keypress(self, key):
        if key == 0 and self.camy != 0:
            self.camy -= 10
            if self.camy < 0:
                self.camy = 0
        elif key == 1:
            self.camy += 10

    def handle_mouseclick(self, x, y):
        for i in range(len(self.moving_things)):
            print(f'i: {i}, moving: {self.moving_things[i].moving}')
            if self.moving_things[i].image.get_rect(topleft=(self.moving_things[i].posx, self.moving_things[i].posy - self.camy)).collidepoint((x, y)) and not self.moving_things[i].moving and self.moving_things[i].stage in self.unlocked_stages:
                self.moving_things[i].handle_click(self.unlocked_stages, self.f_items, self.d_items)

        for b in self.buttons:
            if b.image.get_rect(topleft=(b.x, b.y - self.camy)).collidepoint((x, y)) and b.stage in self.unlocked_stages:
                new_money, stage = b.handle_click(self.money)
                if new_money is not None:
                    self.money = new_money
                    self.unlocked_stages.append(stage)
                    if b.disappear:
                        self.buttons.remove(b)

    def handle_movement(self):
        for thing in self.moving_things:
            thing.handle_movement(self.unlocked_stages)

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
