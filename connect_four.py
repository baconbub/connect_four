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
FOUR = 4
# Length of longer line in instructions
SPACE_OVER = 44
COLUMN_WIDTH = 6
DOUBLE_DIGIT_INT = 10
EMPTY_SPACE = " "



class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.spacing = self.get_spacing()
        self.board_spots = [
            [EMPTY_SPACE for _ in range(self.width)] for _ in range(self.height)
        ]

    def update_board(self, column, player):
        for row in range(self.height - 1, -1, -1):
            if self.board_spots[row][column] == EMPTY_SPACE:
                self.board_spots[row][column] = player.color
                return

    def get_spacing(self):
        # Setting a space buffer to center the board on the instructions
        spacing = (SPACE_OVER - ((self.width * COLUMN_WIDTH) + 1)) // 2
        if spacing < 0:
            spacing = 0
        return spacing
    
    def print_board_bottom(self):
        print(" " * self.spacing, end="")
        if self.width >= DOUBLE_DIGIT_INT:
            for num in range(1, DOUBLE_DIGIT_INT):
                print(f"  [{num}] ", end="")
            for num in range(DOUBLE_DIGIT_INT, self.width + 1):
                print(f" [{num}]", end=" ")
        else:
            for num in range(1, self.width + 1):
                print(f"  [{num}] ", end="")
        # Give space for next line
        print("\n")


    def print_default_board(self):
        self.spacing = self.get_spacing()
        
        for _ in range(self.height - 1):
            print(" " * self.spacing, end="")
            for _ in range(self.width):
                print("|     ", end="")
            print("|")

        # Prints last line ("underline")
        print(" " * self.spacing, end="")
        print("\033[4m|     \033[0m" * self.width, end="\033[4m|\033[0m\n")

        self.print_board_bottom()

    def print_current_board(self):
        print()
        for row in range(self.height - 1):
            print(" " * self.spacing, end="")
            for col in range(self.width):
                if self.board_spots[row][col] == EMPTY_SPACE:
                    print(f"|     ", end="")
                else:
                    print(f"| {self.board_spots[row][col]}  ", end="")
            print("|")

        print(" " * self.spacing, end="")
        for col in range(len(self.board_spots[self.height - 1])):
            if self.board_spots[self.height - 1][col] == EMPTY_SPACE:
                print(f"\033[4m|     \033[0m", end="")
            else:
                print(f"\033[4m| {self.board_spots[self.height - 1][col]}  \033[0m", end="")
        print("\033[4m|\033[0m\n", end="")
        
        self.print_board_bottom()

    def print_board_size(self):
        if self.height != DEFAULT_HEIGHT or self.width != DEFAULT_WIDTH:
            string_length = len(f"Starting the game with a board of {self.height}x{self.width}")
            spacing = (((self.width * COLUMN_WIDTH) + 1) - string_length) // 2
            print(" " * spacing, end=f"Starting the game with a board of {self.height}x{self.width}\n")

    def get_empty_columns(self):
        empty_columns = []
        for col in range(len(self.board_spots[0])):
            if self.board_spots[0][col] == EMPTY_SPACE:
                empty_columns.append(col)
        return empty_columns
    
    def is_board_full(self):
        return all(all(col is not EMPTY_SPACE for col in row) for row in self.board_spots)
            

class Player:
    def __init__(self, color):
         self.score = 0
         self.color = color

    def __str__(self) -> str:
        return "You"

class Computer(Player):
    def __init__(self, color):
        super().__init__(color)

    def __str__(self) -> str:
        return "The computer"

