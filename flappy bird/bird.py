import pygame,sys
from pygame.locals import *
from pygame import K_SPACE
import random



pygame.init()
def createobs():
    y_pos = [ 300, 350, 400,]
    random_height=random.choice(y_pos)
    bottom_pipe=obstacle_surface.get_rect(midtop=(400,random_height))
    top_pipe = obstacle_surface.get_rect(midtop=(400,random_height-900))
    return bottom_pipe,top_pipe
def moveobs(obs):
    for ob in obs:
        ob.centerx-=3
    return obs
def drawobs(obs):
    for ob in obs:
        if ob.bottom >= 724:
            screen.blit(obstacle_surface, ob)
        else:
            flipped_pipe = pygame.transform.flip(obstacle_surface, False, True)
            screen.blit(flipped_pipe, ob)

def checkcollision(obs):
    for ob in obs:
        if bird_rect.colliderect(ob):
            return False
        if bird_rect.top<=-100  or bird_rect.bottom>=600:
            return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * -3, 2)
    return new_bird






Score = 0
font = pygame.font.Font(None, 50)
gravity = 0.25
bird_movement=0

screen = pygame.display.set_mode((476,724))
fps=120
clock = pygame.time.Clock()
bg_surface = pygame.transform.scale(pygame.image.load('images/background/background-day.png'), (476, 724)).convert_alpha()
ground_surface=pygame.image.load('images/background/base.png')
ground_surface=pygame.transform.scale2x(ground_surface)
ground_rect=ground_surface.get_rect(midbottom=(476,0 ))
bird_surface2=pygame.image.load('images/bird/bluebird-midflap.png')
bird_surface1=pygame.image.load("images/bird/bluebird-downflap.png")
bird_surface3=pygame.image.load("images/bird/bluebird-upflap.png")
bird_frames=[bird_surface1,bird_surface2,bird_surface3]
bird_index=0
bird_surface=bird_frames[bird_index]
bird_rect=bird_surface.get_rect(center=(50,300))
# bird_surface=animation(keys)
# bird_surface=pygame.transform.scale2x(bird_surface)
obstacle_surface=pygame.image.load('images/obstacles/pipe-green.png')
obstacle_surface=pygame.transform.scale2x(obstacle_surface)



obslist=[]
scored_pipes = []


floor_xpos=0
SPAWNOBS=pygame.USEREVENT
BIRD_FLAP=pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)

pygame.time.set_timer(SPAWNOBS,1200)
obslist.extend(createobs())
game_active=True

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys=pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if keys[K_SPACE]:
                bird_movement=0
                bird_movement-=10
            if keys[K_SPACE] and game_active==False:
                obslist.clear()
                scored_pipes.clear()
                bird_rect.center=(50,300)
                bird_movement=0
                Score=0
        if event.type == SPAWNOBS:
            obslist.extend(createobs())
        if event.type == BIRD_FLAP:
            bird_index += 1
            if bird_index >= len(bird_frames):
                bird_index = 0
            bird_surface = bird_frames[bird_index]
            bird_rect = bird_surface.get_rect(center=(bird_rect.centerx, bird_rect.centery))

    screen.blit(bg_surface, (0, 0))
    if game_active:
        for pipe in obslist:
            if pipe.centerx < bird_rect.left and pipe not in scored_pipes:
                scored_pipes.append(pipe)
                Score += 0.5

        rotated_bird=rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        bird_movement+=gravity
        bird_rect.centery+=bird_movement
        score_surface = font.render(f'Score: {int(Score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(238,50))
        screen.blit(score_surface, score_rect)
        obslist=moveobs(obslist)
        drawobs(obslist)
    else:
        game_over_surface=pygame.image.load('images/background/gameover.png')
        game_over_surface=pygame.transform.scale2x(game_over_surface)
        game_over_rect=game_over_surface.get_rect(center=(236,362))
        score_surface1 = font.render(f'Score: {int(Score)}', True, (0,0,0))
        score_rect1 = score_surface1.get_rect(center=(238, 500))
        screen.blit(score_surface1, score_rect1)
        screen.blit(game_over_surface, (game_over_rect))






    game_active=checkcollision(obslist)
    floor_xpos -= 1
    screen.blit(ground_surface,(floor_xpos,600))
    screen.blit(ground_surface, (floor_xpos+476, 600))
    if floor_xpos<-476:
        floor_xpos=0
    pygame.display.update()
    clock.tick(fps)