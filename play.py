import pygame
import random
import time

# Define some colors
BLACK = (0, 0, 0)
OFF_WHITE = (225, 225, 225)
OFF_GRAY = (80, 80, 80)
OFF_LIGHT_GRAY = (115, 115, 115)

pygame.init()

# Set the width and height of the screen [width, height]
size = (600, 300)
screen = pygame.display.set_mode(size)

# 8-bit Font file path
font_file_path = "C:\\Users\\Sasoun\\Documents\\Software Workspace\\PycharmProjects\\Dino_Game\\VCR_OSD_MONO_1.001.ttf"

# Load the fonts
font_50 = pygame.font.Font(font_file_path, 50)
font_40 = pygame.font.Font(font_file_path, 40)
font_30 = pygame.font.Font(font_file_path, 30)
font_20 = pygame.font.Font(font_file_path, 20)
font_10 = pygame.font.Font(font_file_path, 10)
text_title = font_50.render("Dino Jump", True, BLACK)
text_ins = font_30.render("Click to Play", True, BLACK)
name_tag = font_10.render("Sasoun Torossian", True, BLACK)
pygame.display.set_caption("Dino Jump")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Game flow variables
done = False
collision = True
first_run = 1

# Jump variables
jump_flag = False
jump_acc = -13

# Score variables
score = 0
hi_score = 0
updateScore = pygame.USEREVENT

# Cactus spawn interval, Replace with pygame.time.set_timer() at some point
spawn_time = 0

# # Store speeding up mechanic (Needs to be implemented much later)
# cactus_speed = [4, 9]
# score_speed_threshold = 50


class Dinosaur:
    def __init__(self, x=0, y=180, dx=4, dy=4, width=40, height=40, color=BLACK):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.color = color

    def load_image(self, img):
        self.image = pygame.image.load(img).convert_alpha()
        # self.image.set_colorkey(BLACK)

    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        self.x += self.dx

    def move_y(self):
        self.y += self.dy

    def draw_rect(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 0)

    def check_out_of_screen(self):
        if self.x + self.width > 400 or self.x < 0:
            self.x -= self.dx


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

    def load_image(self, img):
        self.image = pygame.image.load(img).convert_alpha()
        self.image.set_colorkey(BLACK)

    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        self.x += self.dx

    def move_y(self):
        self.y += self.dy

    def draw_rect(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 0)

    def check_out_of_screen(self):
        if self.x + self.width > 400 or self.x < 0:
            self.x -= self.dx


def check_collision(player_x, player_y, player_width, player_height, cac_x, cac_y, cac_width, cac_height):
    if (player_x + player_width > cac_x) and (player_x < cac_x + cac_width) and (player_y < cac_y + cac_height) and (
            player_y + player_height > cac_y):
        return True
    else:
        return False


def draw_main_menu():
    screen.blit(text_title, [size[0] / 2 - 130, size[1] / 2 - 100])
    score_text = font_40.render("Score:" + str(score).zfill(5), True, BLACK)
    screen.blit(score_text, [size[0] / 2 - 135, size[1] / 2 - 30])
    screen.blit(text_ins, [size[0] / 2 - 120, size[1] / 2 + 40])
    screen.blit(name_tag, [size[0] / 2 - 290, size[1] / 2 + 135])
    pygame.display.flip()


# Create a player object
player = Dinosaur(20, 180, 0, 0, 30, 40, OFF_GRAY)
player.load_image("Dino.png")

# Setup the enemy cactus (PUT IN FUNC)
cactus_arr = []
# maximum of 5 cacti on screen
cactus_arr_max = 5
# for i in range(cactus_count):
#
#     cactus.append(cacti)
# cactus = Cactus(600, 180, -4, 0, 30, 40, BLACK)


# Figure out better way to set cactus position
# def set_cactus_position():
#     cactus[0].x = random.randrange(600, 650)
#     for i in range(1, cactus_count):
#         cactus[i].x = cactus[i - 1].x + random.randrange(50, 300)


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
            print("position of previous cactus is {}".format(cactus_arr[-1].x ))
            cactus = Cactus(600, 180, -4, 0, 30, 40, OFF_GRAY)
            # later, load from array of cactus shapes
            cactus.load_image("Cactus.png")
            cactus.draw_image()
            # cactus.y = 180
            # cactus.x = 600
            cactus_arr.append(cactus)
        else:
            print("previous cactus not traveled far enough")


