from math import sqrt
import cv2
from keyboard import is_pressed
from numpy import array
from pyautogui import click
from PIL import ImageGrab
from time import sleep

gameCords = [182, 349, 776, 764]
chalBtn = [350, 500]
prev_click = [[294, 205]]
startBtn = [645, 755]


def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def startGame():
    # starts the game 350, 500 is cords of chalenge button
    click(chalBtn)
    sleep(.2)


startGame()
run = True
while run:
    sleep(.05)
    ret, thresh = cv2.threshold(cv2.cvtColor(array(ImageGrab.grab(bbox=gameCords)), cv2.COLOR_RGB2GRAY), 150,
                                255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if is_pressed('q'):
            run = False
        M = cv2.moments(c)
        try:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
        except ZeroDivisionError:
            sleep(.2)

        goAway = False
        for pos in prev_click:
            if distance(cx, cy, pos[0], pos[1]) < 4:
                goAway = True
                break
        if goAway:
            continue
        click(gameCords[0] + cx, gameCords[1] + cy)
        prev_click.append([cx, cy])

        if len(prev_click) > 13:
            del prev_click[1]

    if is_pressed('q'):
        break
