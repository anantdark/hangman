from wordgen import *
LIVES = 6
def hangman(word, wordlen):
    while LIVES:
        temp_list = list(wordlen*"*")
        print(*temp_list)

    pass







if __name__=="__main__":
    current_word = myword()
    wordlen = len(current_word)
    hangman(current_word, wordlen)