#imports
import turtle
import random

import board
import settings

# current direction of the snake
direction = 0
current_head = 0
current_tail = 0

def found_food(x, y):
  #TODO - find out if we are colliding with some food on the screen somehow
  if(random.randint(1,10) == 5):
    return True
  return False

def calc_new_position(x, y):
  if (direction) == 0:
    return x+settings.segment_size, y
  if (direction) == 90:
    return x, y+settings.segment_size
  if (direction) == 180:
    return x-settings.segment_size, y
  return x, y-settings.segment_size

def move_snake():
  global current_tail, current_head
  new_x, new_y = calc_new_position(board.snake_segments[current_head].xcor(), board.snake_segments[current_head].ycor())

  item_in_target_position = board.getItemAtPosition(new_x, new_y)

  if (item_in_target_position == None):
    print("Nothing in target space, moving snake...")
  elif (item_in_target_position[0] == "normal_food"):
    print("Found food, growing snake...")
    new_segment = turtle.Turtle(shape="circle", visible=False)
    new_segment.color("green")
    new_segment.penup()
    new_segment.hideturtle()
    new_segment.goto(board.snake_segments[current_tail].xcor(), board.snake_segments[current_tail].ycor())
    new_segment.showturtle()
    board.snake_segments.insert(current_tail, new_segment)
    current_tail += 1
  elif (item_in_target_position[0] == "bad_food"):
    board.addBarrier()
  else: # anything else is a barrier or wall
    print("Hit a barrier or wall... game over!")

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
  board.init()

  for i in range(3):
    food = turtle.Turtle();
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

  turtle.Screen().ontimer(move_snake, settings.move_interval)

# function to set the global direction variable
def setheading(new_direction):
  global direction
  direction = new_direction

# event handlers for changing direction
def go_up():
  setheading(90)
def go_down():
  setheading(270)
def go_left():
  setheading(180)
def go_right():
  setheading(0)

start_game()

wn = turtle.Screen()
wn.onkeypress(go_up, 'Up')
wn.onkeypress(go_down, 'Down')
wn.onkeypress(go_left, 'Left')
wn.onkeypress(go_right, 'Right')
wn.listen()

wn.mainloop()
