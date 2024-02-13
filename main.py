import pygame
from math import sin, cos, pi, sqrt

# start game and game clock
pygame.init()
clock = pygame.time.Clock()

# storage for utilities that don't have a specific place to go
class utilities:
    def __init__(self):
        pass

    def tr(self, degrees):
        return degrees * pi / 180

utils = utilities()

# storage for game data
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

# storage for player data
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

#  intitialize game and player classes
game = Game(True, 60, (1280, 720), 0)
player = Player(game.displaysize, pygame.Vector2(0, 0), 0.0, [70, 14])

#  logging
print(player.dv)
print(player.speeds)
print(game.dt)

while game.running:
    # poll for events and handle window closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    #print(player.velocity)

    # fill the screen with a color to wipe away anything from last frame
    game.screen.fill("black")

    # draw player
    pygame.draw.circle(game.screen, "red", player.pos, 40)

    #  draw aim arrow
    pygame.draw.polygon(game.screen, "red", [
        #  draw front of direction arrow
        ( ((((sin(utils.tr(player.direction))+player.pos.x)-player.pos.x)*(-60))+player.pos.x),
          ((((cos(utils.tr(player.direction))+player.pos.y)-player.pos.y)*(-60))+player.pos.y)),

        #  draw left point of arrow
        ( ((((sin(utils.tr(player.direction-6))+player.pos.x)-player.pos.x)*(-47))+player.pos.x),
           ((((cos(utils.tr(player.direction-6))+player.pos.y)-player.pos.y)*(-47))+player.pos.y) ),

        #  draw middle point of arrow
        (((((sin(utils.tr(player.direction)) + player.pos.x) - player.pos.x) * (-50)) + player.pos.x),
         ((((cos(utils.tr(player.direction)) + player.pos.y) - player.pos.y) * (-50)) + player.pos.y)),

        #  draw right point of arrow
        (((((sin(utils.tr(player.direction+6))+player.pos.x)-player.pos.x)*(-47))+player.pos.x),
          ((((cos(utils.tr(player.direction+6))+player.pos.y)-player.pos.y)*(-47))+player.pos.y))])

    print( str((( round(((((sin(utils.tr(player.direction))+player.pos.x)-player.pos.x)*(-50))+player.pos.x), 2),
             round(((((cos(utils.tr(player.direction))+player.pos.y)-player.pos.y)*(-50))+player.pos.y), 2)),
           (0,0), (1,1))) + " " + str(round(sqrt((player.velocity.x**2+(player.velocity.y**2))), 2)))

    # apply friction
    if player.velocity.magnitude() != 0:
        player.velocity *= game.friction

    #  change player position
    player.pos.x += player.velocity.x
    player.pos.y += player.velocity.y

    #  fully stop momentum if very slow
    if player.velocity.magnitude() < game.autostop_threshold:
        player.velocity = pygame.Vector2(0, 0)

    # wrap player around screen
    player.pos.x = player.pos.x % game.displaysize.x
    player.pos.y = player.pos.y % game.displaysize.y

    # poll for pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        # accelerate player
        player.velocity.x -= player.speeds[0] * player.dv.x / 100
        player.velocity.y -= player.speeds[0] * player.dv.y / 100
    if keys[pygame.K_s]:
        # slow down player
        player.velocity.x += player.speeds[1] * player.dv.x / 100
        player.velocity.y += player.speeds[1] * player.dv.y / 100
    if keys[pygame.K_a]:
        # rotate left
        player.direction += 4
    if keys[pygame.K_d]:
        # rotate right
        player.direction -= 4
    if keys[pygame.K_LEFT]:
        pass
        #endpt =
        #pygame.draw.line(game.screen, "red", player.pos,)
    # draw debug velocity vector line
    pygame.draw.line(game.screen, "green", player.pos,
                     (player.pos.x+(3*player.velocity.x), player.pos.y+(3*player.velocity.y)))

    # fix player.dir
    player.recalc_dir(player.direction)

    # flips the display
    game.update()

    # limit fps
    game.dt = clock.tick(60) / 1000

# exit game
pygame.quit()