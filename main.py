import sys
import pygame
from src.chip8.cpu import CPU
from src.chip8.Keyboard import Keyboard
from src.chip8.Renderer import Renderer
from src.chip8.Speaker import Speaker

from src.implementations.pgRenderer import PygameRenderer
from src.implementations.pgKeyboard import PygameKeyboard


def main():
    renderer = PygameRenderer(10)
    keyboard = PygameKeyboard()
    chip8 = CPU(renderer, keyboard, None)

    chip8.load_sprites()
    chip8.load_data(r"C:\Users\vitor\Desktop\poo\chip8\breakout.ch8", chip8.pc)

    timer = pygame.time.Clock()
    time = 0
    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keyboard.onKeyDown(event.key)

            if event.type == pygame.KEYUP:
                keyboard.onKeyUp(event.key)

        timer.tick(60)
        chip8.cycle()


if __name__ == '__main__':
    main()
