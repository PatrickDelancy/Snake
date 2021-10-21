import turtle
import random
from typing import List, Tuple
import settings

gameBoard: turtle.Turtle = None

barriers: List[turtle.Turtle] = []
snake_segments: List[turtle.Turtle] = []
food: List[Tuple[str, turtle.Turtle]] = []

def getItemAtPosition(x, y) -> Tuple[str, turtle.Turtle]:
    if (x <= settings.minx or x >= settings.maxx or y <= settings.miny or y >= settings.maxy):
        return ("wall", gameBoard)

    for obj in barriers:
        if (obj.xcor() == x and obj.ycor() == y):
            return ("barrier", obj)

    for obj in snake_segments:
        if (obj.xcor() == x and obj.ycor() == y):
            return ("snake", obj)

    for obj in food:
        if (obj[1].xcor() == x and obj[1].ycor() == y):
            return obj

    return None

def getRandomOpenPosition():
    # start outside boundaries -- first loop iteration

    for i in range(100):
        x = random.randint(settings.minx / settings.segment_size, settings.maxx / settings.segment_size) * settings.segment_size
        y = random.randint(settings.miny / settings.segment_size, settings.maxy / settings.segment_size) * settings.segment_size
        if (None == getItemAtPosition(x,y)):
            return (x, y)
    
    return None

def createBarrierTurtle():
    barrier = turtle.Turtle()
    barrier.penup()
    barrier.shape("square")
    barrier.color("black")
    barrier.turtlesize(settings.segment_size / 20)
    return barrier

def drawGameBoard():
    global gameBoard

    screen = turtle.Screen()
    screen.tracer(False)

    if (gameBoard == None):
        gameBoard = turtle.Turtle()
    else:
        gameBoard.reset()
    
    gameBoard.speed(0)
    gameBoard.pensize(settings.segment_size)
    gameBoard.turtlesize(settings.segment_size / 20)
    gameBoard.shape("square")
    gameBoard.penup()
    gameBoard.goto(settings.minx, settings.miny)
    gameBoard.pendown()
    gameBoard.goto(settings.minx, settings.maxy)
    gameBoard.goto(settings.maxx, settings.maxy)
    gameBoard.goto(settings.maxx, settings.miny)
    gameBoard.goto(settings.minx, settings.miny)
    screen.tracer(True)

    for i in range(0, 3 + (2 * settings.difficulty)):
        addBarrier()

def addBarrier():
    screen = turtle.Screen()
    screen.tracer(False)
    pos = getRandomOpenPosition()

    barrier = createBarrierTurtle()
    barrier.goto(pos[0], pos[1])

    screen.tracer(True)
    barriers.append(barrier)

def setDifficulty(difficulty: int = 1):
    settings.difficulty = difficulty

def init():
    drawGameBoard()
