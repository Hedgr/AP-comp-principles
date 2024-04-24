import pygame
from math import sin, cos, pi
from time import time

# initialize pygame and the clock
pygame.init()
clock = pygame.time.Clock()


class utilities:
    def __init__(self):
        # nothing to initialize
        pass

    def tr(self, degrees):
        # simple function to convert between radians and degrees or the other way around
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
    current_frame = 0
    projectiles = []
    asteroids = []

    # set up game, with default values set
    def __init__(self, Running: bool = True, fps: int = 60, screensize: tuple = (1280, 720), dt: int = 0):
        self.framerate = fps
        self.running = Running
        self.displaysize = pygame.Vector2(screensize)
        self.dt = dt
        self.screen = pygame.display.set_mode(screensize)

    # call function to update screen for final operations
    def update(self):
        pygame.display.flip()
        game.current_frame += 1


class Player:
    pos = None
    velocity = None
    direction = None
    speeds = None
    direction_vector = None
    testbuffer = [[0, 0]]
    lastshot = 0

    # init with default values
    def __init__(self, startpos: tuple, velocity: pygame.Vector2 = (0, 0), direction: float = 0.0, speeds=[]):
        self.position = pygame.Vector2(startpos[0] / 2, startpos[1] / 2)
        self.velocity = velocity
        self.direction = direction
        self.direction_vector = pygame.Vector2(sin(utils.tr(direction)), cos(utils.tr(direction)))
        self.speeds = speeds
        self.lastshot = time()

    # updates self.direction_vector after changing the direction
    def recalc_dir(self, dir):
        self.direction_vector = pygame.Vector2(sin(utils.tr(dir)), cos(utils.tr(dir)))

    # calculates a point using an angle and a distance based off the players current position
    def calculate_point_on_circle(self, angle, distance):
        # ((((sin(utils.tr(player.direction)) + player.position.x) - player.position.x) * -60) + player.position.x),
        #      ((((cos(utils.tr(player.direction))+player.position.y)-player.position.y)*(-60))+player.position.y))
        to_ret = (
            ((((sin(utils.tr(
                player.direction - angle)) + player.position.x) - player.position.x) * -distance) + player.position.x),
            ((((cos(utils.tr(player.direction - angle)) + player.position.y) - player.position.y) * (
                -distance)) + player.position.y)
        )
        return to_ret


class projectile:
    position = None
    def __init__(self, spawnpoint, direction_vector, speed):
        self.spawnpoint = spawnpoint
        self.position = spawnpoint
        self.direction_vector = direction_vector
        self.speed = speed


game = Game(True, 60, (1280, 720), 0)
player = Player(game.displaysize, pygame.Vector2(0, 0), 0.0, [70, 14])

while game.running:

    # testing prints
    if game.current_frame % 5 == 0:
        print(player.direction_vector, " | ", player.position, " | ", player.velocity)

    # check if program closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    # print(player.velocity)

    # fill the screen with a color to wipe away anything from last frame
    game.screen.fill("black")

    pygame.draw.circle(game.screen, "red", player.position, 40)

    #  draw aim arrow
    # print("o: ", ((((sin(utils.tr(player.direction))+player.position.x)-player.position.x)*-60)+player.position.x),
    #      ((((cos(utils.tr(player.direction))+player.position.y)-player.position.y)*(-60))+player.position.y))
    # print("n: ", player.calculate_point_on_circle(0, 120))

    pygame.draw.polygon(game.screen, "red", [
        (player.calculate_point_on_circle(0, 60)),

        (player.calculate_point_on_circle(6, 47)),

        (player.calculate_point_on_circle(0, 50)),

        (player.calculate_point_on_circle(-6, 47))])

    # print( str((( round(((((sin(utils.tr(player.direction))+player.position.x)-player.position.x)*(-50))+player.position.x), 2),
    #         round(((((cos(utils.tr(player.direction))+player.position.y)-player.position.y)*(-50))+player.position.y), 2)),
    #       (0,0), (1,1))) + " " + str(round(sqrt((player.velocity.x**2+(player.velocity.y**2))), 2)))
    keys = pygame.key.get_pressed()

    player.position.x += player.velocity.x
    player.position.y += player.velocity.y

    if player.velocity.magnitude() != 0:
        player.velocity *= game.friction

    if player.velocity.magnitude() < game.autostop_threshold:
        player.velocity = pygame.Vector2(0, 0)

    player.position.x = player.position.x % game.displaysize.x
    player.position.y = player.position.y % game.displaysize.y

    if keys[pygame.K_w]:
        player.velocity.x -= player.speeds[0] * player.direction_vector.x / 250
        player.velocity.y -= player.speeds[0] * player.direction_vector.y / 250
    if keys[pygame.K_s]:
        player.velocity.x += player.speeds[1] * player.direction_vector.x / 100
        player.velocity.y += player.speeds[1] * player.direction_vector.y / 100
    if keys[pygame.K_a]:
        player.direction += 4
    if keys[pygame.K_d]:
        player.direction -= 4
    player.recalc_dir(player.direction)

    if pygame.mouse.get_pressed()[0] and (time() - player.lastshot > 0.1):
        player.lastshot = time()
        game.projectiles.append(projectile(player.calculate_point_on_circle(0, 50), player.direction_vector, 15))


    if len(game.projectiles) != 0:
        for i in range(len(game.projectiles)): #70
            game.projectiles[i].position = (game.projectiles[i].position[0] + (-game.projectiles[i].speed * game.projectiles[i].direction_vector[0]),
                                            game.projectiles[i].position[1] + (-game.projectiles[i].speed * game.projectiles[i].direction_vector[1]))
            pygame.draw.circle(game.screen, "yellow", game.projectiles[i].position, 5)

    # flip() the display to put your work on screen
    game.update()

    game.dt = clock.tick(60) / 1000  # limits FPS to 60

pygame.quit()
