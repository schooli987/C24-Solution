import pygame
import pygame
import pymunk
import pymunk.pygame_util

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
score = 0
attempts = 3

# Pymunk Space Setup
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Load Images
bird_image = pygame.image.load('bird.png')
background_image = pygame.image.load('background.jpg')
brick_image = pygame.image.load('wood1.png')
pig_image = pygame.image.load('pig.png')
# Resize Images
background_image = pygame.transform.scale(background_image, (800, 600))
bird_image = pygame.transform.scale(bird_image, (40, 40))
brick_image = pygame.transform.scale(brick_image, (60, 60))
pig_image = pygame.transform.scale(pig_image, (40, 40))

# Ground

ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, 580), (800, 580), 5)
ground_shape.friction = 0.5
space.add(ground_body, ground_shape)

# Create Bird
def create_bird(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = x, y
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 0.8
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

bird_body, bird_shape = create_bird(150, 500)

# Create Block
def create_block(x, y):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (60, 60)))
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (60, 60))
    shape.elasticity = 0.4
    shape.friction = 0.6
    space.add(body, shape)
    return body, shape

blocks = [create_block(600, 520), create_block(660, 520), create_block(720, 520), create_block(660, 480), create_block(690, 480), create_block(680, 440)]

# Create Pigs
def create_pigs(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = x, y
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 0.4
    shape.friction = 0.6
    space.add(body, shape)
    return body, shape

pigs = [create_pigs(650, 520), create_pigs(710, 520), create_pigs(670, 480)]
# Draw function
def draw_objects():
    
    screen.blit(background_image, (0, 0))  # Draw Background

    # Draw Bird
    bird_pos = bird_body.position
    screen.blit(bird_image, (bird_pos.x - 20, bird_pos.y - 20))

    # Draw Blocks with rotation
    for body, shape in blocks:
        block_pos = body.position
        angle = body.angle * (180 / 3.14159)
        rotated_brick = pygame.transform.rotate(brick_image, angle)
        rect = rotated_brick.get_rect(center=(block_pos.x, block_pos.y))
        screen.blit(rotated_brick, rect.topleft)

    for body, shape in pigs:
        global score
        pig_pos = body.position
        if pig_pos.x > 800:
            pigs.remove((body, shape))
            space.remove(body, shape)
            score+=1000
        else:
            screen.blit(pig_image, (pig_pos.x - 20, pig_pos.y - 20))

    # Draw Score and Attempts
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    attempts_text = font.render(f"Attempts: {attempts}", True, (0, 0, 0))
    screen.blit(attempts_text, (10, 50))


# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and attempts>0:
            mouse_pos = pygame.mouse.get_pos()
            bird_body.position = 150, 500
            bird_body.velocity = ((mouse_pos[0] - 150) * 4, (mouse_pos[1] - 500) * 4)
            attempts-=1
           

    space.step(1 / 60.0)
    draw_objects()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
