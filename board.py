import turtle
import random
from typing import List, Tuple
import settings

gameBoard: turtle.Turtle = None
gameMessage: turtle.Turtle = None

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

    if (gameBoard == None):
        gameBoard = turtle.Turtle()
        gameBoard.hideturtle()
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

    for i in range(0, 3 + (2 * settings.difficulty)):
        addBarrier()

def addBarrier():
    pos = getRandomOpenPosition()

    barrier = createBarrierTurtle()
    barrier.goto(pos[0], pos[1])

    barriers.append(barrier)

def clear():
    global snake_segments, barriers, gameBoard, gameMessage, food
    snake_segments = []
    barriers = []
    food = []

    gameBoard = None
    gameMessage = None

    turtle.clearscreen()

def gameOver(reason: str = None, score: int = 0):
    clear()
    if (reason == 'snake'):
        writeMessage("Snake doesn't taste very good.\nYour score = " + str(score))
    elif (reason == 'barrier'):
        writeMessage("You hit a wall. Time to re-think your\nlife choices. Your score = " + str(score))
    else:
        writeMessage("Game Over. Your score = " + str(score))

def writeMessage(message: str):
    global gameMessage
    if (gameMessage == None):
        gameMessage = turtle.Turtle()
        gameMessage.hideturtle()
        gameMessage.penup()
        gameMessage.write(arg=message, align="center", font=("Comic Sans", 30, "normal"))

def clearMessage():
    global gameMessage
    if (gameMessage != None):
        gameMessage.clear()

def setDifficulty(difficulty: int = 1):
    settings.difficulty = difficulty

def init():
    drawGameBoard()
    clearMessage()