# def spawn_cactus():
#     print("spawning cactus")
#     cactus.load_image("Cactus.png")
#     cactus.draw_image()
#     # cactus.move_x()
#     cactus.y = 180
#     cactus.x = random.randrange(600, 700)


def move_cactus():
    # after deleting first element, array size is reduce, but still trying to access last index which doesn't exist.
    for i in range(len(cactus_arr)):
        # print("moving cactus, current array length is {}".format(len(cactus_arr)))
        # print("position of cactus {} is {}".format(i, cactus_arr[i].x))
        cactus_arr[i].move_x()
        cactus_arr[i].draw_image()
        if cactus_arr[i].x < 0:
            # print("cactus {} out of bounds, removing from array".format(i))
            cactus_arr.pop(i)
            # print("new length of array is {}".format(len(cactus_arr)))


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


# def update_score():
#     global score
#     score += 1

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        # Reset everything when the user starts the game.
        if collision and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
            pygame.time.set_timer(updateScore, 100)
            collision = False
            reset_cactus_position()
            # NEED TO reset dino position too (because mid-jump)
            # set_cactus_position()
            # spawn_cactus()#
            score = 0
            pygame.mouse.set_visible(False)

        if not collision:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    # player.dy = -4
                    print("jump_flag = True")
                    jump_flag = True
                    # jump_dino()

        if event.type == updateScore:
            score += 1

            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
            #         player.dy = 0
            #         jump_dino()

    # Screen-clearing code goes here
    screen.fill(OFF_WHITE)

    # Drawing code should go here
    if not collision:
        pygame.draw.line(screen, BLACK, (0, 200), (600, 200))

        # NEED TO COME UP WITH BETTER SOLUTION FOR JUMPING MECHANISM
        if jump_flag:
            if jump_acc < 0:
                print("jumps < 0")
                player.dy = jump_acc
                player.move_y()
                # player.draw_rect()
                player.draw_image()
                pygame.time.delay(20)
                jump_acc += 1
            elif 0 <= jump_acc <= 13:
                print("jumps >= 0")
                player.dy = jump_acc
                player.move_y()
                # player.draw_rect()
                player.draw_image()
                pygame.time.delay(20)
                jump_acc += 1
            elif jump_acc > 13:
                print("jumps > 13")
                player.dy = 0
                player.move_y()
                # player.draw_rect()
                player.draw_image()
                pygame.time.delay(20)
                jump_flag = False
                jump_acc = -13
            else:
                jump_flag = False
                jump_acc = -13
        else:
            player.draw_image()

        if spawn_time == 5:
            spawn_cactus_mod()
            spawn_time = 0
        else:
            spawn_time += 1

        move_cactus_mod()

        #  Check the collision of the player with the cactus
        for i in range(len(cactus_arr)):
            if check_collision(player.x, player.y, player.width, player.height,
                               cactus_arr[i].x, cactus_arr[i].y, cactus_arr[i].width, cactus_arr[i].height):
                collision = True
                pygame.mouse.set_visible(True)
                break

        # Draw the score.
        if not hi_score:
            txt_score = font_20.render(str(score).zfill(5), True, OFF_GRAY)
            screen.blit(txt_score, [530, 15])
        else:
            # Two separate renders for colour contrast
            txt_hi_score = font_20.render("HI " + str(hi_score).zfill(5), True, OFF_LIGHT_GRAY)
            screen.blit(txt_hi_score, [430, 15])
            txt_score = font_20.render(str(score).zfill(5), True, OFF_GRAY)
            screen.blit(txt_score, [530, 15])

        pygame.display.flip()
    else:
        # Stop the score timer
        pygame.time.set_timer(updateScore, 0)
        if score > hi_score:
            hi_score = score

        draw_main_menu()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
