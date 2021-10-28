#imports
import turtle
import board
import settings

# current direction of the snake
heading = 0

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
  global current_tail, current_head, running
  if (running == False):
    return

  new_x, new_y = calc_new_position(board.snake_segments[current_head].xcor(), board.snake_segments[current_head].ycor())

  item_in_target_position = board.getItemAtPosition(new_x, new_y)

  if (item_in_target_position == None):
    print("Nothing in target space, moving snake...")
  elif (item_in_target_position[0] == "normal_food"):
    print("Found food, growing snake...")
    wn.tracer(False)

    new_food_x, new_food_y = board.getRandomOpenPosition()
    item_in_target_position[1].goto(new_food_x, new_food_y)
    new_segment = turtle.Turtle(shape="circle", visible=False)
    new_segment.color("green")
    new_segment.penup()
    new_segment.hideturtle()
    new_segment.goto(board.snake_segments[current_tail].xcor(), board.snake_segments[current_tail].ycor())
    new_segment.showturtle()
    board.snake_segments.insert(current_tail, new_segment)

    wn.tracer(True)
    current_tail += 1
  elif (item_in_target_position[0] == "bad_food"):
    board.addBarrier()
  else: # anything else is a barrier or wall
    print("Hit a barrier or wall... game over!")
    board.gameOver(item_in_target_position[0])
    wn.onkeypress(start_game, 'Return')
    return

  # move the tail to the head
  board.snake_segments[current_tail].hideturtle()
  board.snake_segments[current_tail].goto(new_x, new_y)
  board.snake_segments[current_tail].showturtle()

  #rest the index arrays to the head and tail segments
  current_head = current_tail
  if (current_tail == 0):
    current_tail = len(board.snake_segments) - 1
  else:
    current_tail -= 1

  # reset the timer event to fire  
  turtle.Screen().ontimer(move_snake, settings.move_interval)

# game initialization
def start_game():
  global heading, current_head, current_tail, running
  wn.onkeypress(None, 'Return')

  board.clear()

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
  for i in range(3):
    food = turtle.Turtle()
    food.shape("turtle")
    food.color("blue")
    food.penup()
    pos = board.getRandomOpenPosition()
    food.goto(pos[0], pos[1])
    board.food.append(("normal_food", food))

  for i in range(2):
    food = turtle.Turtle();
    food.shape("turtle")
    food.color("red")
    food.penup()
    pos = board.getRandomOpenPosition()
    food.goto(pos[0], pos[1])
    board.food.append(("bad_food", food))

  new_segment = turtle.Turtle(shape="circle")
  new_segment.color("green")
  new_segment.goto(0, 0)
  new_segment.penup()
  board.snake_segments.append(new_segment)
  wn.tracer(True)
  turtle.Screen().ontimer(move_snake, settings.move_interval)

# function to set the global direction variable
def setheading(new_heading):
  global heading
  heading = new_heading

# event handlers for changing direction
def go_up():
  global running
  if (heading != 270):
    setheading(90)
def go_down():
  global running
  if (heading != 90):
    setheading(270)
def go_left():
  global running
  if (heading != 0):
    setheading(180)
def go_right():
  global running
  if (heading != 180 ):
    setheading(0)
def pause():
  global running, marquee
  if (marquee == None):
    marquee = turtle.Turtle()
    marquee.color("Blue")
    marquee.hideturtle()
    marquee.penup()
    marquee.goto(-150,0)

  if (running):
    running = False
    marquee.write("Paused", font=("Arial", 74, "bold"))
  else:
    marquee.clear() # remove the "Paused" text
    running = True
    # need to restart the timer
    turtle.Screen().ontimer(move_snake, settings.move_interval)

wn = turtle.Screen()
wn.onkeypress(start_game, 'Return')
wn.listen()

board.writeMessage('Press "Enter" to start a new game.')

wn.mainloop()
