import pygame
import math

class Game(object):
    # Variables
    screen = None
    clock = None
    hangman_status = 0
    images = []
    letters = []

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Fonts
    LETTER_FONT = None

    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 500
        self.IMAGE_POS = (10, 10)
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

        # Setup functions
        self.loadImage()
        self.loadLetters()
        self.main()

    def main(self):
        run = True

        self.draw()

        while run:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()

    def draw(self):
        self.screen.fill(self.WHITE)
        self.screen.blit(self.images[self.hangman_status], self.IMAGE_POS)

        for letter in self.letters:
            x, y, ltr = letter
            text = self.LETTER_FONT.render(ltr, 1, self.BLACK)
            self.screen.blit(text, (x - round(text.get_width() / 2), y - round(text.get_height() / 2)))
            pygame.draw.circle(self.screen, self.BLACK, (x, y), self.RADIUS, 1)

        pygame.display.update()

    def loadImage(self):
        for i in range(7):
            image = pygame.image.load(f"images/hangman{str(i)}.png")
            self.images.append(image)

    def loadLetters(self):
        self.LETTER_FONT = pygame.font.SysFont("Consolas", 20)
        letter_x = round(((self.WIDTH - (self.NUM_OF_LETTERS / 2) * (2 * self.RADIUS + self.GAP)) + self.RADIUS) / 2)
        letter_y = self.HEIGHT - (2 * self.GAP + 4 * self.RADIUS)
        char = 65

        for i in range(self.NUM_OF_LETTERS):
            x = letter_x + ((i % 13) * (2 * self.RADIUS + self.GAP))
            y = letter_y + ((i // 13) * (self.GAP + self.RADIUS * 2))
            letter = chr(char + i)
            self.letters.append([x, y, letter])

if __name__ == '__main__':
    game = Game()
