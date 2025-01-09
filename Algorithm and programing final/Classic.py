import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
fps = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")
timer = pygame.time.Clock()

# Fonts
font = pygame.font.Font('assets/Fonts/joystix monospace.otf', 24)
symbols_font = pygame.font.Font('assets/Fonts/joystix monospace.otf', 36)
# Game Variables
word_objects = [] # <--- what stores the generated words that appear on screen
mistkaets = 0
score = 0
paused = True
active_string = ""
submit = ""
word_speed = 1  # Speed of words
spawn_interval = 2  # Time in seconds between spawns
last_spawn_time = time.time()
high_score = 0
# Load Wordlist
'''
wordlist = []
with open("Algorithm and programing final/assets/lang_french.txt", "r") as file:
    wordlist = [line.strip() for line in file.readlines()]
    '''


class Word:
    """Class to represent a falling word."""
    def __init__(self, text, speed, x, y):
        self.text = text
        self.speed = speed
        self.x_position = x
        self.y_position = y

    def draw(self):
        
        
        active_len = len(active_string)
        color = 'blue'        
        screen.blit(font.render(self.text, True, color), (self.x_position, self.y_position))

        if active_string == self.text[:active_len]: #if the active string is the same as the text on screen, the text turns green
            screen.blit(font.render(active_string, True, 'green'), (self.x_position, self.y_position))
            #color = 'green'

        if self.x_position < 800:  
            #color = 'yellow'
            screen.blit(font.render(self.text, True, 'yellow'), (self.x_position, self.y_position))
        
        if self.x_position < 300:  
            #color = 'red'
            screen.blit(font.render(self.text, True, 'red'), (self.x_position, self.y_position))
        
#        else:
#            color = 'blue'

    def update(self):
        self.x_position -= self.speed

class button:
    def __init__(self, x_position, y_position, text, clicked, surface):
        self.x_position = x_position
        self.y_position = y_position
        self.text = text
        self.clicked = clicked
        self.surface = surface

    def draw(self):
        cir = pygame.draw.circle(self.surface,(45, 89, 135), (self.x_position, self.y_position), 35) #parameters : (surface to draw, color, center position(x,y), radius)
        if cir.collidepoint(pygame.mouse.get_pos()):
            btn = pygame.mouse.get_pressed()
            if btn[0]: #in pygame button 0 is left click
                pygame.draw.circle(self.surface, (190, 35, 35), (self.x_position, self.y_position), 35) #interface for feedback upon clicking
                self.clicked = True
            else:
                pygame.draw.circle(self.surface, (190, 89, 135), (self.x_position, self.y_position), 35) #highlighted but not clicked

        pygame.draw.circle(self.surface,'white', (self.x_position, self.y_position), 35, 3)

        self.surface.blit(symbols_font.render(self.text, True, 'white'), (self.x_position - 15, self.y_position - 25))


