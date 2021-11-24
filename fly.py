import pygame, sys, random

SCREEN_WIDTH = 442
SCREEN_HEIGHT = 750
CANVAS_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)  # SCREEN_width, SCREEN_height

def fraw_floor():
    screen.blit(floor_surface, (floor_x_pos, SCREEN_HEIGHT-120))
    screen.blit(floor_surface, (floor_x_pos + SCREEN_WIDTH, SCREEN_HEIGHT-120))

def create_pipe():
    rand_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop=(550, rand_pipe_pos))  # SCREEN_width should > canvas
    bottom_pipe = pipe_surface.get_rect(midbottom=(550, rand_pipe_pos-200)) # space = 2--  
    return top_pipe, bottom_pipe

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)  # (,x direction,y direction)
            screen.blit(flip_pipe, pipe)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3   # move to left
    return pipes

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= -100 or bird_rect.bottom >= SCREEN_HEIGHT-120:  # go beyond top or touch floor
        return True
    return False

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)   #(, rotate value, scale)
    return new_bird

def bird_animation():
    """flap wings"""
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(60, bird_rect.centery))
    return new_bird, new_bird_rect 

def score_display(highest_score, score, game_state):
    if game_state == 'main_game':       
        score_surface = game_font.render(str(int(score)), True, (255,255,255))  # (text, sharp style, color)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH/2, 60))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))  # (text, sharp style, color)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH/2, 60))
        screen.blit(score_surface, score_rect)

        highest_score_surface = game_font.render(f'Highest score: {int(highest_score)}', True, (255,255,255))  # (text, sharp style, color)
        highest_score_rect = score_surface.get_rect(center=(150, 600))
        screen.blit(highest_score_surface, highest_score_rect)

def add_score(score, pipes):
    for pipe in pipes:
        if not bird_rect.colliderect(pipe) and bird_rect.right >= (pipe.left + pipe.right)/2:
            score += 0.5
    return score
    

pygame.init()
screen = pygame.display.set_mode(CANVAS_SIZE)
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/04B_19.ttf',40) # (style,size)

# game variables
GRAVITY = 0.25
JUMP_SCREEN_HEIGHT = 8
game_active = True
bird_movement = 0
int_score = new_score = highest_score = 0

bg_surface = pygame.image.load("assets/images/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, CANVAS_SIZE)  

floor_surface = pygame.image.load("assets/images/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface, (SCREEN_WIDTH, 118))  
floor_x_pos = 0

# bird_surface = pygame.image.load("assets/images/bluebird-midflap.png").convert_alpha()
# bird_surface = pygame.transform.scale(bird_surface, (50, 35))  
# bird_rect = bird_surface.get_rect(center=(60,SCREEN_HEIGHT/2))

bird_down = pygame.transform.scale(pygame.image.load("assets/images/bluebird-downflap.png").convert_alpha(), (50, 35))
bird_mid = pygame.transform.scale(pygame.image.load("assets/images/bluebird-midflap.png").convert_alpha(), (50, 35))
bird_up = pygame.transform.scale(pygame.image.load("assets/images/bluebird-upflap.png").convert_alpha(), (50, 35))
bird_frames = [bird_down, bird_mid, bird_up]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(60,SCREEN_HEIGHT/2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)  # change index every 200ms

pipe_surface = pygame.image.load("assets/images/pipe-green.png").convert()
pipe_surface = pygame.transform.scale(pipe_surface, (80, 492))  # w/h = 0.1625
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # trigger time, 1200ms
pipe_height = [300, 400, 500]

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= JUMP_SCREEN_HEIGHT
            if event.key == pygame.K_SPACE and game_active == False:  # restart game
                game_active = True
                pipe_list.clear()
                bird_rect.center = (60,SCREEN_HEIGHT/2)
                bird_movement = 0 
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # bird
        bird_movement += GRAVITY
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        game_active = not check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        new_score = add_score(int_score, pipe_list)
        if new_score > highest_score:
            highest_score = new_score
        score_display(highest_score, new_score, "main_game")
    else:
        score_display(highest_score, new_score, "game_over")

    # floor
    floor_x_pos -= 1
    fraw_floor()
    if floor_x_pos <= -SCREEN_WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)