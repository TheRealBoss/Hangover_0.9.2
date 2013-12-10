import random
import pygame, sys, time
from pygame.locals import *
from time import sleep
## nizmo

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

          
# set up the window
WINDOWWIDTH = 960
WINDOWHEIGHT = 720
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
pygame.display.set_caption('Hangover')

# set up the colors - eemalda, mida vaja pole
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DGREEN = (0, 128, 0)
BLUE = (0, 0, 255)
LBLUE = (0, 200, 255)
BROWN = (128,128,0)
WHITE = (255,255,255)
SKIN = (160,160,60)
DGREY = (25,25,25)
GREY = (50,50,50)
LGREY = (75,75,75)
GREEN = (0, 160, 0)
YELLOW = (252, 247, 37)

# variables
guess = ""
missedLetters = ""
correctLetters = ""
gameIsDone = False
roundNo = 0
textFile = open("wordlist.txt", "r")
wordList = []
option = [0,'New Game','About','Quit',0,'',0]# menu options
score = [0,0,'',0,0]# [0-Player Rounds,1-Hangman Rounds,2-Result,3-Player Games, 4-Hangman Games]
s = 0   # Stage counter
guessed = [0,'Guess a letter in my secret word!',0]# [0-(0 invalid guess, 1 valid guess),1-Screen Prompt,2-Keyboard delay
infoDisplayText = ['Welcome to Hangover','','by','','The Boss','']# [0-5 Text, 2 per row]
banner =[50,50,0,0,0,0,0,0]# Start point for Hangman+ banner text, mountains etc
MOVESPEED = 50
curser = [390, 190, 50, 50]# Start position for the curser on the menu

# videos
hangoverClip = pygame.movie.Movie('eyeblink.mpg')
danceClip = pygame.movie.Movie('dance.mpg')

# set up the fonts - vajadusel muuta
smallFont = pygame.font.SysFont(None, 20)
basicFont = pygame.font.SysFont(None, 30)
guessFont = pygame.font.SysFont(None, 36)
titleFont = pygame.font.SysFont(None, 48)
bannerFont = pygame.font.SysFont(None, 64)

# dictionary setup
for t in range(3):
    wordList.append(textFile.readline().split())

# Random Word generator
def getRandomWord(wordDict, level):
    wordKey = random.choice(wordDict[level])
    return wordKey

# Displays information text on screen
def infoDisplay():
    text = basicFont.render(infoDisplayText[0] + infoDisplayText[1], True, BLUE,)
    text1 = basicFont.render(infoDisplayText[2] + infoDisplayText[3], True, BLUE,)
    text2 = basicFont.render(infoDisplayText[4] + infoDisplayText[5], True, BLUE,)
    background()
    displayBoard(s, missedLetters, correctLetters, secretWord)
    windowSurface.blit(text, (350,130))
    windowSurface.blit(text1, (350,150))
    windowSurface.blit(text2, (350,170))
    pygame.display.update()
        
# background setup
def background():
    if roundNo == 0:
        background = pygame.image.load("klubi_ees.jpg")
        windowSurface.blit(background, (0, 0))
    elif roundNo == 1:
        background = pygame.image.load("baari_ees.jpg")
        windowSurface.blit(background, (0, 0)) # võta esimene cmd, praegudes on lihtsalt kohatäide
    elif roundNo == 2:
        background = pygame.image.load("tantsuporand.jpg")
        windowSurface.blit(background, (0, 0))

    
# winscreen/lossscreen - siia alla win/lossscreen videode funktsioonid.
def hangover():
    hangoverClip.set_display(windowSurface, (0, 0, 960, 720)) # (left, top, width, height)
    hangoverClip.play()

def dance():
    danceClip.set_display(windowSurface, (0, 0, 960, 720))
    danceClip.play()
    
    
# Get a guess from player
def getGuess(alreadyGuessed):
    while event.type == pygame.KEYDOWN:
        global guess
        guessed[0]=1 #valid guess
        guessed[2]=15 #keyboard delay
        guess = event.dict["unicode"]
        guess = guess.lower()
        if len(guess) != 1:
            guessed[0]=0
            guessed[1]="Please enter a single letter!"
            break
        elif str(guess) in alreadyGuessed:
            guessed[0] = 0
            guessed[1] = "Pick a different letter!"
            break
        elif str(guess) not in "abcdefghijklmnopqrstuvwxyz":
            guessed[0] = 0
            guessed[1] = "Please enter a letter"
            break
        else:
            guessed[1] = "Guess a letter!"
            return guess
    else:
        guessed[0] = 0
        guessed[2] = 0
        return
        
