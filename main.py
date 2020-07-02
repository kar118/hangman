import pygame
import math
import random

class Game(object):
    # Variables
    screen = None
    clock = None
    display_word = None
    hangman_status = None
    word = None
    comunicates = ['You lost!', 'You won!']
    images = []
    words = []
    letters = []
    gusses = []

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 190, 0)

    # Fonts
    LETTER_FONT = None
    WORD_FONT = None

    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 500
        self.IMAGE_POS = (50, 50)
        self.FPS = 60
        self.NUM_OF_LETTERS = 26
        self.GAP = 10
        self.RADIUS = 20

        # Setup function
        self.initGame()

    def initGame(self):
        pygame.init()
        pygame.display.set_caption("Hangman game")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.hangman_status = 0
        self.gusses.clear()
        self.display_word = ""

        # Setup functions
        self.loadImage()
        self.loadFonts()
        self.loadWords()
        self.loadLetters()
        self.word = random.choice(self.words)
        self.main()

    def main(self):
        run = True
        while run:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(self.hangman_status)
                    for letter in self.letters:
                        result = self.isLetterClicked(pos[0], pos[1], letter)
                        if result:
                            letter[3] = False
                            if letter[2] in self.word:
                                self.gusses.append(letter[2])
                            elif letter[2] not in self.word:
                                self.hangman_status += 1

            if self.isWin():
                self.showWin()
                self.reset()
            elif self.isLost():
                self.showLost()
                self.reset()
            else:
                self.draw()
        pygame.quit()

    def draw(self):
        self.screen.fill(self.WHITE)
        self.screen.blit(self.images[self.hangman_status], self.IMAGE_POS)

        self.displayLetters()
        self.displayWord()

        pygame.display.update()

    def reset(self):
        self.gusses.clear()
        self.hangman_status = 0
        self.display_word = 0
        self.word = random.choice(self.words)

        for letter in self.letters:
            letter[3] = True

    def isLost(self):
        if self.hangman_status == 6:
            return True

    def isWin(self):
        if self.display_word == self.word:
            return True

    def showLost(self):
        pygame.time.delay(500)
        self.screen.fill(self.BLACK)
        text = self.WORD_FONT.render(self.comunicates[0] + " Answer: " + self.word, 1, self.WHITE)
        x = round((self.WIDTH - text.get_width()) / 2)
        y = round((self.HEIGHT - text.get_height()) / 2)
        self.screen.blit(text, (x, y))
        pygame.display.update()
        pygame.time.delay(1800)

    def showWin(self):
        pygame.time.delay(500)
        self.screen.fill(self.YELLOW)
        text = self.WORD_FONT.render(self.comunicates[1], 1, self.WHITE)
        x = round((self.WIDTH - text.get_width()) / 2)
        y = round((self.HEIGHT - text.get_height()) / 2)
        self.screen.blit(text, (x, y))
        pygame.display.update()
        pygame.time.delay(1800)

    def loadWords(self):
        with open("words.txt", "r") as f:
            self.words = f.readline().split(",")
            for i in range(len(self.words)):
                self.words[i] = self.words[i].upper()
        f.close()

    def loadImage(self):
        for i in range(7):
            image = pygame.image.load(f"images/hangman{str(i)}.png")
            self.images.append(image)

    def loadFonts(self):
        self.LETTER_FONT = pygame.font.SysFont("Consolas", 20)
        self.WORD_FONT = pygame.font.SysFont("Consolas", 20)

    def loadLetters(self):
        letter_x = round(((self.WIDTH - (self.NUM_OF_LETTERS / 2) * (2 * self.RADIUS + self.GAP)) + self.RADIUS) / 2)
        letter_y = self.HEIGHT - (2 * self.GAP + 4 * self.RADIUS)
        char = 65

        for i in range(self.NUM_OF_LETTERS):
            x = letter_x + ((i % 13) * (2 * self.RADIUS + self.GAP))
            y = letter_y + ((i // 13) * (self.GAP + self.RADIUS * 2))
            letter = chr(char + i)
            self.letters.append([x, y, letter, True])

    def displayWord(self):
        self.display_word = ""
        for letter in self.word:
            if letter in self.gusses:
                self.display_word += letter
            elif letter == " ":
                self.display_word += " "
            else:
                self.display_word += " _"
        text = self.WORD_FONT.render(self.display_word, 1, self.BLACK)
        self.screen.blit(text, (300, 100))

    def displayLetters(self):
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                text = self.LETTER_FONT.render(ltr, 1, self.BLACK)
                self.screen.blit(text, (x - round(text.get_width() / 2), y - round(text.get_height() / 2)))
                pygame.draw.circle(self.screen, self.BLACK, (x, y), self.RADIUS, 1)

    def isLetterClicked(self, mouse_x, mouse_y, letter):
        distance = math.sqrt((letter[0]-mouse_x)**2 + (letter[1]-mouse_y)**2)
        if distance <= self.RADIUS:
            return True
        else:
            return False


if __name__ == '__main__':
    game = Game()
