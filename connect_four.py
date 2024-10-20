"""
Game Name: Connect Four
Description: Get four in a row to win!
Author: Zachary Coe
Date: 2024-10-16
"""



import random
import argparse



DEFAULT_HEIGHT = 6
DEFAULT_WIDTH = 7
RED_CIRCLE = "\U0001f534"
YELLOW_CIRCLE = "\U0001F7E1"
# Length of longer line in instructions
SPACE_OVER = 44
COLUMN_WIDTH = 4
DOUBLE_DIGIT_INT = 10



class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def get_spacing(self):
        # Setting a space buffer to center the board on the instructions
        spacing = (SPACE_OVER - ((self.width * COLUMN_WIDTH) + 1)) // 2
        if spacing < 0:
            spacing = 0
        return spacing

    def print_default_board(self):
        spacing = self.get_spacing()
        
        for _ in range(self.height - 1):
            print(" " * spacing, end="")
            for _ in range(self.width):
                print("|   ", end="")
            print("|")

        # Prints last line ("underline")
        print(" " * spacing, end="")
        print("\033[4m|   \033[0m" * self.width, end="\033[4m|\033[0m\n")
        print(" " * spacing, end=" ")
        if self.width <= 9:
            for num in range(1, self.width + 1):
                print(f"[{num}]", end=" ")
        else:
            for num in range(1, DOUBLE_DIGIT_INT):
                print(f"[{num}]", end=" ")
            for num in range(DOUBLE_DIGIT_INT, self.width + 1):
                print(f"[{num}]", end="")
        # Give space for next line
        print("\n")

    def print_board_sizes(self):
        if self.height != DEFAULT_HEIGHT or self.width != DEFAULT_WIDTH:
            if self.width >= DOUBLE_DIGIT_INT:
                string_length = len(f"Starting the game with a board of {self.height}x{self.width}")
                spacing = (((self.width * COLUMN_WIDTH) + 1) - string_length) // 2
                print(" " * spacing, end=f"Starting the game with a board of {self.height}x{self.width}\n")
            else:
                print(f"Starting the game with a board of {self.height}x{self.width}")

class Player:
     pass

class Game:
    instructions = """\n  Type the column number you want to drop
your piece into. Get 4 in a row and you win!\n"""

    def __init__(self, height, width):
        self.board = Board(height, width)

    def print_instructions(self):
        if self.board.width > DOUBLE_DIGIT_INT:
            first_string_length = len("Type the column number you want to drop")
            second_string_length = len("your piece into. Get 4 in a row and you win!")
            first_spacing = (((self.board.width * COLUMN_WIDTH) + 1) - first_string_length) // 2
            second_spacing = (((self.board.width * COLUMN_WIDTH) + 1) - second_string_length) // 2
            print("\n" + (" " * first_spacing) + "Type the column number you want to drop")
            print((" " * second_spacing) + "your piece into. Get 4 in a row and you win!\n")
        else:
            print(Game.instructions)

        # Prints other information following instructions at launch
        self.board.print_default_board()
        self.board.print_board_sizes()



def parse_args():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Height of the board")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Width of the board")
    return parser.parse_args()

def main():
    # Set height/width of board w/ command-line arguments
    args = parse_args()
    height = args.height
    width = args.width

    # Initialize game and print instructions/board
    connect_four = Game(height, width)
    connect_four.print_instructions()
    

    
        


if __name__ == "__main__":
    main()