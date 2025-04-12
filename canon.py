import pygame
import pymunk
import pymunk.pygame_util

# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
score = 0
attempts = 5
game_over = False
game_won = False
cannonball_visible = False

# Pymunk Space Setup
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

pygame.mixer.init()

# Load Sound Effects
win_sound = pygame.mixer.Sound('win.mp3')
lose_sound = pygame.mixer.Sound('lose.mp3')
launch_sound = pygame.mixer.Sound('shoot.mp3')
hit_sound = pygame.mixer.Sound('brick_hit.mp3')
# Load Images
cannon_image = pygame.image.load('canon.png')
cannon_ball_image = pygame.image.load('cannon_ball.png')
brick_image = pygame.image.load('bricks.png')
background_image = pygame.image.load('bg4.jpg')

# Resize Images
background_image = pygame.transform.scale(background_image, (800, 600))
cannon_ball_image = pygame.transform.scale(cannon_ball_image, (50, 50))
cannon_image = pygame.transform.scale(cannon_image, (200, 200))
brick_image = pygame.transform.scale(brick_image, (60, 60))

pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")  # Your file name here
pygame.mixer.music.set_volume(0.2)               # Optional: volume (0.0 to 1.0)
pygame.mixer.music.play(-1)                      # Loop music indefinitely

# Flat Ground (fixed)
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, 580), (800, 580), 5)
ground_shape.friction = 1
space.add(ground_body, ground_shape)

# Create Cannonball (Initially Hidden)
cannonball_body = None
cannonball_shape = None

# Create Cannon
def create_cannon(x, y):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (60, 60))
    space.add(body, shape)
    return body, shape

cannon_body, cannon_shape = create_cannon(10, 500)

# Create Block
def create_block(x, y):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (60, 60)))
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (60, 60))
    shape.elasticity = 0.4
    shape.friction = 0.6
    shape.collision_type = 2
    space.add(body, shape)
    return body, shape

# Create stacked blocks (fixed positions)
blocks = [
    create_block(540, 520), create_block(600, 520), create_block(660, 520),create_block(720, 520),create_block(780, 520),
    create_block(600, 460), create_block(660, 460), create_block(720, 460),
    create_block(630, 400), create_block(690, 400),
    create_block(660, 340)
]


# Create Cannonball
def create_cannonball(x, y):
    global cannonball_body, cannonball_shape, cannonball_visible
    if cannonball_body:
        space.remove(cannonball_body, cannonball_shape)
    cannonball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    cannonball_body.position = x, y
    cannonball_shape = pymunk.Circle(cannonball_body, 20)
    cannonball_shape.elasticity = 0.2
    cannonball_shape.friction = 0.2
    cannonball_shape.collision_type = 1
    space.add(cannonball_body, cannonball_shape)
    cannonball_visible = True

# Draw everything
def draw_objects():
    global game_over, game_won
    screen.blit(background_image, (0, 0))

    if len(blocks) == 0 and not game_over:
        win_sound.play()
        game_won = True
        font = pygame.font.SysFont(None, 72)
        win_text = font.render("YOU WON!", True, (0, 255, 0))
        screen.blit(win_text, (320, 250))
        return

    if game_over and not game_won:
        lose_sound.play()
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("YOU LOST", True, (0, 0, 255))
        screen.blit(game_over_text, (300, 250))
        return

    # Cannonball
    if cannonball_visible and cannonball_body:
        pos = cannonball_body.position
        screen.blit(cannon_ball_image, (pos.x - 25, pos.y - 25))

    # Cannon
    pos = cannon_body.position
    screen.blit(cannon_image, (pos.x - 20, pos.y - 20))

    # Blocks
    for body, shape in blocks:
        pos = body.position
        angle = body.angle * (180 / 3.14159)
        rotated = pygame.transform.rotate(brick_image, angle)
        rect = rotated.get_rect(center=(pos.x, pos.y))
        if pos.x > 800:
          hit_sound.play()
          blocks.remove((body, shape))
          space.remove(body, shape)
        else:
            screen.blit(rotated, rect.topleft)

    # Score + Attempts
    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Attempts: {attempts}", True, (0, 0, 0)), (10, 50))

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and attempts > 0 and not game_over and not game_won:
            mouse_pos = pygame.mouse.get_pos()
            create_cannonball(150, 500)
            cannonball_body.velocity = ((mouse_pos[0] - 150) * 4, (mouse_pos[1] - 500) * 4)
            attempts -= 1
            launch_sound.play()
            if attempts == 0 and len(blocks) > 0:
                game_over = True
                pygame.mixer.music.stop()
    space.step(1 / 60.0)
    
    draw_objects()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
