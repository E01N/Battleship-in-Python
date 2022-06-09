#Legend
# X for placing ship
# ' ' for available space
# '-' for missed shot

from random import randint

#board for holding ship locations
HIDDEN_BOARD = [[' '] * 8 for x in range(8)]
#board for displaying hits and misses
GUESS_BOARD = [[' '] * 8 for x in range(8)]


#prints board 8*8 with seperators between spaces
def print_board(board):
    print('  A B C D E F G H ')
    print('  ---------------')
    row_number = 1
    for row in board:
        print("%d|%s|" % (row_number, "|".join(row)))
        row_number += 1


#converts letters to coresponding number
letters_to_numbers = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}


# creates 5 random ships on board
def create_ships(board):
    for ship in range(5):
        ship_row, ship_column = randint(0,7), randint(0,7)
        while board[ship_row][ship_column] == 'X':
            ship_row, ship_column = randint(0,7), randint(0,7)
        board[ship_row][ship_column] = 'X'


# lets user choose what location on the board to hit
def get_ship_loctation():
    row = input('Please enter ship row 1-8 ')
    while row not in '12345678':
        print('Please enter a valid row')
        row = input('Please enter ship row 1-8 ')

    column = input('Please enter ship column A-H ').upper()
    while column not in 'ABCDEFGH':
        print('Please enter valid column')
        column = input('Please enter ship column A-H ').upper()
    return int(row) - 1, letters_to_numbers[column]


# counts hits for game score
def count_hit_ships(board):
    count = 0
    for row in board:
        for column in board:
            if column == 'X':
                count =+1
        return count

create_ships(HIDDEN_BOARD)
print_board(HIDDEN_BOARD)
turns = 10
while turns > 0:
    print('Welcome to Battleship')
    print_board(GUESS_BOARD)
    row, column = get_ship_loctation()   
if GUESS_BOARD[row][column] == '-':
    print('You have already guessed that')
elif HIDDEN_BOARD[row][column] == 'X':
    print('You have hit the battleship!')
    GUESS_BOARD[row][column] = 'X'
    turns -= 1
else:
    print('Sorry, you missed')
    GUESS_BOARD[row][column] = '-'
    turns -= 1 
if count_hit_ships(GUESS_BOARD) == 5:
    print('YOU WIN!')
    
print('You have' +str(turns) + 'turns remaining')
if turns == 0:
    print('GAME OVER')
    
