import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 610, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

class Tile:
    def __init__(self, row, col, letter, color, size):
        self.row = row
        self.col = col
        self.letter = letter
        self.color = color
        self.size = size

    def draw(self):
        pygame.draw.rect(window, self.color, (self.col * 120 + 15, self.row * 120 + 10, self.size[0], self.size[1]))

        font = pygame.font.SysFont("Arial", 90)
        text = font.render(self.letter, 1, (255, 255, 255))
        window.blit(text, (self.col * 120 + 40, self.row * 120 + 10))


class Board:
    def __init__(self):
        self.tiles = []

        self.word = self.generate_random_word()
        self.current_guess = ""
        self.guess_num = 1

        self.letters_in_word = []
        self.correct_letters = ""

        self.game_over = False

        self.generate_board()

    def generate_random_word(self):
        with open(r"possible_words.txt", "r") as f:
            words = f.read().split("\n")
            word = random.choice(words)

        return word

    def generate_board(self):
        for row in range(6):
            for col in range(5):
                tile = Tile(row, col, "", (70, 70, 70), (100, 100))
                self.tiles.append(tile)

    def update(self):
        self.update_tiles()

    def display_guess_on_tile(self, tile):
        for tile in self.tiles:
            if tile.row == self.guess_num - 1:
                tile.letter = ""
                if tile.col < len(self.current_guess):
                    tile.letter = self.current_guess[tile.col]

    def update_tiles(self):
        for tile in self.tiles:
            self.display_guess_on_tile(tile)
            tile.draw()

    def add_letter_to_guess(self, letter):
        if len(self.current_guess) < 5:
            self.current_guess += letter

    def remove_letter_from_guess(self):
        self.current_guess = self.current_guess[:-1]

    def submit_guess(self):
        with open(r"possible_guesses.txt", "r") as f:
            words = f.read().split("\n")
            if self.current_guess.lower() in words:
                self.color_tiles()
                
                self.guess_num += 1
                self.current_guess = ""
                self.handle_game_win()
                self.handle_game_end()
            else:
                print("Incorrect guess!")

    def color_tiles(self):
        self.correct_letters = ""
        for tile in self.tiles:
            if tile.row == self.guess_num - 1:
                if tile.letter.lower() == self.word[tile.col]:
                    tile.color = (0, 255, 0)
                    self.correct_letters += tile.letter
                elif tile.letter.lower() in self.word and tile.letter.lower() not in self.letters_in_word:
                    tile.color = (255, 255, 0)
                    self.letters_in_word.append(tile.letter.lower())
        self.letters_in_word = []

    def handle_game_end(self):
        if self.guess_num > 6 and not self.game_over:
            self.game_over = True
            print("Game over!")
            print(f"The word was: {self.word}")

    def handle_game_win(self):
        player_won = True
        for letter in self.word:
            if letter.upper() not in self.correct_letters:
                player_won = False

        if player_won:
            print("You won!")
            self.game_over = True
            sys.exit()
class Game:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()

        self.board = Board()

        self.run()

    def run(self):
        while self.running:
            window.fill((0, 0, 0))
            self.get_input()

            self.board.update()

            self.end_game()

            pygame.display.update()
            self.clock.tick(self.fps)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key).lower() in "abcdefghijklmnopqrstuvwxyz":
                    self.board.add_letter_to_guess(pygame.key.name(event.key).upper())
                if event.key == pygame.K_BACKSPACE:
                    self.board.remove_letter_from_guess()
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    self.board.submit_guess()

    def end_game(self):
        if self.board.game_over:
            self.running = False
            pygame.quit()
            sys.exit()

Game()