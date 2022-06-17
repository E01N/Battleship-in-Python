import random
import time
import sys
import os

"""
Legend:
1. "." = water or empty space 
2. "0" = part of a ship 
3. "X" = part of a ship that was hit
3. "#" = water that was hit with no ship

"""

# grid 
grid = [[]]
# grid size
grid_size = 10
# number of ships 
num_of_ships = 5
# bullets left
bullets_left = 50
# game over
game_over = False
# number of ships sunk 
num_of_ships_sunk = 0
# ship position on grid
ship_positions = [[]]
# global variable for alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Variable for debug mode turn to True to show ships
debug_mode = False

def validate_grid_and_place_ship(start_row, end_row, start_col, end_col):
    """ Will check row and column to see if it is a valid area to place ship
        return True or False. """
    global grid
    global ship_positions

    all_valid = True
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] != ".":
                all_valid = False
                break
    if all_valid:
        ship_positions.append([start_row, end_row, start_col, end_col])
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                grid[r][c] = "0"
    return all_valid


def try_to_place_ship_on_grid(row, col, direction, length):
    """ Based on direction will call on help method to help ship placement. """
    global grid_size
  
    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
    if direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1
        
    elif direction == "right":
        if col + length >= grid_size:
            return False
        end_col = col + length
        
    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1

    elif direction == "down":
        if row + length >= grid_size:
            return False
        end_row = row + length
    
    return validate_grid_and_place_ship(start_row, end_row, start_col, end_col)


def create_grid():
    # Will create 10X10 grid and place ships at random
    global grid
    global grid_size
    global num_of_ships
    global ship_positions

    # if ran multiple times will give different values
    random.seed(time.time())

    rows, cols, = (grid_size, grid_size)

    # create 2D arrey
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
        grid.append(row)

    num_of_ships_placed = 0

    ship_positions = [] 

    # create random positions for ships on grid
    while num_of_ships_placed != num_of_ships:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)
        if try_to_place_ship_on_grid(random_row, random_col, direction, ship_size):
            num_of_ships_placed += 1
            
            
def print_grid():
    """ Will print the grid rows A-J and columns 0-9. """
    global grid 
    global alphabet

    alphabet = alphabet[0: len(grid) + 1]

    for row in range(len(grid)):
        # print out our row A-J
        print(alphabet[row], end=")")
        for col in range(len(grid[row])):
            if grid[row][col] == "0":
                if debug_mode:
                    print("0", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(grid[row][col], end=" ")
        print("")

    # print our column 0-9
    print(" ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")


def accept_valid_bullet_placement():
    """ Will get valid position to place users shot. """
    global alphabet
    global grid

    is_valid_placement = False
    row = -1
    col = -1
    while is_valid_placement is False:
        # user gets prompt to enter area on grid
        placement = input("Enter row (A-J) and column (0-9) such as B5: ")
        placement = placement.upper()
        if len(placement) <= 0 or len(placement) > 2:
            # if entered incorrectly user will get error message
            print("Error: Please enter only one row and column such as B5")
            continue
        row = placement[0]
        col = placement[1]
        if not row.isalpha() or not col.isnumeric():
            # if entered incorrectly user will get error message
            print("Error: Please enter letter (A-J) for row and (0-9) for column")
            continue
        row = alphabet.find(row)
        if not (-1 < row < grid_size):
            # if entered incorrectly user will get error message
            print("Error: Please enter letter (A-J) for row and (0-9) for column")
            continue
        col = int(col)
        if not (-1 < col < grid_size):
            # if entered incorrectly user will get error message
            print("Error: Please enter letter (A-J) for row and (0-9) for column")
            continue
        if grid[row][col] == "#" or grid[row][col] == "X":
            # if user repeates a choice an error message will show
            print("You have already attacked here")
            continue
        if grid[row][col] == "." or grid[row][col] == "0":
            is_valid_placement = True

    return row, col


def check_for_ship_sunk(row, col):
    """ If all parts of the ship are hit, it is sunk and later increment ship sunk. """
    global ship_positions
    global grid

    for position in ship_positions:
        start_row = position[0]
        end_row = position[1]
        start_col = position[2]
        end_col = position[3]
        if start_row <= row <= end_row and start_col <= col <= end_col:
            # found ship now check if sunk
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if grid[r][c] != "X":
                        return False
    return True


def shoot_bullet():
    """ Updates grid and ships on where bullets have been shot. """
    global grid
    global num_of_ships_sunk
    global bullets_left

    row, col = accept_valid_bullet_placement()
    print("")
    print("----------------------------------")
    # missed shot
    if grid[row][col] == ".":
        print("You missed")
        grid[row][col] = "#"
    # ship hit
    elif grid[row][col] == "0":
        grid[row][col] = "X"
        # check if ship was sunk
        if check_for_ship_sunk(row, col):
            print("Ship sunk!")
            num_of_ships_sunk += 1
        else:
            print("You hit a ship")

    bullets_left -= 1


def check_for_game_over():
    """ If all ships are sunk or if user runs out of bullets it's Game Over. """
    global num_of_ships
    global num_of_ships_sunk
    global bullets_left
    global game_over
    # if num_of_ships equals num_of_ships_sunk the user wins
    if num_of_ships == num_of_ships_sunk:
        print("You Win!")
        game_over = True
    # if all of the bullets are gone the user looses
    elif bullets_left == 0:
        print("You are out of bullets, you loose")
        game_over = True


def main():
    """ Main entry of application which runs game loop. """
    global game_over

    print("----Welcome to Battleship!----")
    print(" You have 50 bullets to take down all of the ships")

    create_grid()

    while game_over is False:
        print_grid()
        print("Number of ships remaining: " + str(num_of_ships - num_of_ships_sunk))
        print("Number of bullets remaining: " + str(bullets_left))
        shoot_bullet()
        print("----------------------------------")
        check_for_game_over()

    while game_over is True:
        print("----------------------------------")
        print("Thank you for playing")
        break

if __name__ == '__main__':
    main()
