import sys
from sys import platform
from os import system
from time import sleep

sys.path.append("..")

from rich import print
from rich.prompt import Prompt
from nltk.corpus import wordnet

from words.wordgen import *  # NOQA


if platform == "linux" or platform == "linux2":
    clear = "clear"
elif platform == "win32":
    clear = "cls"


def welcome_screen():
    for word in ["[bold green]Welcome [/bold green]", "[bold green]to [/bold green]", "[bold green]anantdark's [/bold green]", "[bold green]Hangman [/bold green]", "[bold green]game.[/bold green]"]:
        print(word, end=" ")
        sleep(0.5)
    print()


def play_again():
    play_again_prompt = Prompt.ask("Would you like to play again?", default='n').lower()
    return play_again_prompt


def get_score(wins, games):
    if games == 1:
        print(f"You have won {wins} out of {games} game")
    else:
        print(f"You have won {wins} out of {games} games")


def definition(word):
    syns = wordnet.synsets(word)
    return syns[0].definition(), syns[0].examples()


def print_definition(word):
    try:
        result = definition(word)
        if result[0] :
            print("DEFINITION: ", result[0], end="\n")
        if result[1] != []:
            print("EXAMPLES: ", result[1], end="\n")
        else:
            print("EXAMPLES: [bold red]NOT FOUND![/bold red]")
    except:
            print("ERROR: [bold red]AN ERROR OCCURRED![/bold red]")


def hangman(word, wins: int = 0, games: int = 0):
    """
    Parameters:
    word (str): This variable holds the string to be guessed.
    wins (int): This variable tracks the number of wins the player has had.
    games (int): This variable tracks the number of games the player has played.
    """
    welcome_screen()
    system(clear)
    used_letters = []
    lives = 6
    board = "*"*len(word)

    def prompt_with_message(message):
        print(f"{message}\nYou still have {lives} lives. Guess again!")
        return input()

    while lives:
        print(f'You have {lives} lives. Guess a word. \nCurrent board',
            f'(guessed letters: {" ".join(used_letters)})' if used_letters else '',
            f'\n{board}')
        guess = input()
        # If guess is more than 1 character, prompt to try again
        while len(guess) != 1:
            guess = prompt_with_message("You can only guess with 1 character")
        # If character exist in word, then don't lose a life
        character_exist = False
        # If the player has reused a guess, prompt to try again
        while guess in used_letters:
            guess = prompt_with_message("You have already used this letter.")
        
        used_letters += guess
        
        for i in range(len(word)):
            if guess == word[i]:
                # Keep everything before and after index but replace at index
                board = board[:i] + guess + board[i+1:]
                character_exist = True
        if not character_exist:
            lives -= 1
        print(board)
        system(clear)
        # If any character is missing, continue (go back to top of while loop
        # and skipping win prompt
        completed_word = True
        for char in board:
            if char == "*":
                completed_word = False
                break
        if completed_word:
            break

    if lives == 0:
        print(f'You lost all your lives\U00002764 \U00002639 The word is [bold red]{word}[/bold red]')
    else:
        print(f'You win\U0001F389! The word is [bold green]{word}[/bold green]')
        wins += 1
    
    # Increment number of games played.
    games += 1

    # Print the words definition to screen.
    print_definition(word)

    # Get current score.
    get_score(wins, games)
    
    # Get user response to play again
    user_response = play_again()
    if user_response == 'y':
        return hangman(word = random_word(), wins=wins, games=games)
    else:
        exit()
        

def run():
    hangman(random_word())
