import random
import pygame

# TODO: Organize files into folder (assets)
# TODO: Organize GUI into single class? (online examples) (Inherit from GameEngine)
# TODO: Game engine wrapper class for handling
# TODO: Clean up globals. Put into GUI or GameEngine class
# TODO: After Refactor, figure out new features.
# TODO: Expand screen size?
# TODO: Open in center of screen?

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
# TODO: Why not just use collision flag
first_run = True  # Indicates if game is being run for first time
# Used to lock other events while in main menu
event_lock = True  # Come up with better solution.

# Dino image list for walking. Add animation when dino collides.
updateDinoImage = pygame.USEREVENT+1

# Score variables
score = 0
hi_score = 0
updateScore = pygame.USEREVENT

# Cactus spawn interval, Replace with pygame.time.set_timer() at some point
spawn_counter = 0
spawnCactus = pygame.USEREVENT+2
moveCactus = pygame.USEREVENT+3

# # Store speeding up mechanic (Needs to be implemented much later)
# cactus_speed = [4, 9]
# score_speed_threshold = 50


# TODO: Put all into GUI class. Different screens will inherit?
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


class Object():
    def __init__(self, x, y, dx, dy, width, height, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height

    def load_image(self, image):
        self.image = pygame.image.load(image).convert_alpha()

    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        self.x += self.dx

    def move_y(self):
        self.y += self.dy

    def move_asset(self):
        self.move_x()
        self.move_y()
        self.draw_image()

    # Draw rectangle instead of image. Used for testing.
    def draw_rect(self):
        pygame.draw.rect(screen, [self.x, self.y, self.width, self.height], 0)

    @classmethod
    def check_collision(cls, dino, cactus_arr):
        for i in range(len(cactus_arr)):
            if (dino.x + dino.width > cactus_arr[i].x) and \
                    (dino.x < cactus_arr[i].x + cactus_arr[i].width) and \
                    (dino.y < cactus_arr[i].y + cactus_arr[i].height) and \
                    (dino.y + dino.height > cactus_arr[i].y):
                return True
            return False


class Dinosaur(Object):
    dino_images = ['Dino_1.png', 'Dino_2.png']

    def __init__(self, x=20, y=180, dx=0, dy=0, width=30, height=40,
                 jump_acc=-13, switch_image=0, jump_flag=False):
        super().__init__(x, y, dx, dy, width, height, Dinosaur.dino_images[0])
        self.jump_acc = jump_acc
        self.switch_image = switch_image
        self.jump_flag = jump_flag

    def reset_dino_position(self):
        self.x = 20
        self.y = 180
        self.jump_acc = -13
        self.jump_flag = False
        self.dy = 0

    def switch_dino_image(self):
        self.switch_image = not self.switch_image
        super().load_image(Dinosaur.dino_images[self.switch_image])

    # TODO: HAS to be a better/nicer way of doing this.
    def dino_move(self):
        if self.jump_flag:
            if self.jump_acc <= 13:
                self.dy = self.jump_acc
                self.jump_acc += 1
            else:
                self.jump_flag = False
                self.dy = 0
                self.jump_acc = -13

        super().move_asset()


# Create a Dinosaur object
dino = Dinosaur()


class Cactus(Object):
    spawn_time = [500, 700, 1000, 1200, 1500, 1700, 1900, 2300]

    def __init__(self, width, height, image, x=600, y=180, dx=-4, dy=0):
        super().__init__(x, y, dx, dy, width, height, image)

    @classmethod
    def reset_cactus_position(cls, cactus_arr):
        if len(cactus_arr) > 0:
            cactus_arr.clear()

    @classmethod
    def spawn_cactus(cls, cactus_arr):
        cactus = Cactus(30, 40, 'Cactus.png')
        cactus_arr.append(cactus)

    # TODO: Review later.
    @classmethod
    def move_cactus(cls, cactus_arr):
        for i, cacti in enumerate(cactus_arr):
            super(Cactus, cacti).move_asset()
            if cacti.x < 0:
                cactus_arr.pop(i)


# Create cactus array to store Cactus class instances
cactus_arr = []

# Main loop for game
while not game_finished:
    # Called whenever there is event.
    # TODO: Put all this into GameEngine wrapper.
    for event in pygame.event.get():

        # User pressed 'X' button to quit.
        # Allows program to exit while and safely quit program
        if event.type == pygame.QUIT:
            game_finished = True

        # Reset everything when the user starts the game, or when they crash
        if (first_run or collision) and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
            pygame.time.set_timer(updateScore, 100)
            pygame.time.set_timer(updateDinoImage, 100)
            pygame.time.set_timer(spawnCactus, 1000)
            pygame.mouse.set_visible(False)
            first_run = False
            collision = False
            score = 0
            Cactus.reset_cactus_position(cactus_arr)
            dino.reset_dino_position()

        if event.type == pygame.KEYDOWN and not event_lock:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                dino.jump_flag = True

        if event.type == updateScore and not event_lock:
            score += 1

        if event.type == updateDinoImage and not event_lock:
            dino.switch_dino_image()

        if event.type == spawnCactus and not event_lock:
            Cactus.spawn_cactus(cactus_arr)
            pygame.time.set_timer(spawnCactus, Cactus.spawn_time[random.randint(0, len(Cactus.spawn_time)-1)])

    # Screen-clearing code goes here
    screen.fill(OFF_WHITE)

    # Drawing code should go here
    if first_run or collision:
        event_lock = True
        pygame.mouse.set_visible(True)
        pygame.time.set_timer(updateScore, 0)  # Stop score timer
        pygame.time.set_timer(updateDinoImage, 0)  # Stop dino walking animation
        if score > hi_score:  # Calculate hi score
            hi_score = score

        draw_main_menu()
    else:
        event_lock = False
        pygame.draw.line(screen, BLACK, (0, 200), (600, 200))  # Draw ground line.

        dino.dino_move()
        Cactus.move_cactus(cactus_arr)

        collision = Object.check_collision(dino, cactus_arr)

        # Draw the score.
        draw_score()

        # Updates entire surface display
        pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
