import sys

import pygame
import math
import random

sys.path.append("..")

from words.wordgen import random_word  # NOQA

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet # for definition and synonyms

# Setup Display
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Button Variables
RADIUS = 20
GAP_SIZE = 15
letters = []
startX = round((WIDTH - (RADIUS * 2 + GAP_SIZE) * 13) / 2)  # Value =42

# startX= round((WIDTH-((RADIUS*2*13)+(GAP_SIZE*12)))/2) # value = 50
startY = 400

A = 65
for i in range(26):
    x = startX + GAP_SIZE * 2 + ((RADIUS * 2 + GAP_SIZE) * (i % 13))
    y = startY + ((i // 13) * (GAP_SIZE + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts

LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("comicsans", 80)

# Loading Images
images = []
for i in range(7):
    image = pygame.image.load(f'hangman{i}.png')
    images.append(image)

# Game Variables
hangman_status = 0

# word="FOOD"
word = random_word().upper()
guessed = []

# SETUP game Loop
FPS = 60
clock = pygame.time.Clock()
running = True

def definition(word):
    syns = wordnet.synsets(word.lower())
    defini = syns[0].definition()
    defin = defini.split()        
    split_index = len(defin)-1
    definition = "no definition found :("
    if (len(defin) < 6):
        definition = defini
    if (len(defin) < 14 and len(defin) > 6):
        def1, def2 = "", ""
        for i in range(0, split_index//2):
            def1 = def1 + " " + defin[i]
        for j in range(split_index//2, split_index):
            def2 = def2 + " " + defin[j]
        definition = def1 + "\n" + def2
    if (len(defin) > 14):
        def1, def2, def3 = "", "", ""
        for i in range(0, split_index//3):
            def1 = def1 + " " + defin[i]
        for j in range(split_index//3, (split_index//3)*2):
            def2 = def2 + " " + defin[j]
        for k in range((split_index//3)*2, split_index):
            def3 = def3 + " " + defin[k]
        definition = def1 + "\n" + def2 + "\n" + def3
    
    return definition
    
def draw():
    screen.fill(WHITE)
    # Draw title
    text = TITLE_FONT.render("SIMPLE HANGMAN GAME", 1, RED)
    screen.blit(text, (WIDTH/2-text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "

    text = WORD_FONT.render(display_word, 1, BLACK)
    screen.blit(text, (400, 200))

    # draw Buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, BLACK)
            # screen.blit(text,(x-10,y-14)) # this one works too
            screen.blit(text, (x - int(text.get_width() / 2),
                        y - int(text.get_height() / 2)))

    screen.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):  # DRY concept lol
    screen.fill(WHITE)
    #multiline message
    if message.__contains__("\n"):
        lines = message.split('\n')
        for i, msg in enumerate(lines):
            txt_surface = LETTER_FONT.render(msg, 1, BLACK)
            if (i == 0): txt_surface = WORD_FONT.render(msg, 1, BLACK)
            screen.blit(txt_surface, (int(WIDTH/2-txt_surface.get_width()/2),
                int((HEIGHT/6)*(i+1/2))))
    #single line message
    if not message.__contains__("\n"):
        text = WORD_FONT.render(message, 1, BLACK)
        screen.blit(text, (int(WIDTH/2-text.get_width()/2),
                    int(HEIGHT/2-text.get_height()/2)))
    pygame.display.update()
    pygame.time.delay(6000)


while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            # print(m_x,m_y)
            # print(RADIUS)
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    # Distance formula
                    distance = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                    if distance < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1
    draw()
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    draw()
    if won:
        display_message("YOU WON!!!!\nThe word is: " + word)
        break
    if hangman_status == 6:
        
        definition = definition(word)
        
        display_message("You Lost :(\n" + word.lower().capitalize() + ": " + definition)
        break

pygame.quit()
