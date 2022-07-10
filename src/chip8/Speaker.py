from abc import ABC, abstractmethod


class Speaker(ABC):
    def __init__(self):
        '''
        Os sons do chip8 irão corresponder aos dispositivos originais,
        com frequência fixa de 440 hertz e sample rate de 44.1 khz.
        Esses valores podem ser alterados usando polimorfismo.
        '''
        self.frequency = 440
        self.sample_rate = 44100  # 44.1 Khz

    @abstractmethod
    def play(self):
        '''
        Função responsável por tocar um som quando chamada.
        Pode-se usar a frequência e sample rate especificados ou qualquer outra combinação.
        Pode-se criar uma onda em qualquer formato.
        '''
        pass

    def stop(self):
        '''
        Função responsável por parar de tocar um som quando chamada.
        '''
        pass
