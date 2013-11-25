# Rock-paper-scissors-lizard-Spock template
import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions


def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "Number our of range."
        print "So the number is considered as", number % 4
        # Call the function number_to_name again with (number % 4)
        return number_to_name(number % 4)


def name_to_number(name):
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "Invalid name '" + name + "' received.",
        print "So considered it as 'rock'"
        # Call the function name_to_number again with rock 'rock'
        return name_to_number("rock")

    
def rpsls(name):
    # convert name to player_number using name_to_number
    print "Player chooses", name
    player_number = name_to_number(name)

    # compute random guess for comp_number using random.randrange()
    computer_number = random.randrange(0, 5)

    # convert comp_number to name using number_to_name
    computer_name = number_to_name(computer_number)
    print "Computer chooses", computer_name

    # compute difference of player_number and comp_number modulo five
    diff_number = ( player_number - computer_number ) % 5

    # use if/elif/else to determine winner
    if diff_number == 0:
        print "Player and computer tie!\n"
    elif diff_number > 2:
        print "Computer Wins!\n"
    else:
        print "Player Wins!\n"
    

# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
