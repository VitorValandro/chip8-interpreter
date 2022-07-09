import pygame
from ..chip8.Keyboard import Keyboard


class PygameKeyboard(Keyboard):
    def __init__(self):
        super().__init__()
        # polimorfismo do KEYMAP para se ajustar aos eventos do pygame
        self.KEYMAP = {
            pygame.K_1: 0x1,  # 1
            pygame.K_2: 0x2,  # 2
            pygame.K_3: 0x3,  # 3
            pygame.K_4: 0xc,  # 4
            pygame.K_q: 0x4,  # Q
            pygame.K_w: 0x5,  # W
            pygame.K_e: 0x6,  # E
            pygame.K_r: 0xd,  # R
            pygame.K_a: 0x7,  # A
            pygame.K_s: 0x8,  # S
            pygame.K_d: 0x9,  # D
            pygame.K_f: 0xe,  # F
            pygame.K_z: 0xa,  # Z
            pygame.K_x: 0x0,  # X
            pygame.K_b: 0xb,  # C
            pygame.K_v: 0xf,  # V
        }

    def isKeyPressed(self, keyCode):
        '''
        Função que recebe o keyCode de uma tecla que deve retornar
        True se está pressionada e False senão
        '''
        return self.keysPressed[keyCode]

    def onKeyDown(self, keyCode):
        '''
        Função chamada quando usuário aperta uma tecla. Deve-se armazenar a tecla apertada no array
        self.keysPressed e verificar se a função self.onNextKeyPress foi chamada pela instrução LD Vx, K (0xFx0A)
        '''
        if keyCode in self.KEYMAP.keys():
            key = self.KEYMAP.get(keyCode)
            self.keysPressed[key] = True

            if self.onNextKeyPressed != None:
                self.onNextKeyPressed(int(key))
                self.onNextKeyPressed = None

    def onKeyUp(self, keyCode):
        '''
        Função chamda quando usuário solta uma tecla. Deve-se retirar a tecla que estava apertada do array
        self.keysPressed
        '''
        if keyCode in self.KEYMAP.keys():
            key = self.KEYMAP.get(keyCode)
            self.keysPressed[key] = False
