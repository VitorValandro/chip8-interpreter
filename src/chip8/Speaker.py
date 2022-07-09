from abc import ABC, abstractmethod


class Speaker(ABC):
    @abstractmethod
    def play(self):
        '''
        Função responsável por tocar um som quando chamada.
        '''
        pass

    def stop(self):
        '''
        Função responsável por parar de tocar um som quando chamada.
        '''
        pass
