import sys
import pygame
from src.chip8.cpu import CPU
from src.chip8.Keyboard import Keyboard
from src.chip8.Renderer import Renderer
from src.chip8.Speaker import Speaker

from src.implementations.pgRenderer import PygameRenderer
from src.implementations.pgKeyboard import PygameKeyboard

a = PygameRenderer(10)
b = PygameKeyboard()

a.setPixel(0, 0)
a.setPixel(5, 2)
a.render()

timer = pygame.time.Clock()
time = 0
while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            b.onKeyDown(event.key)

        if event.type == pygame.KEYUP:
            b.onKeyUp(event.key)
