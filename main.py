#imports
import turtle
import board
import settings

# current heading of the snake
heading = 0

# a counter to store how many "ticks" or the game occurred
ticks = 0

# difficulty level
difficulty = 1

# use indexes to keep track of the segment array element at head and tail of snake
current_head = 0
current_tail = 0

#running flag
running = True

#Turtle for information on the screen
marquee: turtle.Turtle() = None

def calc_new_position(x, y):
  if (heading) == 0:
    return x+settings.segment_size, y
  if (heading) == 90:
    return x, y+settings.segment_size
  if (heading) == 180:
    return x-settings.segment_size, y
  return x, y-settings.segment_size

def move_snake():
  global current_tail, current_head, ticks, difficulty
  if (running == False):
    return

  new_x, new_y = calc_new_position(board.snake_segments[current_head].xcor(), board.snake_segments[current_head].ycor())

  item_in_target_position = board.getItemAtPosition(new_x, new_y)
  wn.tracer(False)
  if (item_in_target_position == None):
    ticks += 1
  elif (item_in_target_position[0] == "normal_food"):
    # find new empty position and move the food to it
    new_food_x, new_food_y = board.getRandomOpenPosition() 
    item_in_target_position[1].goto(new_food_x, new_food_y)

    # add a new segment to the segment array
    new_segment = turtle.Turtle(shape="circle", visible=False)
    new_segment.color("green")
    new_segment.penup()
    new_segment.hideturtle()
    new_segment.goto(board.snake_segments[current_tail].xcor(), board.snake_segments[current_tail].ycor())
    new_segment.showturtle()
    board.snake_segments.insert(current_tail, new_segment)
    current_tail += 1 # move tail index down the array one
  elif (item_in_target_position[0] == "bad_food"):
    board.addBarrier()
  else: # anything else is a barrier or wall
    board.gameOver(item_in_target_position[0], len(board.snake_segments))
    difficulty_keys_on()
    return

  # move the tail to the head
  board.snake_segments[current_tail].hideturtle()
  board.snake_segments[current_tail].goto(new_x, new_y)
  board.snake_segments[current_tail].showturtle()
  wn.tracer(True)

  # re-set the index arrays to the head and tail segments
  current_head = current_tail
  if (current_tail == 0):
    current_tail = len(board.snake_segments) - 1
  else:
    current_tail -= 1

  # reset the timer event to fire  
  turtle.Screen().ontimer(move_snake, settings.move_interval[difficulty-1])

# game initialization
def start_game(difficulty_selected):
  global heading, current_head, current_tail, running, difficulty

  difficulty = difficulty_selected
  difficulty_keys_off() # unhook the number key press events

  board.clear()

  # hook up all the movement keys and the pause (space)
  wn.onkeypress(pause, 'space')
  wn.onkeypress(go_up, 'Up')
  wn.onkeypress(go_down, 'Down')
  wn.onkeypress(go_left, 'Left')
  wn.onkeypress(go_right, 'Right')

  wn.tracer(False)

  heading = 0
  current_head = 0
  current_tail = 0
  running = True

  board.init()
  for i in range(3): # create 3 "good" food
    food = turtle.Turtle()
    food.shape("turtle")
    food.color("blue")
    food.penup()
    pos = board.getRandomOpenPosition()
    food.goto(pos[0], pos[1])
    board.food.append(("normal_food", food))

  for i in range(2): # create 2 "bad" food
    food = turtle.Turtle()
    food.shape("turtle")
    food.color("red")
    food.penup()
    pos = board.getRandomOpenPosition()
    food.goto(pos[0], pos[1])
    board.food.append(("bad_food", food))

  # start the segment array with the first element
  new_segment = turtle.Turtle(shape="circle")
  new_segment.color("green")
  new_segment.goto(0, 0)
  new_segment.penup()
  board.snake_segments.append(new_segment)
  wn.tracer(True)

  # start the game timer
  turtle.Screen().ontimer(move_snake, settings.move_interval[difficulty-1])

# function to set the global direction variable
def setheading(new_heading):
  global heading
  heading = new_heading

# event handlers for changing direction
def go_up():
  if (heading != 270):
    setheading(90)
def go_down():
  if (heading != 90):
    setheading(270)
def go_left():
  if (heading != 0):
    setheading(180)
def go_right():
  if (heading != 180 ):
    setheading(0)
def pause():
  global running, marquee
  if (marquee == None): # if the marquee has never been initialized
    marquee = turtle.Turtle()
    marquee.color("Blue")
    marquee.hideturtle()
    marquee.penup()
    marquee.goto(0,0)

  if (running): # set to paused
    running = False
    marquee.write("Paused", align="center", font=("Arial", 74, "bold"))
  else: # set to running
    marquee.clear() # remove the "Paused" text
    running = True
    # need to restart the timer
    turtle.Screen().ontimer(move_snake, settings.move_interval[difficulty-1])

def difficulty_1():
  start_game(1)
def difficulty_2():
  start_game(2)
def difficulty_3():
  start_game(3)
def difficulty_4():
  start_game(5)
def difficulty_5():
  start_game(5)

def difficulty_keys_on():
  wn.onkeypress(difficulty_1, '1')
  wn.onkeypress(difficulty_2, '2')
  wn.onkeypress(difficulty_3, '3')
  wn.onkeypress(difficulty_4, '4')
  wn.onkeypress(difficulty_5, '5')

def difficulty_keys_off():
  wn.onkeypress(None, '1')
  wn.onkeypress(None, '2')
  wn.onkeypress(None, '3')
  wn.onkeypress(None, '4')
  wn.onkeypress(None, '5')

board.writeMessage('Press a number 1-5 to select difficulty\nlevel and start the game.')

wn = turtle.Screen()
difficulty_keys_on()
wn.listen()
wn.mainloop()