# Updates the screen with the guesses, correct letters
def displayBoard(display, missedLetters, correctLetters, secretWord): #0- display
    blanks = '-' * len(secretWord)
    blankText = titleFont.render(blanks, True, WHITE,)## võibolla vigane
    windowSurface.blit(blankText, (150,140))
    title = titleFont.render('Hangover', True, WHITE,)
    titles = titleFont.render('Hangover', True, BLACK,)
    pygame.draw.rect(windowSurface, BLACK,(740,20,220,440),1)
    pygame.draw.rect(windowSurface, BLACK,(741,21,218,89))
    length = basicFont.render(str(len(secretWord)) + ' letters', True, YELLOW,)
    if roundNo<3:
        scoreboard = basicFont.render('Round ' + str(roundNo+1), True, YELLOW,)
        scoreboards = basicFont.render('Round ' + str(roundNo+1), True, YELLOW,)
        windowSurface.blit(scoreboards,(815,419))
        windowSurface.blit(scoreboard,(815,420))
    guessText = basicFont.render(guessed[1], True, WHITE,)
    guessTexts = basicFont.render(guessed[1], True, BLACK,)
    windowSurface.blit(guessTexts, (148,98))
    windowSurface.blit(guessText, (150,100))
    windowSurface.blit(titles,(783,23))
    windowSurface.blit(title,(785,25))
    windowSurface.blit(length,(815,90))
    if score[2]!='':
        result = titleFont.render(score[2], True, BLUE,)
        windowSurface.blit(result, (730,365))
    for i in range (len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks [i+1:]
            correctText = titleFont.render(blanks, True, WHITE,)
            pygame.draw.rect(windowSurface, BLACK,(140, 135, len(secretWord) * 25,40))
            windowSurface.blit(correctText, (150,140))
    if display >=1: #elif
        pygame.draw.rect(windowSurface, WHITE,(741,109,218,41))
        pygame.draw.rect(windowSurface, BLACK,(740,109,220,41),1)
        text1a = guessFont.render('1.', True, BLACK,)
        text1b = guessFont.render(missedLetters[0].upper(), True, BLUE,)
        text1c = titleFont.render('X', True, RED,)
        windowSurface.blit(text1a, (747,120))
        windowSurface.blit(text1b, (840,120))
        windowSurface.blit(text1c, (900,116))
        if display >= 2:
            pygame.draw.rect(windowSurface, WHITE,(741,149,218,41))
            pygame.draw.rect(windowSurface, BLACK,(740,149,220,41),1)
            text2a = guessFont.render('2.', True, BLACK,)
            text2b = guessFont.render(missedLetters[1].upper(), True, BLUE,)
            text2c = titleFont.render('X', True, RED,)
            windowSurface.blit(text2a, (747,160))
            windowSurface.blit(text2b, (840,160))
            windowSurface.blit(text2c, (900,156))
            if display >= 3:
                pygame.draw.rect(windowSurface, WHITE,(741,189,218,41))
                pygame.draw.rect(windowSurface, BLACK,(740,189,220,41),1)
                text3a = guessFont.render('3.', True, BLACK,)
                text3b = guessFont.render(missedLetters[2].upper(), True, BLUE,)
                text3c = titleFont.render('X', True, RED,)
                windowSurface.blit(text3a, (747,200))
                windowSurface.blit(text3b, (840,200))
                windowSurface.blit(text3c, (900,196))
                if display >= 4:
                    pygame.draw.rect(windowSurface, WHITE,(741,229,218,41))
                    pygame.draw.rect(windowSurface, BLACK,(740,229,220,41),1)
                    text4a = guessFont.render('4.', True, BLACK,)
                    text4b = guessFont.render(missedLetters[3].upper(), True, BLUE,)
                    text4c = titleFont.render('X', True, RED,)
                    windowSurface.blit(text4a, (747,240))
                    windowSurface.blit(text4b, (840,240))
                    windowSurface.blit(text4c, (900,236))
                    if display >= 5:
                        pygame.draw.rect(windowSurface, WHITE,(741,229,218,41))
                        pygame.draw.rect(windowSurface, BLACK,(740,229,220,41),1)
                        text4a = guessFont.render('5.', True, BLACK,)
                        text4b = guessFont.render(missedLetters[4].upper(), True, BLUE,)
                        text4c = titleFont.render('X', True, RED,)
                        windowSurface.blit(text4a, (747,240))
                        windowSurface.blit(text4b, (840,240))
                        windowSurface.blit(text4c, (900,236))
                        

def update():
    background()
    displayBoard(s, missedLetters, correctLetters, secretWord)
    pygame.display.update()
    
# window
def start():
    background()
    infoDisplay()
    pygame.display.update()
    sleep(2)

# Opening menu
def menu():
    # run the menu loop
    moveUp = False
    moveDown = False
    while option[4]==0:# Option [5] is the selection output bit
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                    # change the keyboard variables
                    if event.key == K_UP or event.key == ord('w'):#Curser Up
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == ord('s'):#Curser Down
                        moveUp = False
                        moveDown = True
                    if event.key == K_RETURN or event.key == K_SPACE:#Select current option
                        if curser[1]==190:
                            option[4]=1
                            secretWord = getRandomWord(wordList, roundNo)
                        if curser[1]==240:
                            option[6]=600
                            about()
                        if curser[1]==290:
                            pygame.quit()
                            sys.exit()
            if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveDown = False

        # move the Curser
        if moveDown and curser[1] < 290:
            curser[1] += MOVESPEED
            moveDown = False
        if moveUp and curser[1] > 200:
            curser[1] -= MOVESPEED
            moveUp = False

        # draw the background onto the surface & draw the banner
        background()
        drawBanner()

        # Output the current curser position
        if curser[1]==190:
            curser[2]=150
            option[5]='Play this awesome game'
        if curser[1]==240:
            curser[2]=150
            option[5]='About Hangover'
        if curser[1]==290:
            curser[2]=150
            option[5]='Quit Game'

        # draw the curser onto the surface
        pygame.draw.rect(windowSurface, WHITE, (curser[0],curser[1],curser[2],curser[3]),1)

        # draw the options onto the surface
        text1s = guessFont.render(option[1], True, BLACK,)
        text1 = guessFont.render(option[1], True, WHITE,)
        text2s = guessFont.render(option[2], True, BLACK,)
        text2 = guessFont.render(option[2], True, WHITE,)
        text3s = guessFont.render(option[3], True, BLACK,)
        text3 = guessFont.render(option[3], True, WHITE,)
        text4s = basicFont.render(option[5], True, BLACK,)
        text4 = basicFont.render(option[5], True, WHITE,)
        text6s = bannerFont.render("Hangover",True, BLACK,)
        text6 = bannerFont.render("Hangover",True, BLUE,)
        windowSurface.blit(text1s, (400,200))
        windowSurface.blit(text1, (402,202))
        windowSurface.blit(text2s, (400,250))
        windowSurface.blit(text2, (403,252))
        windowSurface.blit(text3s, (400,300))
        windowSurface.blit(text3, (402,302))
        windowSurface.blit(text4s, (400,350))
        windowSurface.blit(text4, (402,352))
        windowSurface.blit(text6s, (banner[0]-2,banner[1]-2))
        windowSurface.blit(text6, (banner[0],banner[1]))
        backgroundAnim()
        # draw the window onto the screen
        pygame.display.update()

def drawBanner():
    pygame.draw.line(windowSurface,WHITE,(0,70),(WINDOWWIDTH,70),50)
    pygame.draw.line(windowSurface,BLACK,(0,47),(WINDOWWIDTH,47),1)
    pygame.draw.line(windowSurface,BLACK,(0,93),(WINDOWWIDTH,93),1)

def backgroundAnim(): # muuda
        if banner[0]<=960:# Animate the banner text
            banner[0]+=1
        if banner[0]>960:
            banner[0]=-240
        if banner[2]<=1250:
            banner[2]+=1
        if banner[2]>1250:
            banner[2]=0
        if banner[3]<=1250:
            banner[3]+=2
        if banner[3]>1250:
            banner[3]=0
        if banner[4]<=1250:
            banner[4]+=3
        if banner[4]>1250:
            banner[4]=0
        if banner[5]<=1250:
            banner[5]+=4
        if banner[5]>1250:
            banner[5]=0
        if banner[6]>750:
            banner[6]=-350
        banner[7]+=1
        if banner[7]>10:
            banner[7]=0
            banner[6]+=1

def about():
    while option[6]>=0:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:#Return to main menu
                    option[6]=0
        background()
        drawBanner()
        text1s = guessFont.render('This is a game, based on the movie "The Hangover"', True, BLACK,)
        text1 = guessFont.render('This is a game, based on the movie "The Hangover"', True, WHITE,)
        text2s = guessFont.render('and done with the concept of the game "Hangman"', True, BLACK,)
        text2 = guessFont.render('and done with the concept of the game "Hangman"', True, WHITE,)
        text3s = guessFont.render('It is made using IDLE 3.3.2 and Pygame 1.9.2', True, BLACK,)
        text3 = guessFont.render('It is made using IDLE 3.3.2 and Pygame 1.9.2', True, WHITE,)
        text4s = guessFont.render('The game "Hangover"' , True, BLACK,)
        text4 = guessFont.render('The game "Hangover"', True, WHITE,)
        text5s = smallFont.render('Press "ENTER" to return to main menu', True, BLACK,)
        text5 = smallFont.render('Press "ENTER" to return to main menu', True, WHITE,)
        text6s = bannerFont.render("Hangover",True, BLACK,)
        text6 = bannerFont.render("Hangover",True, BLUE,)
        windowSurface.blit(text1s, (50,200))
        windowSurface.blit(text1, (52,202))
        windowSurface.blit(text2s, (50,250))
        windowSurface.blit(text2, (52,252))
        windowSurface.blit(text3s, (50,300))
        windowSurface.blit(text3, (52,302))
        windowSurface.blit(text4s, (50,350))
        windowSurface.blit(text4, (52,352))
        windowSurface.blit(text5s, (50,400))
        windowSurface.blit(text5, (52,402))
        windowSurface.blit(text6s, (banner[0]-2,banner[1]-2))
        windowSurface.blit(text6, (banner[0],banner[1]))
        backgroundAnim()
        option[6]-=1
        timer=int(option[6]/40)
        text7s = guessFont.render(str(timer), True, BLACK,)
        text7 = guessFont.render(str(timer), True, WHITE,)
        windowSurface.blit(text7s, (769,9))
        windowSurface.blit(text7, (770,10))
        pygame.display.update()



# game loop
secretWord = getRandomWord(wordList, roundNo)
menu()
start()
##infoDisplayText = ['Think you can beat me??','','Hahahahahaha!!!','','You have no chance!','']
infoDisplay()
infoDisplayText = ['Well done!','','You have reached round ',str(roundNo+1)]
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    update()
    if guessed[2]>0:# Guess input keyboard delay
        guessed[2]-=1
    else:
        if guessed[0] == 0: # if invalid guess, add it to missed letters #
            getGuess(missedLetters + correctLetters)
        else:
            guessed[0] = 0
            if str(guess) in secretWord:
                correctLetters = correctLetters + guess # add a valid guess to correct letters
                foundAllLetters = True
                for i in range(len(secretWord)):
                    if secretWord[i] not in correctLetters: # if a letter is missing from the whole word, all letters are not found
                        foundAllLetters = False
                        break
                if foundAllLetters: # if the word is fully guessed...
                    roundNo+=1 # next round
                    update()
                    sleep(1)
                    if roundNo == 3: # if last word is guessed
                        infoDisplayText = ['Congratulation!','','You had a nice party','','and arrived home happily!','']
                        infoDisplay()
                        sleep(3)
                        gameIsDone = True
                    else:
                        score[2]=''
                        guess = ''
                        missedLetters = ''
                        correctLetters = ''
                        secretWord = getRandomWord(wordList, roundNo)
                        if roundNo == 1:    
                            infoDisplayText = ['Well done!','','You have reached round ',str(roundNo+1), ' ', ' ']
                        elif roundNo == 2:
                            infoDisplayText = ['Well done!','','You have reached round ',str(roundNo+1), ' ', ' ']
                        elif roundNo == 3:
                            infoDisplayText = ['Well done!','','You have reached round ',str(roundNo+1), ' ', ' ']                          
                        gameIsDone = False
                        guessed=[0,'Guess a letter in my secret word!',0]
                        s = 0
                        start()
            else:
                missedLetters = missedLetters + str(guess)
                s+= 1
                if len(missedLetters) == 6:
                            score[2]='You Lost!'
                            displayBoard(s, missedLetters, correctLetters, secretWord)
                            infoDisplayText = ['Hahaha ','You Lost!','You had reached round ',str(roundNo+1),'The word was ',secretWord.title()]
                            infoDisplay()
                            sleep(2)
                            gameIsDone = True
            if gameIsDone:
                if roundNo == 3:
                    sleep(1) ## Sleep ette pane funktsioon, näiteks allpool on hangover(). See on winscreen video vms. Sleep väärtus vastavalt video pikkusele.
                if roundNo == 2:
                    sleep(1)
                if roundNo == 1:
                    sleep(1)
                if roundNo == 0:
                    hangover()
                    sleep(8)
                roundNo=0
                score[2]=''
                guess = ''
                missedLetters = ''
                correctLetters = ''
                option[4]=0
                menu()
                secretWord = getRandomWord(wordList, roundNo)
                infoDisplayText = ['Welcome to Hangover','','by','','The Boss','']
                gameIsDone = False
                guessed=[0,'Guess a letter in my secret word!',0]
                s = 0
                start()
