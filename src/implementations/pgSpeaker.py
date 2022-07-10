import pygame
import numpy
from ..chip8.Speaker import Speaker


class PygameSpeaker(Speaker):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()

        self.buffer = numpy.sin(2 * numpy.pi * numpy.arange(self.sample_rate) * self.frequency / self.sample_rate).astype(numpy.float32)
        self.sound = pygame.mixer.Sound(self.buffer)

    def play(self):
        '''
        Função responsável por tocar um som quando chamada.
        Deve-se usar a frequência e sample rate especificados.
        Deve-se criar uma onda em forma de sino.
        '''
        self.sound.play(0)

    def stop(self):
        self.sound.stop()