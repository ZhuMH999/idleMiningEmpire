import pygame
from idleMiningEmpire.constants import WIDTH, HEIGHT, STAGES, BUILDINGS

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

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)

class Model:
    def __init__(self):
        self.run = True
        self.camy = 0

    def handle_keypress(self, key):
        if key == 0 and self.camy != 0:
            self.camy -= 10
            if self.camy < 0:
                self.camy = 0
        elif key == 1:
            self.camy += 10

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
                self.model.handle_keypress(1)
            elif keys[pygame.K_DOWN]:
                self.model.handle_keypress(0)

            self.view.draw()

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    c = Controller()
    c.run()
