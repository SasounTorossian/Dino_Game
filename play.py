import pygame
import random
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (159, 163, 168)

pygame.init()

# Set the width and height of the screen [width, height]
size = (600, 300)
screen = pygame.display.set_mode(size)

# Load the fonts
font_40 = pygame.font.SysFont("Arial", 40, True, False)
font_30 = pygame.font.SysFont("Arial", 30, True, False)
font_10 = pygame.font.SysFont("Arial", 10, True, False)
text_title = font_40.render("Dino Jump", True, BLACK)
text_ins = font_30.render("Click to Play!", True, BLACK)
name_tag = font_10.render("Sasoun Torossian", True, BLACK)
pygame.display.set_caption("Dino Jump")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
collision = True
jump_flag = False
jump_acc = -13

# Store the score
score = 0


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


def check_collision(player_x, player_y, player_width, player_height, cac_x, cac_y, cac_width, cac_height):
    if (player_x + player_width > cac_x) and (player_x < cac_x + cac_width) and (player_y < cac_y + cac_height) and (
            player_y + player_height > cac_y):
        return True
    else:
        return False


def draw_main_menu():
    screen.blit(text_title, [size[0] / 2 - 106, size[1] / 2 - 100])
    score_text = font_40.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, [size[0] / 2 - 70, size[1] / 2 - 30])
    screen.blit(text_ins, [size[0] / 2 - 85, size[1] / 2 + 40])
    screen.blit(name_tag, [size[0] / 2 - 300, size[1] / 2 + 135])
    pygame.display.flip()


# Create a player object
player = Dinosaur(20, 180, 0, 0, 30, 40, BLACK)
player.load_image("Dino.png")


# Setup the enemy cactus (PUT IN FUNC)
cactus = []
cactus_count = 3
for i in range(cactus_count):
    cacti = Cactus(600, 180, -4, 0, 30, 40, BLACK)
    cactus.append(cacti)


# Figure out better way to set cactus position
def set_cactus_position():
    cactus[0].x = random.randrange(600, 650)
    for i in range(1, cactus_count):
        cactus[i].x = cactus[i - 1].x + random.randrange(50, 300)


def reset_cactus_position():
    cactus[0].x = random.randrange(600, 650)
    for i in range(1, cactus_count):
        cactus[i].x = cactus[i - 1].x + random.randrange(50, 300)


def move_cactus():
    for i in range(cactus_count):
        cactus[i].load_image("Cactus.png")
        cactus[i].draw_image()
        cactus[i].move_x()
        # Should implement  def check_out_of_screen(self) perhaps?
        if cactus[i].x < 0:
            cactus[i].y = 180
            cactus[i].x = random.randrange(600, 800)


# -------- Main Program Loop -----------

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Reset everything when the user starts the game.
        if collision and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
            collision = False
            set_cactus_position()
            pygame.mouse.set_visible(False)

        if not collision:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    # player.dy = -4
                    print("jump_flag = True")
                    jump_flag = True
                    # jump_dino()

            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
            #         player.dy = 0
            #         jump_dino()

    # Screen-clearing code goes here
    screen.fill(GRAY)

    # Drawing code should go here
    if not collision:
        pygame.draw.line(screen, BLACK, (0, 200), (600, 200))

        # player.draw_image()
        # player.move_y()
        # player.check_out_of_screen()

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
            # player.draw_rect()
            player.draw_image()

        # player.draw_rect()
        move_cactus()
        # player.check_out_of_screen()

        # # Check the collision of the player with the cactus
        for i in range(cactus_count):
            if check_collision(player.x, player.y, player.width, player.height,
                               cactus[i].x, cactus[i].y, cactus[i].width, cactus[i].height):
                collision = True
                pygame.mouse.set_visible(True)
                break

        # Draw the score.
        txt_score = font_30.render("Score: " + str(score), True, WHITE)
        screen.blit(txt_score, [15, 15])

        pygame.display.flip()
    else:
        draw_main_menu()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