def draw_screen():
    global high_score
    #Draw the score, mistakes, and active string.
    pygame.draw.rect(screen, (32,42,68), [0, HEIGHT - 100, WIDTH, 100])
    pygame.draw.rect(screen,'white', [0,0, WIDTH, HEIGHT], 5)           # PARAMETERS = rect(surface, color, rect((left, top), (width, height)), width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1) 
    pygame.draw.line(screen,'white',(650, HEIGHT - 100), (650, HEIGHT), 2)
    pygame.draw.line(screen,'white',(1600, HEIGHT - 100), (1600, HEIGHT), 2)
    pygame.draw.line(screen,'white',(300, HEIGHT - 100), (300, HEIGHT), 2)

    pygame.draw.line(screen,'white',(0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)

    # text for showing the current level, player's current input, high score, score, mistakes, and pause


    screen.blit(font.render(f'Your Answer: "{active_string}"', True, 'white'), (675, HEIGHT - 75))

    #pause button
    pause_button = button(1645, HEIGHT - 52, '█', False, screen)
    pause_button.draw()

    screen.blit(font.render(f'Score:{score}', True, 'white'), (330, HEIGHT - 85))
    screen.blit(font.render(f'Best:{high_score}', True, 'white'), (330, HEIGHT - 50))
    #screen.blit(font.render(f'Best:{high_score}', True, 'white'), (550, 10))
    screen.blit(font.render(f'Mistakes:{mistkaets}/10', True, 'white'), (20, HEIGHT - 75))

    return pause_button.clicked 


def generate_word():
    #Spawns a new word at a random position.
    global word_speed
    global word_objects

    y_pos = None

    x_pos =  WIDTH + 300
    text = random.choice(wordlist).lower()
    
    max_attempts = 10

    for _ in range(max_attempts):
        y_pos = random.randint(10, HEIGHT - 150)
        x_pos = WIDTH + random.randint(50, 300)  # Add some randomness to x-position for spawning.

        # Check for overlaps with existing words
        if not any(
            abs(y_pos - w.y_position) < 50 and abs(x_pos - w.x_position) < 200
            for w in word_objects
        ):
            break
    else:
        
        y_pos = random.randint(10, HEIGHT - 150)
        x_pos = WIDTH + random.randint(50, 300)

    new_word = Word(text, word_speed, x_pos, y_pos)
    word_objects.append(new_word)


def check_answer(scor):
    """Checks if the active string matches any word."""
    global word_objects
    for w in word_objects:
        if w.text == submit:
            word_objects.remove(w)
            points = len(w.text) * 2 * (len(w.text) / 3)
            scor += int(points)
    return scor


languages = ['english', 'dutch', 'french']  # Available languages
current_language = 'english' 

def load_wordlist(language):
    # Load word list based on the selected language
    filepath = f'assets/lang_{language}.txt'
    with open(filepath, 'r') as file:
        da_words = file.read().splitlines()
    da_words.sort(key=len)  #  for later

    return da_words

def draw_pause():
    '''
    pause_text = font.render("Paused. Press ESC to resume.", True, BLACK)
    screen.blit(pause_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))'''

    global current_language

    surface = pygame.Surface((WIDTH, HEIGHT),pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [300,300,600,300], 0, 5) # parameters: (screen, [red, blue, green], [left, top, width, height], filled)
    pygame.draw.rect(surface, (0, 0, 0, 200), [300,300,600,300], 5, 5) #border
    # define buttons for pause menu
    resume_button = button(360, 400, '>', False, surface)
    resume_button.draw()
    quit_button = button(610, 400, 'X', False, surface)
    quit_button.draw()
    restart_button = button(610, 500, '@', False, surface)
    restart_button.draw()
    #define text for pause menu
    surface.blit(font.render('MENU', True, 'white'), (310,310))
    surface.blit(font.render('LANGUAGES', True, 'white'), (825,310))

    surface.blit(font.render('PLAY', True, 'white'), (410,385))
    surface.blit(font.render('QUIT', True, 'white'), (650,385))
    surface.blit(font.render('RESTART', True, 'white'), (650,485))


    # Language selection buttons
    for i, lang in enumerate(languages):

        lang_button = button(860 , 400 + i * 150, '', False, surface)
        surface.blit(font.render(f'{lang.upper()}', True, 'white'), (905, 385 + i * 150))
        lang_button.draw()
        if lang_button.clicked:
            current_language = lang  # Update the language
        if current_language == lang: # When button is clicked Green happens
            pygame.draw.circle(surface, 'green', (860, 400 + i * 150), 35, 5)
    screen.blit(surface,(0,0))
    return resume_button.clicked,  quit_button.clicked, restart_button.clicked

#high score read in from txt
file = open('HighScore_classic.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()

def check_high_score():
    """Checks and saves high scores."""
    global high_score
    if score > high_score:
        high_score = score
        file = open('HighScore_classic.txt', 'w') #this method is not recommended but it works for now
        file.write(str(int(high_score)))
        file.close()


#------------------------------MAIN GAME LOOP---------MAIN GAME LOOP---------------------------------------------------------------------------------------------------------
run = True
while run:
    screen.fill("black")
    timer.tick(fps)
    pause_button = draw_screen()

    if paused :        
        resume_button, quit_button, restart_button = draw_pause() #if paused is true such as the case when starting the game, draw the pause menu
        
        if resume_button: #if resume button is clicked, unpause
            paused = False
            wordlist = load_wordlist(current_language)
        if quit_button: # added an ingame quit button just to make it prettier, does the same thing as pygame.QUIT
            check_high_score() #add high score checking before exit
            run = False 
        if restart_button:
            paused = False
            mistkaets = 0
            word_objects.clear()
            word_speed = 1
            check_high_score()
            score = 0
    
    elif not paused:
        draw_screen()

        # Spawn new words periodically
        if time.time() - last_spawn_time > spawn_interval:
            generate_word()
            last_spawn_time = time.time()

        # Update and draw words
        for w in word_objects[:]:
            w.draw()
            w.update()

            # Remove words that go off-screen
            if w.x_position < -200:
                word_objects.remove(w)
                mistkaets += 1


    # Input handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            check_high_score()
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:#can also use escape to pause or resume
                paused = not paused
                wordlist = load_wordlist(current_language)
            
            if not paused:
                if event.unicode.isalpha():
                    active_string += event.unicode.lower()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN:
                    submit = active_string
                    active_string = ''
    if pause_button:
        paused = True
    # Handle submission
    if submit != '':
        score = check_answer(score)
        submit = ""

    # Restart game
    if mistkaets >= 10:
        paused = True
        mistkaets = 0
        word_objects.clear()
        word_speed = 1
        check_high_score()
        score = 0
    


    pygame.display.update()

pygame.quit()
