import pygame

FLOOR_IMG = pygame.transform.scale2x(pygame.image.load('imgs/base.png'))

class Floor:
    VELOCIDADE = 5
    LARGURA = FLOOR_IMG.get_width() - 5
    IMAGEM = FLOOR_IMG
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA + 2
        
    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA
            
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))