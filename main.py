import pygame
from math import sin, cos, pi, sqrt

pygame.init()
clock = pygame.time.Clock()

class utilities:
    def __init__(self):
        pass

    def tr(self, degrees):
        return degrees * pi / 180

utils = utilities()


class Game:
    running = False
    screen = None
    framerate = None
    displaysize = None  # no losses with looking up screen size
    dt = None
    friction = .99
    autostop_threshold = 0.25

    def __init__(self, Running: bool = True, fps: int = 60, screensize: tuple = (1280, 720), dt: int = 0):
        self.framerate = fps
        self.running = Running
        self.displaysize = pygame.Vector2(screensize)
        self.dt = dt
        self.screen = pygame.display.set_mode(screensize)

    def update(self):
        pygame.display.flip()


class Player:
    pos = None
    velocity = None
    direction = None
    speeds = None
    dv = None

    def __init__(self, startpos: tuple, velocity: pygame.Vector2 = (0, 0), direction: float = 0.0, speeds = []):
        self.pos = pygame.Vector2(startpos[0] / 2, startpos[1] / 2)
        self.velocity = velocity
        self.direction = direction
        self.dv = pygame.Vector2(sin(utils.tr(direction)), cos(utils.tr(direction)))
        self.speeds = speeds

    def recalc_dir(self, dir):
        self.dv = pygame.Vector2(sin(utils.tr(dir)), cos(utils.tr(dir)))


game = Game(True, 60, (1280, 720), 0)
player = Player(game.displaysize, pygame.Vector2(0, 0), 0.0, [70, 14])

print(player.dv)
print(player.speeds)
print(game.dt)

while game.running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    #print(player.velocity)

    # fill the screen with a color to wipe away anything from last frame
    game.screen.fill("black")

    pygame.draw.circle(game.screen, "red", player.pos, 40)

    #  draw aim arrow
    pygame.draw.polygon(game.screen, "red", [
        ( ((((sin(utils.tr(player.direction))+player.pos.x)-player.pos.x)*(-60))+player.pos.x),
          ((((cos(utils.tr(player.direction))+player.pos.y)-player.pos.y)*(-60))+player.pos.y)),

        ( ((((sin(utils.tr(player.direction-6))+player.pos.x)-player.pos.x)*(-47))+player.pos.x),
           ((((cos(utils.tr(player.direction-6))+player.pos.y)-player.pos.y)*(-47))+player.pos.y) ),

        (((((sin(utils.tr(player.direction)) + player.pos.x) - player.pos.x) * (-50)) + player.pos.x),
         ((((cos(utils.tr(player.direction)) + player.pos.y) - player.pos.y) * (-50)) + player.pos.y)),

        (((((sin(utils.tr(player.direction+6))+player.pos.x)-player.pos.x)*(-47))+player.pos.x),
          ((((cos(utils.tr(player.direction+6))+player.pos.y)-player.pos.y)*(-47))+player.pos.y))])

    print( str((( round(((((sin(utils.tr(player.direction))+player.pos.x)-player.pos.x)*(-50))+player.pos.x), 2),
             round(((((cos(utils.tr(player.direction))+player.pos.y)-player.pos.y)*(-50))+player.pos.y), 2)),
           (0,0), (1,1))) + " " + str(round(sqrt((player.velocity.x**2+(player.velocity.y**2))), 2)))

    player.pos.x += player.velocity.x
    player.pos.y += player.velocity.y

    if player.velocity.magnitude() != 0:
        player.velocity *= game.friction

    if player.velocity.magnitude() < game.autostop_threshold:
        player.velocity = pygame.Vector2(0, 0)


    player.pos.x = player.pos.x % game.displaysize.x
    player.pos.y = player.pos.y % game.displaysize.y

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.velocity.x -= player.speeds[0] * player.dv.x / 100
        player.velocity.y -= player.speeds[0] * player.dv.y / 100
    if keys[pygame.K_s]:
        player.velocity.x += player.speeds[1] * player.dv.x / 100
        player.velocity.y += player.speeds[1] * player.dv.y / 100
    if keys[pygame.K_a]:
        player.direction += 4
    if keys[pygame.K_d]:
        player.direction -= 4
    player.recalc_dir(player.direction)

    # flip() the display to put your work on screen
    game.update()

    game.dt = clock.tick(60) / 1000  # limits FPS to 60

pygame.quit()
