import pygame, random

CANO_IMG = pygame.transform.scale2x(pygame.image.load('imgs/pipe.png'))


class Pipe:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.img_topo = pygame.transform.flip(CANO_IMG, False, True)
        self.img_base = CANO_IMG
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.img_topo.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.img_topo, (self.x, self.pos_topo))
        tela.blit(self.img_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.img_topo)
        base_mask = pygame.mask.from_surface(self.img_base)

        distancia_topo = self.x - passaro.x, self.pos_topo - round(passaro.y)
        distancia_base = self.x - passaro.x, self.pos_base - round(passaro.y)

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        if topo_ponto or base_ponto:
            return True
        return False