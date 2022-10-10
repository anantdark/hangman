import pygame
import math
import random

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
TITLE_FONT=pygame.font.SysFont("comicsans", 80)

# Loading Images
images = []
for i in range(7):
    image = pygame.image.load(f'hangman{i}.png')
    images.append(image)

# Game Variables
hangman_status = 0
words=["Developer","Ambush","Reddit","Food","PYGAME","PYthon"]
words=[word.upper() for word in words]

# word="FOOD"
word = random.choice(words)
guessed = []

# SETUP game Loop
FPS = 60
clock = pygame.time.Clock()
running = True


def draw():
    screen.fill(WHITE)
    #Draw title
    text= TITLE_FONT.render("SIMPLE HANGMAN GAME",1,RED)
    screen.blit(text,(WIDTH/2-text.get_width()/2,20))

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
            screen.blit(text, (x - int(text.get_width() / 2), y - int(text.get_height() / 2)))

    screen.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def display_message(message): #DRY concept lol
    screen.fill(WHITE)
    text= WORD_FONT.render(message,1,BLACK)
    screen.blit(text,(int(WIDTH/2-text.get_width()/2),int(HEIGHT/2-text.get_height()/2)))
    pygame.display.update()
    pygame.time.delay(2000)

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
                    distance = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)  # Distance formula
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
        display_message("YOU WON!!!!")
        break
    if hangman_status == 6:
        display_message("You Lost :(")
        break

pygame.quit()
