import random

def myword():
    # will return the word to be used for the game
    word  = "mango"
    return word

def random_word():
    lines = open('five_letter_words.txt').read().splitlines()
    return random.choice(lines)

if __name__=="__main__":
    print("CoDeD By AnAnT")
