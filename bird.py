import pygame

BIRD_IMG = [
	pygame.transform.scale2x(pygame.image.load('imgs/bird1.png')),
	pygame.transform.scale2x(pygame.image.load('imgs/bird2.png')),
	pygame.transform.scale2x(pygame.image.load('imgs/bird3.png'))
]


class Bird:
    IMGS = BIRD_IMG
    ROTACAO_MAX = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_img = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura -= self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
            
        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX

        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_img += 1
        if self.contagem_img < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
            
        elif self.contagem_img < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_img < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_img < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_img < self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_img = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_img = self.TEMPO_ANIMACAO * 2

        img_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_img_center = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = img_rotacionada.get_rect(center=pos_img_center)
        tela.blit(img_rotacionada, retangulo.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)