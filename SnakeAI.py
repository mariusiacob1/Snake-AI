# ************************************
# Python Snake
# ************************************
from tkinter import *
from search import *
import random
import math 

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 500
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([100, (100-50*i)])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):

        # x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        # y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [450, 450]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

class Astar(Problem):
    
    def __init__(self, initial, goal):
        super().__init__(initial, goal)
        
    
    def snake():
        body_size = BODY_PARTS
        coordinates = [[100, 100], [100, 50], [100, 0]]
        for i in range(0, body_size):
            coordinates.append([100, (100-50*i)])

    
        
    def goal_test(self,state):
        # did the snake get the fruit
         
        # below may be unnessecary if display and scoring handled outside of algo
        # x, y = state
        # if x == food.coordinates[0] and y == food.coordinates[1]:
        # # global score
        # # score += 1
        #     # label.config(text="Score:{}".format(score))
        #     canvas.delete("food")
        #     food = Food()
        print("gets to goal test")
        return state[0] == self.goal
    
    def result(self, state, action):
        # give the resulting square of going in any given direction
        print("gets to result checking")
        x, y = state[0] # state here is equal to the snake's coordinates

        if action == "up":
            y -= SPACE_SIZE
        elif action == "down":
            y += SPACE_SIZE
        elif action == "left":
            x -= SPACE_SIZE
        elif action == "right":
            x += SPACE_SIZE
            
        state.insert(0,x,y) # adds the next position the snake will head into the 
        del state[-1]
        print("gets to result checking")
        return state 
    
    def actions(self, state):
        # give three possible directions the snake could go, not including backwards.
        # also check for collision with existing snake body here, and do not provide that direction in that case
        print("gets to action list")
        possible_actions = ["up", "down", "left", "right"]
        
        x,y = state
       
        # remove abilty to go backwards
        if direction == 'right':
            possible_actions.remove("left")
    
        if direction == 'left':
            possible_actions.remove("right")
    
        if direction == 'down':
            possible_actions.remove("up")
    
        if direction == 'up':
            possible_actions.remove("down")
        
        # check for collision with self
        for i in possible_actions:
            for body_part in snake.coordinates[1:]:
                    if x == body_part[0] and y == body_part[1]:
                        possible_actions.remove(i)

        # check for collision with wall
        if x < 0:
            possible_actions.remove("left") 
        elif  x >= GAME_WIDTH:
            possible_actions.remove("right")
        if y < 0:
            possible_actions.remove("up")
        elif y >= GAME_HEIGHT:
            possible_actions.remove("down")


                
        return possible_actions
        
     
     
            
    
    
def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def check_distance(snake, food):
    food_coords = [food.coordinates[0], food.coordinates[1]]
    return math.dist(snake.coordinates[0], food_coords)

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")


window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()
print(snake.coordinates, " *********************")



next_turn(snake, food)
food_coords = (food.coordinates[0], food.coordinates[1])
print(food_coords)
ast = Astar(initial=[[100, 100], [100, 50], [100, 0]], goal=food_coords)
solution = breadth_first_graph_search(ast)
print(solution)
window.mainloop()