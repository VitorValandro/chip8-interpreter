import pygame
from ..chip8.Renderer import Renderer


class PygameRenderer(Renderer):
    def __init__(self, scale):
        super().__init__()
        self.scale = scale
        self.screen = pygame.display.set_mode(
            (self.cols * scale, self.rows * scale))
        self.display = [0] * self.rows * self.cols

        pygame.display.set_caption('CHIP-8 interpreter renderer')

    def setPixel(self, x, y):
        if x > self.cols:
            x -= self.cols
        elif x < 0:
            x += self.cols

        if y > self.rows:
            y -= self.rows
        elif y < 0:
            y += self.rows

        pixelIndex = (x + y * self.cols)
        if pixelIndex == 2048:
            pixelIndex -= 1

        self.display[pixelIndex] ^= 1
        return self.display[pixelIndex] == 0

    def clear(self):
        self.display = [0] * self.rows * self.cols

    def render(self):
        black = (0, 0, 0)
        white = (255, 255, 255)

        self.screen.fill(black)

        for i in range(len(self.display)):
            x = (i % self.cols) * self.scale
            y = (i // self.cols) * self.scale

            if self.display[i] == 1:
                pygame.draw.rect(self.screen, white,
                                 (x, y, self.scale, self.scale))

        pygame.display.update()