class Game:
    instructions = """\n  Type the column number you want to drop
your piece into. Get 4 in a row and you win!\n"""

    def __init__(self, height, width, hard=False):
        self.play_again = True
        self.is_winner = False
        self.winner = None
        self.board = Board(height, width)
        self.intro_print()
        self.hard = hard
        self.player = Player(self.pick_piece())
        self.computer = Computer(self.set_computer_piece())
        self.games = 0

    def print_instructions(self):
        first_string_length = len("Type the column number you want to drop")
        second_string_length = len("your piece into. Get 4 in a row and you win!")
        first_spacing = (((self.board.width * COLUMN_WIDTH) + 1) - first_string_length) // 2
        second_spacing = (((self.board.width * COLUMN_WIDTH) + 1) - second_string_length) // 2
        print("\n" + (" " * first_spacing) + "Type the column number you want to drop")
        print((" " * second_spacing) + "your piece into. Get 4 in a row and you win!\n")
        

    def intro_print(self):
        # Prints information following instructions at launch
        self.print_instructions()
        self.board.print_default_board()
        self.board.print_board_size()

    def reset_board(self):
        self.board = Board(self.board.height, self.board.width)

    def reset_game(self):
        self.reset_board()
        self.is_winner = False
        self.winner = None
        

    def get_play_again(self):
        play_list = ["n", "y"]
        while True:     
            try:   
                play = input("Play again? (y/n) ").lower()
                if play in play_list:
                    if play == "y":
                        self.play_again = True
                        return
                    else:
                        self.play_again = False
                        return
                else:
                    raise ValueError()
            except ValueError:
                print("Please type either y or n.")

    def pick_piece(self):
        options = ["red", "r", "y", "yellow"]
        while True:
            try:
                player_piece = input(f"Which color would you like to play as? ({YELLOW_CIRCLE} /{RED_CIRCLE}) ").lower()
                if player_piece in options[:2]:
                    return RED_CIRCLE
                elif player_piece in options[2:]:
                    return YELLOW_CIRCLE
                else:
                    raise ValueError()
            except ValueError:
                print("Invalid input. Please type 'red' or 'yellow'")

    def set_computer_piece(self):
        if self.player.color == RED_CIRCLE:
            return YELLOW_CIRCLE
        else:
            return RED_CIRCLE
        
    def determine_first(self):
        first = random.choice([self.player, self.computer])
        print(f"{str(first)} will go first.")
        return first
    
    def get_player_turn(self):
        empty_columns = []
        for col in self.board.get_empty_columns():
            col += 1
            empty_columns.append(col)
        while True:
            try:
                turn = input("Where would you like to drop your piece: ")
                if turn.isnumeric():
                    turn = int(turn)
                    if turn in empty_columns:
                        turn -= 1
                        return turn
                    else:
                        raise ValueError()
                else:
                    raise ValueError()
            except ValueError:
                print(f"Please choose an empty column: {empty_columns}")

    def easy_computer_turn(self):
        # Randomly choose a spot on the board
        empty_columns = self.board.get_empty_columns()
        turn = random.choice(empty_columns)
        pause()
        self.board.update_board(turn, self.computer)
        self.board.print_current_board()
    
    def player_turn(self):
        turn = self.get_player_turn()
        self.board.update_board(turn, self.player)
        self.board.print_current_board()
    
    def one_round_player_start(self):
        self.player_turn()
        if self.check_game_over():
            return

        if not self.hard:
            self.easy_computer_turn()
            if self.check_game_over():
                return

    def one_round_computer_start(self):
        if not self.hard:
            self.easy_computer_turn()
            if self.check_game_over():
                return
        
        self.player_turn()
        if self.check_game_over():
            return

    def check_game_over(self):
        return self.check_for_winner() or self.board.is_board_full()

    def check_for_winner(self):
        horizontal_win, winner = self.check_horizontal()
        if horizontal_win:
            self.is_winner, self.winner = True, winner
            return self.is_winner

        vertical_win, winner = self.check_vertical()
        if vertical_win:
            self.is_winner, self.winner = True, winner
            return self.is_winner

        rising_diagonal_win, winner = self.check_rising_diagonal()
        if rising_diagonal_win:
            self.is_winner, self.winner = True, winner
            return self.is_winner

        falling_diagonal_win, winner = self.check_falling_diagonal()
        if falling_diagonal_win:
            self.is_winner, self.winner = True, winner
            return self.is_winner


    def check_horizontal(self):
        spots = self.board.board_spots
        for row in range(self.board.height):
            red_check = 0
            yellow_check = 0
            for col in range(self.board.width):
                if spots[row][col] == RED_CIRCLE:
                    red_check += 1
                    yellow_check = 0
                elif spots[row][col] == YELLOW_CIRCLE:
                    yellow_check += 1
                    red_check = 0
                else:
                    red_check = 0
                    yellow_check = 0
                if red_check >= FOUR:
                    return True, RED_CIRCLE
                elif yellow_check >= FOUR:
                    return True, YELLOW_CIRCLE
        return False, None
    
    def check_vertical(self):
        spots = self.board.board_spots
        for col in range(self.board.width):
            red_check = 0
            yellow_check = 0
            for row in range(self.board.height):
                if spots[row][col] == RED_CIRCLE:
                    red_check += 1
                    yellow_check = 0
                elif spots[row][col] == YELLOW_CIRCLE:
                    yellow_check += 1
                    red_check = 0
                else:
                    red_check = 0
                    yellow_check = 0
                if red_check >= FOUR :
                    return True, RED_CIRCLE
                elif yellow_check >= FOUR:
                    return True, YELLOW_CIRCLE
        return False, None
    
    def check_rising_diagonal(self):
        spots = self.board.board_spots
        for row in range(self.board.height - 3):
            for col in range(self.board.width - 3):
                if spots[row][col] == RED_CIRCLE and \
                    spots[row + 1][col + 1] == RED_CIRCLE and \
                        spots[row + 2][col + 2] == RED_CIRCLE and \
                            spots[row + 3][col + 3] == RED_CIRCLE:
                    return True, RED_CIRCLE
                elif spots[row][col] == YELLOW_CIRCLE and \
                    spots[row + 1][col + 1] == YELLOW_CIRCLE and \
                        spots[row + 2][col + 2] == YELLOW_CIRCLE and \
                            spots[row + 3][col + 3] == YELLOW_CIRCLE:
                    return True, YELLOW_CIRCLE
        return False, None
    
    def check_falling_diagonal(self):
        spots = self.board.board_spots
        for row in range(FOUR - 1, self.board.height - 3):
            for col in range(self.board.width - 3):
                if (spots[row][col] == RED_CIRCLE and \
                    spots[row - 1][col + 1] == RED_CIRCLE and \
                        spots[row - 2][col + 2] == RED_CIRCLE and \
                            spots[row - 3][col + 3] == RED_CIRCLE):
                    return True, RED_CIRCLE
                elif (spots[row][col] == YELLOW_CIRCLE and \
                    spots[row - 1][col + 1] == YELLOW_CIRCLE and \
                        spots[row - 2][col + 2] == YELLOW_CIRCLE and \
                            spots[row - 3][col + 3] == YELLOW_CIRCLE):
                    return True, YELLOW_CIRCLE
        return False, None
    
    def update_scores(self):
        if self.player.color == self.winner:
            print(f"{self.player} win!!")
            self.player.score += 1
        elif self.computer == self.winner:
            print(f"{self.computer} wins!!")
            self.computer.color += 1
    
    def print_scores(self):
        print(f"Wins:   {self.player.score}")
        print(f"Losses: {self.computer.score}")
        print(f"Ties:   {self.games - self.player.score - self.computer.score}")
    
    def end_game(self):
        self.games += 1
        self.update_scores()
        self.print_scores()
        print()
        self.get_play_again()
        print()
                    

        



def parse_args():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Height of the board")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Width of the board")
    return parser.parse_args()

def pause():
    while True:
        input("Press ENTER to continue")
        break



def main():
    # Set height/width of board w/ command-line arguments
    args = parse_args()
    height = args.height
    width = args.width

    # Initialize game and print instructions/board
    connect_four = Game(height, width)
    while connect_four.play_again:
        # Reset game to play again after first
        if connect_four.games > 0:
            connect_four.reset_game()
        # Randomly choose who goes first each game
        who_first = connect_four.determine_first()

        while not connect_four.check_game_over():
            # Turn order changes depending on who first
            if who_first == connect_four.player:
                connect_four.one_round_player_start()
            else:
                connect_four.one_round_computer_start()
        # Once the game is over, update/print scores
        connect_four.end_game()

    

    
        


if __name__ == "__main__":
    main()