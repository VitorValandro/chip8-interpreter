from abc import ABC, abstractmethod


class Keyboard(ABC):
    def __init__(self):
        self.KEYMAP = {
            49: 0x1,  # 1
            50: 0x2,  # 2
            51: 0x3,  # 3
            52: 0xc,  # 4
            81: 0x4,  # Q
            87: 0x5,  # W
            69: 0x6,  # E
            82: 0xd,  # R
            65: 0x7,  # A
            83: 0x8,  # S
            68: 0x9,  # D
            70: 0xe,  # F
            90: 0xa,  # Z
            88: 0x0,  # X
            67: 0xb,  # C
            86: 0xf,  # V
        }

        self.keysPressed = [0] * 16
        self.onNextKeyPressed = None

    @abstractmethod
    def isKeyPressed(self, keyCode):
        '''
        Função que recebe o keyCode de uma tecla que deve retornar
        True se está pressionada e False senão
        '''
        pass

    @abstractmethod
    def onKeyDown(self, key):
        '''
        Função chamada quando usuário aperta uma tecla. Deve-se armazenar a tecla apertada no array
        self.keysPressed e verificar se a função self.onNextKeyPress foi chamada pela instrução LD Vx, K (0xFx0A)
        '''
        pass

    @abstractmethod
    def onKeyUp(self, key):
        '''
        Função chamda quando usuário solta uma tecla. Deve-se retirar a tecla que estava apertada do array
        self.keysPressed
        '''
        pass
