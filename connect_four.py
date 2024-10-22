"""
Game Name: Connect Four
Description: Get four in a row to win!
Author: Zachary Coe
Date: 2024-10-21
"""



import random
from math import inf
import argparse



DEFAULT_HEIGHT = 6
DEFAULT_WIDTH = 7
RED_CIRCLE = "\U0001f534"
YELLOW_CIRCLE = "\U0001F7E1"
POINTER = "↓"
FOUR = 4
THREE = 3
TWO = 2
TWO_ROW_SCORE = 100
THREE_ROW_SCORE = 250
BLOCK_SCORE = 300
WINNER_SCORE = 1000
# Length of longer line in instructions
SPACE_OVER = 44
COLUMN_WIDTH = 6
DOUBLE_DIGIT_INT = 10
EMPTY_SPACE = " "

MAX_DEPTH = 3



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
            
    def undo_update(self, column):
        for row in range(self.height):
            if self.board_spots[row][column] != EMPTY_SPACE:
                self.board_spots[row][column] = EMPTY_SPACE
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

    def print_chosen_row(self, column):
        print(" " * self.spacing, end="")
        for col in range(self.width):
            if col == column:
                print(f"   {POINTER}  ", end="")
            else:
                print("      ", end="")
        print()

    def print_current_board(self, column):
        print()
        self.print_chosen_row(column)
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
            print(" " * spacing, end=f"Starting the game with a board of {self.height}x{self.width}\n\n")

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
    def __init__(self, height, width, hard=False):
        self.play_again = True
        self.winner = None
        self.board = Board(height, width)
        self.intro_print()
        self.hard = self.get_difficulty()
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
        self.winner = None

    def get_difficulty(self):
        while True:
            try:
                options = ["easy", "e", "hard", "h"]
                difficulty = input("\nSelect the difficulty (Easy/Hard): ").lower()
                if difficulty in options[:2]:
                    return False
                elif difficulty in options[2:]:
                    return True
                else:
                    raise ValueError()
            except ValueError:
                print("Invalid input. Please type 'easy' or 'hard'.")
        
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
        self.board.print_current_board(turn)

    def hard_computer_turn(self):
        turn = self.find_best_move()
        pause()
        self.board.update_board(turn, self.computer)
        self.board.print_current_board(turn)
    
    def player_turn(self):
        turn = self.get_player_turn()
        self.board.update_board(turn, self.player)
        self.board.print_current_board(turn)
    
    def player_start(self):
        self.player_turn()
        if self.check_game_over():
            return

        if not self.hard:
            self.easy_computer_turn()
            if self.check_game_over():
                return
        else:
            self.hard_computer_turn()
            if self.check_game_over():
                return

    def computer_start(self):
        if not self.hard:
            self.easy_computer_turn()
            if self.check_game_over():
                return
        else:
            self.hard_computer_turn()
            if self.check_game_over():
                return
        
        self.player_turn()
        if self.check_game_over():
            return

    def check_game_over(self):
        return self.check_for_winner()[0] or self.board.is_board_full()

    def check_for_winner(self):
        horizontal_win, winner = self.check_horizontal()
        if horizontal_win:
            return True, winner

        vertical_win, winner = self.check_vertical()
        if vertical_win:
            return True, winner

        rising_diagonal_win, winner = self.check_rising_diagonal()
        if rising_diagonal_win:
            return True, winner

        falling_diagonal_win, winner = self.check_falling_diagonal()
        if falling_diagonal_win:
            return True, winner
        
        return False, None

    def check_horizontal(self, in_a_row=FOUR):
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
                if red_check >= in_a_row:
                    return True, RED_CIRCLE
                elif yellow_check >= in_a_row:
                    return True, YELLOW_CIRCLE
        return False, None
    
    def check_vertical(self, in_a_row=FOUR):
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
                if red_check >= in_a_row :
                    return True, RED_CIRCLE
                elif yellow_check >= in_a_row:
                    return True, YELLOW_CIRCLE
        return False, None
    
    def check_rising_diagonal(self, in_a_row=FOUR):
        spots = self.board.board_spots
        for row in range(self.board.height - 1, in_a_row - 2, -1):
            for col in range(self.board.width - in_a_row + 1):
                if all(spots[row - n][col + n] == RED_CIRCLE for n in range(in_a_row)):
                    return True, RED_CIRCLE
                elif all(spots[row - n][col + n] == YELLOW_CIRCLE for n in range(in_a_row)):
                    return True, YELLOW_CIRCLE
        return False, None
    
    def check_falling_diagonal(self, in_a_row=FOUR):
        spots = self.board.board_spots
        for row in range(self.board.height - in_a_row + 1):
            for col in range(self.board.width - in_a_row + 1):
                if all(spots[row + n][col + n] == RED_CIRCLE for n in range(in_a_row)):
                    return True, RED_CIRCLE
                elif all(spots[row + n][col + n] == YELLOW_CIRCLE for n in range(in_a_row)):
                    return True, YELLOW_CIRCLE
        return False, None
    
    def three_in_a_row_computer(self):
        score = 0

        if self.check_horizontal(THREE) == (True, self.computer.color):
            score += THREE_ROW_SCORE
        if self.check_vertical(THREE) == (True, self.computer.color):
            score += THREE_ROW_SCORE
        if self.check_rising_diagonal(THREE) == (True, self.computer.color):
            score += THREE_ROW_SCORE
        if self.check_falling_diagonal(THREE) == (True, self.computer.color):
            score += THREE_ROW_SCORE

        return score
    
    def two_in_a_row_computer(self):
        score = 0

        if self.check_horizontal(TWO) == (True, self.computer.color):
            score += TWO_ROW_SCORE
        if self.check_vertical(TWO) == (True, self.computer.color):
            score += TWO_ROW_SCORE
        if self.check_rising_diagonal(TWO) == (True, self.computer.color):
            score += TWO_ROW_SCORE
        if self.check_falling_diagonal(TWO) == (True, self.computer.color):
            score += TWO_ROW_SCORE

        return score

    def three_in_a_row_player(self):
        score = 0

        if self.check_horizontal(THREE) == (True, self.player.color):
            score -= THREE_ROW_SCORE
        if self.check_vertical(THREE) == (True, self.player.color):
            score -= THREE_ROW_SCORE
        if self.check_rising_diagonal(THREE) == (True, self.player.color):
            score -= THREE_ROW_SCORE
        if self.check_falling_diagonal(THREE) == (True, self.player.color):
            score -= THREE_ROW_SCORE

        return score
    
    def two_in_a_row_player(self):
        score = 0

        if self.check_horizontal(TWO) == (True, self.player.color):
            score -= TWO_ROW_SCORE
        if self.check_vertical(TWO) == (True, self.player.color):
            score -= TWO_ROW_SCORE
        if self.check_rising_diagonal(TWO) == (True, self.player.color):
            score -= TWO_ROW_SCORE
        if self.check_falling_diagonal(TWO) == (True, self.player.color):
            score -= TWO_ROW_SCORE

        return score
    
    def check_for_blocks(self):
        score = 0
        empty_columns = self.board.get_empty_columns()

        for col in empty_columns:
            self.board.update_board(col, self.player)
            
            is_winner, winner = self.check_for_winner()

            if is_winner and winner == self.player.color:
                score -= BLOCK_SCORE

            self.board.undo_update(col)
        
        return score
    
    def evaluation_function(self):
        score = 0

        # Three in a row
        score += self.three_in_a_row_computer()
        score += self.three_in_a_row_player()

        # Two in a row
        score += self.two_in_a_row_computer()
        score += self.two_in_a_row_player()

        score += self.check_for_blocks()
        return score
    
    def minimax(self, is_maximizing=False, depth=0, alpha=(-inf), beta=(inf)):
        is_winner, winner = self.check_for_winner()
        if is_winner:
            if winner == self.computer.color:
                return WINNER_SCORE - (depth * 5)
            elif winner == self.player.color:
                return -WINNER_SCORE + (depth * 5)
        
        # A tie
        if self.board.is_board_full():
            return 0
        # Reached max recursion depth
        if depth == MAX_DEPTH:
            return self.evaluation_function()
        
        empty_columns = self.board.get_empty_columns()
        
        if is_maximizing:
            best_score = float(-inf)
            for col in range(self.board.width):
                if col in empty_columns:
                    self.board.update_board(col, self.computer)
                    new_score = self.minimax(not is_maximizing, depth+1, alpha, beta)
                    self.board.undo_update(col)
                    best_score = max(best_score, new_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        
        else:
            best_score = float(inf)
            for col in range(self.board.width):
                    if col in empty_columns:
                        self.board.update_board(col, self.player)
                        new_score = self.minimax(not is_maximizing, depth+1, alpha, beta)
                        self.board.undo_update(col)
                        best_score = min(best_score, new_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score
        
    def find_best_move(self):
        best_score = (-inf)
        best_move = -1
        empty_columns = self.board.get_empty_columns()

        # Sets up an alternating move checker
        # prioritizing middle of the board and
        # moving outwards from there
        middle = self.board.width // 2
        columns = [middle]
        for n in range(1, middle + 1):
            if middle + n < self.board.width:
                columns.append(middle + n)
            if middle - n >= 0:
                columns.append(middle - n)

        for col in columns:
            if col in empty_columns:
                self.board.update_board(col, self.computer)

                current_score = self.minimax()

                self.board.undo_update(col)

                if current_score > best_score:
                    best_move = col
                    best_score = current_score

        return best_move
    
    def set_winner(self):
        winner = self.check_for_winner()[1]
        self.winner = winner
    
    def update_scores(self):
        if self.player.color == self.winner:
            print(f"{self.player} win!!")
            self.player.score += 1
        elif self.computer.color == self.winner:
            print(f"{self.computer} wins!!")
            self.computer.score += 1
    
    def print_scores(self):
        print(f"Wins:   {self.player.score}")
        print(f"Losses: {self.computer.score}")
        print(f"Ties:   {self.games - self.player.score - self.computer.score}")
    
    def end_game(self):
        self.games += 1
        self.set_winner()
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
            connect_four.board.print_default_board()
        # Randomly choose who goes first each game
        who_first = connect_four.determine_first()

        while not connect_four.check_game_over():
            # Turn order changes depending on who first
            if who_first == connect_four.player:
                connect_four.player_start()
            else:
                connect_four.computer_start()
        # Once the game is over, update/print scores
        connect_four.end_game()

    

if __name__ == "__main__":
    main()