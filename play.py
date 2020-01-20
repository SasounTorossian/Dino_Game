import random
import pygame
from itertools import cycle

# Define some colors
BLACK = (0, 0, 0)
OFF_WHITE = (225, 225, 225)
OFF_GRAY = (80, 80, 80)
OFF_LIGHT_GRAY = (115, 115, 115)

# Initialise game engine
pygame.init()

# Set the width and height of the screen [width, height]
SIZE = (600, 300)
screen = pygame.display.set_mode(SIZE)

# 8-bit Font file path
FONT_FILE_PATH = "C:\\Users\\Sasoun\\Documents\\Software Workspace\\PycharmProjects\\Dino_Game\\VCR_OSD_MONO_1.001.ttf"

# Load the fonts
font_50 = pygame.font.Font(FONT_FILE_PATH, 50)
font_40 = pygame.font.Font(FONT_FILE_PATH, 40)
font_30 = pygame.font.Font(FONT_FILE_PATH, 30)
font_20 = pygame.font.Font(FONT_FILE_PATH, 20)
font_10 = pygame.font.Font(FONT_FILE_PATH, 10)
text_title = font_50.render("Dino Jump", True, BLACK)
text_ins = font_30.render("Click to Play", True, BLACK)
name_tag = font_10.render("Sasoun Torossian", True, BLACK)
pygame.display.set_caption("Dino Jump")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Game flow variables
game_finished = False
collision = False
first_run = True  # Indicates if game is being run for first time

# Jump variables
jump_flag = False
JUMP_ACC = -13  # How quickly Dino jumps and descends.

# Dino image list for walking
DINO_IMAGES = ['Dino_1.png', 'Dino_2.png']
updateDinoImage = pygame.USEREVENT+1

# Score variables
score = 0
hi_score = 0
updateScore = pygame.USEREVENT

# Cactus spawn interval, Replace with pygame.time.set_timer() at some point
spawn_counter = 0

# # Store speeding up mechanic (Needs to be implemented much later)
# cactus_speed = [4, 9]
# score_speed_threshold = 50


def draw_main_menu():
    screen.blit(text_title, [SIZE[0] / 2 - 130, SIZE[1] / 2 - 100])
    score_text = font_40.render("Score:" + str(score).zfill(5), True, BLACK)
    screen.blit(score_text, [SIZE[0] / 2 - 135, SIZE[1] / 2 - 30])
    screen.blit(text_ins, [SIZE[0] / 2 - 120, SIZE[1] / 2 + 40])
    screen.blit(name_tag, [SIZE[0] / 2 - 290, SIZE[1] / 2 + 135])
    pygame.display.flip()


def draw_score():
    if not hi_score:
        txt_score = font_20.render(str(score).zfill(5), True, OFF_GRAY)
        screen.blit(txt_score, [530, 15])
    else:
        # Two separate renders for colour contrast
        txt_hi_score = font_20.render("HI " + str(hi_score).zfill(5), True, OFF_LIGHT_GRAY)
        screen.blit(txt_hi_score, [430, 15])
        txt_score = font_20.render(str(score).zfill(5), True, OFF_GRAY)
        screen.blit(txt_score, [530, 15])


def check_collision():
    for i in range(len(cactus_arr)):
        if (dino.x + dino.width > cactus_arr[i].x) and \
                (dino.x < cactus_arr[i].x + cactus_arr[i].width) and \
                (dino.y < cactus_arr[i].y + cactus_arr[i].height) and \
                (dino.y + dino.height > cactus_arr[i].y):
            return True
        else:
            return False


class Dinosaur:
    def __init__(self, x=0, y=180, dx=4, dy=4, width=40, height=40, jump_acc=0, switch_image=0):
        self.image = pygame.image.load(DINO_IMAGES[0]).convert_alpha()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.jump_acc = jump_acc
        self.switch_image = switch_image

    # Creates walking animation when called every 100ms
    def switch_dino_image(self):
        self.switch_image = not self.switch_image
        self.image = pygame.image.load(DINO_IMAGES[self.switch_image]).convert_alpha()

    # Used to update the image of the Dino
    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    # Move Dino on x axis by amount defined by dx. Might not be needed.
    def move_x(self):
        self.x += self.dx

    # Move Dino on y axis by amount defined by dy
    def move_y(self):
        self.y += self.dy

    # Draw rectangle instead of image. Used for testing.
    def draw_rect(self):
        pygame.draw.rect(screen, [self.x, self.y, self.width, self.height], 0)

    def dino_jump(self):
        global jump_flag
        if self.jump_acc <= 13:
            self.dy = self.jump_acc
            self.move_y()
            self.draw_image()
            pygame.time.delay(15)
            self.jump_acc += 1
        else:
            jump_flag = False
            self.jump_acc = -13

    # Check if dino is out of screen boundaries. Might not be needed.
    # def check_out_of_screen(self):
    #     if self.x + self.width > 400 or self.x < 0:
    #         self.x -= self.dx


