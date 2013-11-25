# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import math
import random

# initialize global variables used in your code

counter = 0
magic_number = 0
low = 0
high = 100

# helper function to start and restart the game
def new_game():
    
    global magic_number
    global counter

    print "New game. Range is from",low,"to",high
    
    magic_number = random.randrange(low,high)
    #print "Magic Number:", magic_number
    
    counter = int(math.ceil(math.log(high-low, 2)))
    print "Number of remaining guesses is",counter,"\n"

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global low
    global high
    
    low = 0
    high = 100
    new_game()
    

def range1000():
    # button that changes range to range [0,1000) and restarts
    global low
    global high
    
    low = 0
    high = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global counter
    global magic_number
        
    print "Guess was", guess   
        
    counter = counter - 1
    print "Number of remaining guesses is",counter

    if magic_number > int(guess):
        print "Higher!\n"
        flag = 0
    elif magic_number < int(guess):
        print "Lower!\n"
        flag = 0
    else:
        print "Correct! You Win!!\n"
        flag = 1
        new_game()

    if flag == 0 and counter == 0:
        print "GameOver! You Lose!!"
        print "Number is",magic_number,"\n"
        new_game()

  
def draw(canvas):
    canvas.draw_text("Guess the number", [0,100], 28, "Red")

    
# create frame
my_frame = simplegui.create_frame("Guess The Number", 200,200)
my_frame.set_canvas_background("cyan")
my_frame.set_draw_handler(draw)

# register event handlers for control elements
my_frame.add_button("Range is [0,100]", range100, 150)
my_frame.add_button("Range is [0,1000]", range1000, 150)
my_frame.add_input("Enter a guess",input_guess, 150)

# call new_game and start frame
my_frame.start()
new_game()
