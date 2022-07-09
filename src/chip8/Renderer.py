from abc import ABC, abstractmethod


class Renderer(ABC):
    def __init__(self):
        self.cols = 64
        self.rows = 32

    @abstractmethod
    def setPixel(self, x, y):
        '''
        Função para desenhar ou apagar o pixel da coordenada (x, y).
        Se um pixel está posicionado fora dos limites da tela, deve-se
        cruzar a tela e desenhá-lo a partir do lado oposto.
        Deve retornar True se o pixel foi apagado e False se foi desenhado.
        '''

    @abstractmethod
    def clear(self):
        '''
        Função para limpar a tela.
        '''

    @abstractmethod
    def render(self):
        '''
        Função para ser executada em loop e atualizar a tela conforme os dados de display se alteram.
        '''
