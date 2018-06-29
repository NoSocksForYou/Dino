DINO_STRENGTH = 5
DINO_GRAVITY = 2
CACTUS_PROBABILITY = 1 # in percents per frame
CACTUS_SPAWN_GAIN = 0.0001
PTEROSAUR_PROBABILITY = 2
PTEROSAUR_SPAWN_GAIN = 0.0001
WINDOW_DIM_X = 229
WINDOW_DIM_Y = 52
CACTUS_MAX_SPEED = 4
CACTUS_MIN_SPEED = 2
FRAMERATE = 10000
SPEED_GAIN = 0.0001
DINO_COLLISION_LOGIC = False

import time
import random

from utils import ACoord, Logger
from sprite import Sprite
from dino import Dino
from cactus import Cactus
from ScreenPrinter import ScreenPrinter
from pterosaur import Pterosaur
from color import colors



printer = ScreenPrinter("background.txt", term_dim_x=WINDOW_DIM_X, term_dim_y=WINDOW_DIM_Y)
dino_spr = Sprite.fromFilePath("resources/dino/dino.txt")
cactus_spr = Sprite.fromFilePath("resources/cactus/cactus.txt")

printer.attachSprite(dino_spr)
dino = Dino(dino_spr,
            strength=DINO_STRENGTH,
            gravity=DINO_GRAVITY,
            pos_y=WINDOW_DIM_Y - 12,
            collision_logic=DINO_COLLISION_LOGIC,
            framerate=7)

cactus_sprites = []
cacti = []
pterosaurs = []

counter = 0
latest = 0

speed = 3

def makeCactus(screen_printer, path):
    cactus_sprites.append(Sprite.fromFilePath(path))
    screen_printer.attachSprite(cactus_sprites[-1])
    return Cactus(cactus_sprites[-1], speed=-5)

def makePterosaur(screen_printer, path):
    temp_sprite = Sprite.fromFilePath(path)
    screen_printer.attachSprite(temp_sprite)
    return Pterosaur(temp_sprite, speed=-5)


# cacti.append(makeCactus(printer, "resources/cactus/cactus.txt"))
# pterosaurs.append(makePterosaur(printer, "resources/pterosaur/pterosaur1.txt"))


while True:
    printer.commit()
    printer.updateSprites()

    cycle_beginning = time.time()



    if random.randint(0, 100) in list(range(int(CACTUS_PROBABILITY + counter * CACTUS_SPAWN_GAIN))) and latest > 50:
        cacti.append(makeCactus(printer, "resources/cactus/cactus.txt"))
        latest = -1

    if random.randint(0, 100) in list(range(int(PTEROSAUR_PROBABILITY + counter ** PTEROSAUR_SPAWN_GAIN))) and latest > 50 and counter > 1000:
        pterosaurs.append(makePterosaur(printer, "resources/pterosaur/pterosaur1.txt"))
        latest = -1

    # if latest >= 20:
    #     # pterosaurs.append(makePterosaur(printer, "resources/pterosaur/pterosaur1.txt"))
    #     cacti.append(makeCactus(printer, "resources/cactus/cactus.txt"))
    #
    #     latest = -1


    # speed = 10
    speed = int(8 + counter * SPEED_GAIN)
    Cactus.changeSpeed(speed)
    Pterosaur.changeSpeed(speed)

    # print(f"{colors.blackwhite} asd")


    counter += 1
    latest += 1

    #speed
    speed_string = f"Speed: {speed}"
    printer.putText(printer.term_dim_x - 20 - len(speed_string), 8, speed_string, color=colors.blackwhite)


    # Score
    scorestring = f"Score: {counter}"

    printer.putText(printer.term_dim_x - 5 - len(scorestring), 8, scorestring, color=colors.blackwhite)

    if dino.checkForCollisions():
        # printer.putText(12, 8, "Game over!")
        gameover = Sprite.fromFilePath("resources/misc/gameover.txt")
        printer.attachSprite(gameover)
        gameover.draw(40, 16)
        printer.commit()
        quit()

    cycle_end = time.time()
    cycle_time = cycle_end - cycle_beginning

    time.sleep(max(1 / FRAMERATE - cycle_time, 0))
