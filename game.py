import pygame
from bird import Bird
from floor import Floor
from pipe import Pipe
import neat

ai_is_playing = True
generation = 0

SCREEN_X, SCREEN_Y = 480, 720
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load('imgs/bg.png'))

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 20)


def draw_screen(screen, birds, pipes, floor, score):
    # desenhando os objetos
    screen.blit(BACKGROUND_IMG, (0, 0))
    for pipe in pipes:
        pipe.desenhar(screen)
    for bird in birds:
        bird.desenhar(screen)
        
    # textos
    text = FONTE_PONTOS.render(f"Pontuação: {score}", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_X - 10 - text.get_width(), 10))
    if ai_is_playing:
        gen_text = FONTE_PONTOS.render(
            f"Geração: {generation}", 1, (255, 255, 255)
        )
        screen.blit(gen_text, (10, 10))
    
    floor.desenhar(screen)
    pygame.display.update()


def main(genomas=None, config=None):
    global generation
    generation += 1
    
    if ai_is_playing:
        networks = []
        genomas_list = [] 
        birds = []
        for _, genoma in genomas:
            network = neat.nn.FeedForwardNetwork.create(genoma, config)
            networks.append(network)
            genoma.fitness = 0
            genomas_list.append(genoma)
            birds.append(Bird(130, 350))
    else:
        birds = [Bird(130, 350)]
    
    floor = Floor(690)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    score = 0
    fps = pygame.time.Clock()
    running = True
    while running:
        fps.tick(30)
        
        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                
            if not ai_is_playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        [bird.pular() for bird in birds]
        
        # pegando índice do cano mais proximo
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > (
                pipes[0].x + pipes[0].img_topo.get_width()
            ):
                pipe_index = 1
        else:
            running = False
            break
        
        # movendo objetos
        for i, bird in enumerate(birds):
            bird.mover()
            if ai_is_playing:
                genomas_list[i].fitness += 0.1
                output = networks[i].activate(
                    (
                        bird.y,
                        abs(bird.y - pipes[pipe_index].altura),
                        abs(bird.y - pipes[pipe_index].pos_base)
                    )
                )
                
                if output[0] > 0.5:
                    bird.pular()
        floor.mover()
        
        # capturando colisões dos pipes com os pássaros
        add_pipe = False
        pipes_to_remove = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colidir(bird):
                    birds.pop(i)
                    if ai_is_playing:
                        genomas_list[i].fitness -= 1
                        genomas_list.pop(i)
                        networks.pop(i)
                    
                if not pipe.passou and bird.x > pipe.x:
                    pipe.passou = True
                    add_pipe = True
            pipe.mover()
             
            if pipe.x + pipe.img_topo.get_width() < 0:
                pipes_to_remove.append(pipe)
                
        if add_pipe:
            score += 1
            pipes.append(Pipe(500))
            if ai_is_playing:
                for genoma in genomas_list:
                    genoma.fitness += 5
                
        for pipe in pipes_to_remove:
            pipes.remove(pipe)
        
        # colisão com o chão
        for i, bird in enumerate(birds):
            if (bird.y + bird.imagem.get_width()) > floor.y or bird.y < 0:
                birds.pop(i)
                if ai_is_playing:
                    genomas_list.pop(i)
                    networks.pop(i)
        
        draw_screen(screen, birds, pipes, floor, score)


def run(file_config_path):
    neat_config = neat.config.Config(neat.DefaultGenome,
                                     neat.DefaultReproduction,
                                     neat.DefaultSpeciesSet,
                                     neat.DefaultStagnation,
                                     file_config_path)
    
    population = neat.Population(neat_config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    
    if ai_is_playing:
        population.run(main, 50)
    else:
        main()
    

if __name__ == '__main__':
    run('conf.txt')
