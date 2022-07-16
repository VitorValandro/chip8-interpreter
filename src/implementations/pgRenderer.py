import pygame
from ..chip8.Renderer import Renderer


class PygameRenderer(Renderer):
    def __init__(self, scale):
        super().__init__()
        self.scale = scale
        self.screen = pygame.display.set_mode(
            (self.cols * scale, self.rows * scale))
        self.display = self.matrix_generator(self.cols, self.rows)

        pygame.display.set_caption('CHIP-8 interpreter renderer')

    def setPixel(self, x, y):
        if x >= self.cols:
            x -= self.cols
        elif x < 0:
            x += self.cols

        if y >= self.rows:
            y -= self.rows
        elif y < 0:
            y += self.rows

        self.display[y][x] ^= 1
        return self.display[y][x] == 0

    def clear(self):
        self.display = self.matrix_generator(self.cols, self.rows)

    def render(self):
        black = (0, 0, 0)
        white = (255, 255, 255)

        self.screen.fill(black)

        for i in range(self.rows):
            y = i * self.scale
            for j in range(self.cols):
                x = j * self.scale

                if self.display[i][j] == 1:
                    pygame.draw.rect(self.screen, white,
                                     (x, y, self.scale, self.scale))

        pygame.display.update()

    def matrix_generator(self, col, lines):
        matrix = []
        for i in range(lines):
            l = []
            for j in range(col):
                l.append(0)
            matrix.append(l)

        return matrix