# Create a dino object
dino = Dinosaur(20, 180, 0, 0, 30, 40, JUMP_ACC)


class Cactus:
    def __init__(self, x, y, dx, dy, width, height, color):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.color = color

    # Load Cactus image. Create alpha channel for transparency
    def load_image(self, img):
        self.image = pygame.image.load(img).convert_alpha()
        # self.image.set_colorkey(BLACK)

    # Used to update the image of the Cactus
    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    # Move Cactus on x axis by amount defined by dx
    def move_x(self):
        self.x += self.dx

    # Move Cactus on y axis by amount defined by dy. Might not be needed.
    def move_y(self):
        self.y += self.dy

    # Draw rectangle instead of image. Used for testing.
    def draw_rect(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 0)

    # Check if Cactus is out of screen boundaries.
    def check_out_of_screen(self):
        if self.x + self.width > 400 or self.x < 0:
            self.x -= self.dx


''' Single instance of cactus that produces 
    cacti clones which go across the screen.
    can be a timer event like the score.
    list of cactus images, of different size
    play original, see how often they spawn.
    control spawn rate by semi-randomizing spawn_timer'''

# Setup the enemy cactus (PUT IN FUNC)
cactus_arr = []
# maximum of 5 cacti on screen
cactus_arr_max = 4


def reset_cactus_position():
    if len(cactus_arr) > 0:
        cactus_arr.clear()


def spawn_cactus_mod():
    if len(cactus_arr) >= cactus_arr_max:
        print("maximum number of cacti on screen")
    elif not len(cactus_arr):
        print("spawning first cactus")
        cactus = Cactus(600, 180, -4, 0, 30, 40, OFF_GRAY)
        cactus.load_image("Cactus.png")
        cactus.draw_image()
        # cactus.y = 180
        # cactus.x = random.randrange(600, 700)
        cactus_arr.append(cactus)
    else:
        if cactus_arr[-1].x < random.randint(10, 500):
            print("spawning cactus")
            print("position of previous cactus is {}".format(cactus_arr[-1].x))
            cactus = Cactus(600, 180, -4, 0, 30, 40, OFF_GRAY)
            # later, load from array of cactus shapes
            cactus.load_image("Cactus.png")
            cactus.draw_image()
            # cactus.y = 180
            # cactus.x = 600
            cactus_arr.append(cactus)
        else:
            pass
            # print("previous cactus not traveled far enough")


def move_cactus_mod():
    i = 0
    while i < len(cactus_arr):
        # print("moving cactus, current array length is {}".format(len(cactus_arr)))
        # print("position of cactus {} is {}".format(i, cactus_arr[i].x))
        cactus_arr[i].move_x()
        cactus_arr[i].draw_image()
        if cactus_arr[i].x < 0:
            # print("cactus {} out of bounds, removing from array".format(i))
            cactus_arr.pop(i)
            # print("new length of array is {}".format(len(cactus_arr)))
        i += 1


# Main loop for game
while not game_finished:
    # Called whenever there is event.
    for event in pygame.event.get():

        # User pressed 'X' button to quit.
        # Allows program to exit while and safely quit program
        if event.type == pygame.QUIT:
            game_finished = True

        # Reset everything when the user starts the game, or when they crash
        if (first_run or collision) and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
            pygame.time.set_timer(updateScore, 100)
            pygame.time.set_timer(updateDinoImage, 100)
            first_run = False
            collision = False
            reset_cactus_position()
            # NEED TO reset dino position too (because mid-jump)
            score = 0
            pygame.mouse.set_visible(False)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                jump_flag = True

        if event.type == updateScore:
            score += 1

        if event.type == updateDinoImage:
            dino.switch_dino_image()

    # Screen-clearing code goes here
    screen.fill(OFF_WHITE)

    # Drawing code should go here
    if first_run or collision:
        pygame.mouse.set_visible(True)
        pygame.time.set_timer(updateScore, 0)  # Stop score timer
        pygame.time.set_timer(updateDinoImage, 0)  # Stop dino walking animation
        if score > hi_score:  # Calculate hi score
            hi_score = score

        draw_main_menu()
    else:
        pygame.draw.line(screen, BLACK, (0, 200), (600, 200))  # Draw ground line.

        if jump_flag:
            dino.dino_jump()
        else:
            dino.draw_image()

        if spawn_counter == 5:
            spawn_cactus_mod()
            spawn_counter = 0
        else:
            spawn_counter += 1

        move_cactus_mod()

        #  Check the collision of the dino with the cactus
        collision = check_collision()

        # Draw the score.
        draw_score()

        # Updates entire surface display
        pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
