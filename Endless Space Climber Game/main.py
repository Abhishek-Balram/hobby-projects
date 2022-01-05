import pygame
import random
import os

# Constants - colours
PURPLE = (228, 0, 224)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0,)
YELLOW = (254, 226, 62)
GRAY = (75, 75, 75)

# Constants - general
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRAVITY = 0.1
MOUSE_WIDTH, MOUSE_HEIGHT = 40, 40
MIN_USERNAME_LENGTH = 1

# Constants - player
PLAYER_SPEED = 3
PLAYER_WIDTH, PLAYER_HEIGHT = 30, 52
PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT = 53, 83
PLAYER_Y_SPAWN = 300

# Constants - asteroids and stars
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
ASTEROID_SPRITE_WIDTH, ASTEROID_SPRITE_HEIGHT = 50, 50
ASTEROID_SPEED = 1
ASTEROID_OFFSET = 150
STAR_WIDTH, STAR_HEIGHT = 30, 30
STAR_CHANCE = 0.25

# initialising pygame and creating the game window
pygame.init()
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Space Climber")
clock = pygame.time.Clock()

# Fonts
USERNAME_FONT = pygame.font.SysFont("Default", 30)
BUTTON_FONT = pygame.font.SysFont("Arial", 80)
LARGE_BUTTON_FONT = pygame.font.SysFont("Arial", 90)
SCORE_FONT = pygame.font.SysFont("Default", 70)
TEXT_BOX_FONT = pygame.font.SysFont("Arial", 100)
TITLE_FONT = pygame.font.SysFont("Default", 100)

# Images
ASTRONAUT_LEFT_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("sprites", "walk_left.png")),
                                               (PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT)).convert_alpha()
ASTRONAUT_RIGHT_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("sprites", "walk_right.png")),
                                                (PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT)).convert_alpha()
ASTEROID_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("sprites", "asteroid.png")),
                                         (ASTEROID_SPRITE_WIDTH, ASTEROID_SPRITE_HEIGHT)).convert_alpha()
STAR_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("sprites", "star.png")),
                                     (STAR_WIDTH, STAR_HEIGHT)).convert_alpha()
MOUSE_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("sprites", "mouse.png")),
                                      (MOUSE_WIDTH, MOUSE_HEIGHT)).convert_alpha()
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("sprites", "background.png")),
                                          (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()


class Button(object):
    """A class to represent buttons"""

    buttons = []

    def __init__(self, x, y, label):
        """
       Constructs all the necessary attributes for the button object
       :param x: The x position of the button
       :param y: The y position of the button
       :param label: Text that describes the function of the button to users
       """
        self.x = x
        self.y = y
        self.width, self.height = BUTTON_FONT.size(label)[0], BUTTON_FONT.size(label)[1]
        self.label = label
        self.mouse_over = False
        Button.buttons.append(self)

    def draw(self):
        """ Draws the button object onto the pygame window."""

        if self.mouse_over:
            draw_text(self.label, (self.x, self.y), LARGE_BUTTON_FONT, YELLOW)
        else:
            draw_text(self.label, (self.x, self.y), BUTTON_FONT, WHITE)

    def check_clicked(self, mouse_pos, mouse_pressed):
        """
       Checks if the mouse is over the button or if the button is clicked. Adjusts position of the button as necessary.
       :param mouse_pos: The current (x, y) position of the mouse
       :param mouse_pressed: A bool value for whether or not the mouse-button is pressed
       :return: A bool value for whether or not the button has been clicked
       """
        # Check if the mouse is hovering over a button
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_pressed:  # Check if mouse is clicked
                return True
        else:
            self.mouse_over = False

        # Adjusting button size if the mouse is hovering over it (because it is enlarged now).
        if self.mouse_over:
            self.width, self.height = LARGE_BUTTON_FONT.size(self.label)[0], LARGE_BUTTON_FONT.size(self.label)[1]
        else:
            self.width, self.height = BUTTON_FONT.size(self.label)[0], BUTTON_FONT.size(self.label)[1]


class SolidObject(object):
    """A class to represent objects that have hit-boxes and can collide with each other"""

    players = []
    asteroids = []
    stars = []

    def __init__(self, x_pos, y_pos, width, height, sprite, sprite_width, sprite_height):
        """
       Constructs the necessary attributes of the solid object
       :param x_pos: The objects x-position
       :param y_pos: The objects y-position
       :param width: The objects hit-box width
       :param height: The objects hit-box height
       :param sprite: The objects sprite
       :param sprite_width: The width of the sprite (larger that hit-box width)
       :param sprite_height: The height of the sprite (larger than hit-box height)
       """
        self.x = x_pos
        self.y = y_pos
        self.x_vel = 0
        self.y_vel = 0
        self.width = width
        self.height = height
        self.sprite = sprite
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

    def update_pos(self):
        """Uses the objects velocities to move the object"""
        self.x += self.x_vel
        self.y += self.y_vel

    def draw_sprite(self):
        """Draws the objects sprite onto the pygame window"""
        sprite_x, sprite_y = centre_align(self.x, self.y, self.width, self.height, self.sprite_width,
                                          self.sprite_height)
        WINDOW.blit(self.sprite, (sprite_x, sprite_y))


class Player(SolidObject):
    """ A class that represents player characters. Is solid and can collide. """

    def __init__(self, x, y, username, player_num):
        """
       Constructs the necessary attributes of the player object
       :param x: x-position of the player character
       :param y: y-position of the player character
       :param username: players chosen username
       :param player_num: used to distinguish between players in two-player mode
       """
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT, ASTRONAUT_RIGHT_SPRITE, PLAYER_SPRITE_WIDTH,
                         PLAYER_SPRITE_HEIGHT)
        self.alive = True
        self.score = 0
        self.username = username
        self.standing_on_asteroid = False
        self.player_num = player_num
        SolidObject.players.append(self)

    def check_horizontal_collisions(self):
        """ Check for horizontal collisions with asteroids """

        # Create rect for the player hit-box
        player_destination = pygame.Rect(self.x + self.x_vel, self.y, self.width,
                                         self.height)

        # Looping through asteroids and checking for collisions between asteroid hit-box and player hit-box
        for asteroid in SolidObject.asteroids:
            asteroid_hit_box = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
            if player_destination.colliderect(asteroid_hit_box):
                # Move player until they are one pixel away from the asteroid then remove velocity so they don't collide
                if self.x_vel > 0:
                    while self.x + self.width + 1 < asteroid.x:
                        self.x += 1
                else:
                    while self.x - 1 > asteroid.x + asteroid.width:
                        self.x -= 1
                self.x_vel = 0

    def check_vertical_collisions(self):
        """ Check for vertical collisions with asteroids """

        # Create rect for the player hit-box
        player_destination = pygame.Rect(self.x, self.y + self.y_vel, self.width,
                                         self.height)

        # Loop through asteroids and check for collisions between asteroid hit-box and player hit-box
        for asteroid in SolidObject.asteroids:
            asteroid_hit_box = pygame.Rect(asteroid.x, asteroid.y, asteroid.width, asteroid.height)
            if player_destination.colliderect(asteroid_hit_box):
                # Move player until they are one pixel away from the asteroid then adjust velocity so they don't collide
                if self.y_vel > 0:
                    while self.y + self.height + 1 < asteroid.y:
                        self.y += 1
                    self.standing_on_asteroid = True
                else:
                    while self.y - 1 > asteroid.y + asteroid.height:
                        self.y -= 1
                self.y_vel = ASTEROID_SPEED

    def check_star_collisions(self):
        """ Check if the player is touching a star. If so, add to the their score. """
        for star in SolidObject.stars:
            star_hit_box = pygame.Rect(star.x, star.y, star.width, star.height)
            if star_hit_box.colliderect(pygame.Rect(self.x, self.y, self.width, self.height)):
                SolidObject.stars.remove(star)
                self.score += 50

    def check_boundary_collisions(self):
        """ Check and prevent the player from going off the screen boundaries. """

        # Right edge
        if self.x + self.width + self.x_vel > SCREEN_WIDTH:
            self.x_vel = 0
            while self.x + self.width + 1 <= SCREEN_WIDTH:
                self.x += 1

        # Left edge
        if self.x + self.x_vel < 0:
            self.x_vel = 0
            while self.x - 1 >= 0:
                self.x -= 1

        # Top edge
        if self.y + self.y_vel < 0:
            self.y_vel = 0
            while self.y - 1 >= 0:
                self.y -= 1

        # Bottom edge - if they go past the bottom edge they lose the game
        if self.y > SCREEN_HEIGHT:
            self.alive = False

    def handle_movement(self, keys_pressed):
        """ Move the player character based on which keys have been pressed """

        # Handling input
        if self.player_num == 1:
            right_key, left_key, jump_key = pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP
        else:
            right_key, left_key, jump_key = pygame.K_d, pygame.K_a, pygame.K_w

        if keys_pressed[left_key]:
            self.x_vel = -PLAYER_SPEED
            self.sprite = ASTRONAUT_LEFT_SPRITE
        if keys_pressed[right_key]:
            self.x_vel = PLAYER_SPEED
            self.sprite = ASTRONAUT_RIGHT_SPRITE
        if keys_pressed[jump_key] and self.standing_on_asteroid:
            self.y_vel = -PLAYER_SPEED * 2
        self.standing_on_asteroid = False

        # Check for collisions first, then update the players position and reset/adjust velocities
        self.check_vertical_collisions()
        self.check_horizontal_collisions()
        self.check_boundary_collisions()
        self.check_star_collisions()
        self.update_pos()
        self.x_vel = 0
        self.y_vel += GRAVITY

    def draw(self):
        """Draw the player sprite and username onto the pygame window"""

        username_size = USERNAME_FONT.size(self.username)
        username_x = self.x + (self.width - username_size[0]) // 2
        username_y = self.y - username_size[1] - 10
        draw_text(self.username, (username_x, username_y), USERNAME_FONT, WHITE)
        self.draw_sprite()


class Asteroid(SolidObject):
    """ A class that represents asteroids. They are solid and act as platforms that the player can jump to and from"""

    def __init__(self, x, y):
        """
       Construct the necessary attributes of the asteroid object.
       :param x: The asteroids x-position
       :param y: The asteroids y-position
       """
        super().__init__(x, y, ASTEROID_WIDTH, ASTEROID_HEIGHT, ASTEROID_SPRITE, ASTEROID_SPRITE_WIDTH,
                         ASTEROID_SPRITE_HEIGHT)
        self.y_vel = ASTEROID_SPEED
        SolidObject.asteroids.append(self)

    def handle_movement(self):
        """ Moves the asteroid and removes it from the game if it goes off the bottom of the screen"""

        self.update_pos()
        if self.y > SCREEN_HEIGHT:
            SolidObject.asteroids.remove(self)


class Star(SolidObject):
    """ A class that represents stars. They are solid and give the player points when they are touched"""

    def __init__(self, x, y):
        """
       Constructs the necessary attributes of the star object.
       :param x: The x-position of the star
       :param y: The y-position of the star
       """
        super().__init__(x, y, STAR_WIDTH, STAR_HEIGHT, STAR_SPRITE, STAR_WIDTH, STAR_HEIGHT)
        self.y_vel = ASTEROID_SPEED
        SolidObject.stars.append(self)

    def handle_movement(self):
        """ Moves the star object and removes it from the game if it goes below the bottom of the screen"""

        self.update_pos()
        if self.y > SCREEN_HEIGHT:
            SolidObject.stars.remove(self)


def draw_text(string, position, font, colour):
    """ Creates a surface with text and draws it onto the pygame window"""

    text = font.render(string, False, colour)
    WINDOW.blit(text, position)


def centre_align(x_pos, y_pos, width, height, image_width, image_height):
    """
   Carries out calculations to centre-align a sprite image with its hit-box.
   :param x_pos: The x-position of the hit-box
   :param y_pos: The y-position of the hit-box
   :param width: The width of the hit-box
   :param height: The height of the hit-box
   :param image_width: The width of the image
   :param image_height: The height of the image
   :return: The required x and y coordinates for the top-left corner of the image such that the image and hit-box are
   centre-aligned
   """
    image_x_pos = x_pos - (image_width - width) // 2
    image_y_pos = y_pos - (image_height - height) // 2
    return image_x_pos, image_y_pos


def get_username(prompt):
    """
   Displays a text-box and prompts the player to enter a username
   :param prompt: The text prompt that will be displayed in the text-box
   :return: The username that the player has entered
   """
    # Creating a pygame.Rect for the text-box
    text_box_width, text_box_height = int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.2)
    text_box = pygame.Rect(0, 0, text_box_width, text_box_height)
    text_box.centerx, text_box.centery = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    # Creating a pygame.Rect for the text-box outline
    outline_size = 10
    text_box_outline = pygame.Rect(0, 0, text_box_width + outline_size, text_box_height + outline_size)
    text_box_outline.centerx, text_box_outline.centery = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    # Creating a pygame.Rect for the text cursor
    blink_timer = 0
    display_cursor = True
    cursor = pygame.Rect(text_box.x, 0, 5, int(text_box.height * 0.8))
    cursor.centery = text_box.centery

    # Getting user input and updating username
    valid_characters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
    username = ""
    getting_input = True
    while getting_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN and len(username) >= MIN_USERNAME_LENGTH:
                    getting_input = False
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    username = username[:-1]
                elif event.unicode in valid_characters:
                    if TEXT_BOX_FONT.size(username + event.unicode)[0] < text_box.width:
                        username += event.unicode

        # updating the text that is displayed in the text box
        if len(username) == 0:
            text_string = prompt
            text_colour = GRAY
        else:
            text_string = username
            text_colour = WHITE

        # updating text cursor position and making it blink
        cursor.x = text_box.x + TEXT_BOX_FONT.size(username)[0]
        blink_timer += 1
        if blink_timer >= 360:
            blink_timer = 0
            display_cursor = not display_cursor

        # Drawing the frame
        WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
        pygame.draw.rect(WINDOW, YELLOW, text_box_outline)
        pygame.draw.rect(WINDOW, BLACK, text_box)
        if display_cursor:
            pygame.draw.rect(WINDOW, WHITE, cursor)
        draw_text(text_string, (text_box.x, text_box.y), TEXT_BOX_FONT, text_colour)
        pygame.display.update()

    return username


def start_menu():
    """
   Displays the main menu of the game where the player chooses the game mode they want to play.
   :return: The option from the menu that the user has selected.
   """

    # Creating title
    title_string = "Endless Space Climber"
    title_size = TITLE_FONT.size(title_string)
    title_x = (SCREEN_WIDTH - title_size[0]) // 2
    title_y = int(SCREEN_HEIGHT) * 0.05

    # Creating buttons and disabling default mouse cursor
    pygame.mouse.set_visible(False)
    Button.buttons = []
    button_labels = ["Single Player", "Two Player", "Quit"]
    button_y = SCREEN_HEIGHT // 2
    for label in button_labels:
        button_width = BUTTON_FONT.size(label)[0]
        button_x = (SCREEN_WIDTH - button_width) // 2
        Button(button_x, button_y, label)

        button_y += (SCREEN_HEIGHT // 2) // len(button_labels)

    # Loop until the player clicks an option from the menu
    looping = True
    while looping:
        mouse_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = True

        # Checking if any of the menu buttons are clicked
        mouse_pos = pygame.mouse.get_pos()
        for button in Button.buttons:
            if button.check_clicked(mouse_pos, mouse_pressed):
                if button.label == "Single Player":
                    return "Get 1 Username"
                elif button.label == "Two Player":
                    return "Get 2 Usernames"
                else:
                    return

        # Drawing frame onto the screen
        WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
        draw_text(title_string, (title_x, title_y), TITLE_FONT, PURPLE)
        for button in Button.buttons:
            button.draw()
        WINDOW.blit(MOUSE_SPRITE, mouse_pos)
        pygame.display.update()


def play_game(usernames):
    """
   Displays the game-environment where the player controls their character and plays the game.
   :param usernames: A list of usernames. The length of this list is used to distinguish between single and two player.
   :return: A bool value for whether or not the player has chosen to play again.
   """

    # Initial difficulty variables
    time_elapsed = 0
    asteroids_per_wave = 3

    # Creating player instances
    SolidObject.players = []
    two_player = len(usernames) == 2
    if two_player:
        player_one = Player(600, PLAYER_Y_SPAWN, usernames[0], 1)
        player_two = Player(600, PLAYER_Y_SPAWN, usernames[1], 2)
    else:
        player_one = Player(600, PLAYER_Y_SPAWN, usernames[0], 1)
        player_two = Player(0, 0, "", 2)

    # Creating asteroids and stars
    SolidObject.asteroids = []
    SolidObject.stars = []
    wave_y_pos = PLAYER_Y_SPAWN + PLAYER_HEIGHT
    while wave_y_pos > - ASTEROID_HEIGHT - (SCREEN_HEIGHT - PLAYER_Y_SPAWN):
        generate_asteroid_wave(wave_y_pos, asteroids_per_wave, False)
        wave_y_pos -= 150

    # Creating row of asteroids at the bottom so that players don't die at the start
    asteroid_x = 0
    for i in range(SCREEN_WIDTH // ASTEROID_SPRITE_WIDTH):
        Asteroid(asteroid_x, PLAYER_Y_SPAWN + PLAYER_HEIGHT)
        asteroid_x += ASTEROID_SPRITE_WIDTH

    # Keep playing until the win/lose conditions are met
    playing_game = True
    while playing_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Player movement
        keys_pressed = pygame.key.get_pressed()
        player_one.handle_movement(keys_pressed)
        player_two.handle_movement(keys_pressed)

        # Win/Lose conditions
        if two_player:
            if not player_one.alive:
                return end_game_screen("The winner was {}".format(player_two.username))
            elif not player_two.alive:
                return end_game_screen("The winner was {}".format(player_one.username))
        else:
            if not player_one.alive:
                return end_game_screen("Your score was {}".format(player_one.score))

        # Handling asteroids
        for asteroid in SolidObject.asteroids:
            asteroid.handle_movement()
        if len(SolidObject.asteroids) < 4 * asteroids_per_wave:
            generate_asteroid_wave(-ASTEROID_HEIGHT, asteroids_per_wave, not two_player)

        # Handling stars
        for star in SolidObject.stars:
            star.handle_movement()

        # Increasing difficulty over time
        time_elapsed += 1 / 60
        if time_elapsed > 120:
            asteroids_per_wave = 5
        elif time_elapsed > 45:
            asteroids_per_wave = 4

        # Drawing frame onto the screen
        WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
        for asteroid in SolidObject.asteroids:
            asteroid.draw_sprite()
        for star in SolidObject.stars:
            star.draw_sprite()
        player_one.draw()
        if two_player:
            player_two.draw()
        else:
            draw_text("Score: {}".format(player_one.score), (0, 0), SCORE_FONT, WHITE)
        pygame.display.update()

        # set the max frames per seconds
        clock.tick(FPS)


def generate_asteroid_wave(wave_y_pos, asteroid_quantity, spawn_stars):
    """
   Generates a row of asteroids that all have the same y-position, but have randomised x-positions. Each asteroid has
   a chance of having a star generated on top of it.
   :param wave_y_pos: The y-position that all the asteroids will share
   :param asteroid_quantity: The number of asteroids that will be generated
   :param spawn_stars: A bool value. If false, no stars will be generated on top of the asteroids.
   """

    # Calculating randomised x-positions and generating the asteroid
    asteroids_x = []
    new_asteroid_x = 0
    for i in range(asteroid_quantity):
        # Incrementing x-position by random amounts
        new_asteroid_x += SCREEN_WIDTH // asteroid_quantity - random.randint(-ASTEROID_OFFSET, ASTEROID_OFFSET)

        # Making sure x-position doesn't go off the screen
        if new_asteroid_x + ASTEROID_WIDTH >= SCREEN_WIDTH:
            new_asteroid_x -= SCREEN_WIDTH - ASTEROID_WIDTH

        # Making sure asteroids don't overlap with others
        for asteroid_x in asteroids_x:
            while new_asteroid_x + ASTEROID_WIDTH >= asteroid_x and new_asteroid_x < asteroid_x + ASTEROID_WIDTH:
                new_asteroid_x += ASTEROID_WIDTH

        # Generating asteroid
        asteroids_x.append(new_asteroid_x)
        Asteroid(new_asteroid_x, wave_y_pos)

        # Stars
        if spawn_stars:
            if random.randint(1, int(1 / STAR_CHANCE)) == int(1 / STAR_CHANCE):
                star_x, star_y = new_asteroid_x + (ASTEROID_SPRITE_WIDTH - STAR_WIDTH) // 2, wave_y_pos - STAR_HEIGHT
                Star(star_x, star_y)


def end_game_screen(message):
    """
   Displays a "Game Over" screen. Called from play_game() when the win/lose conditions are met.
   :param message: A string containing a message that will be displayed in the centre of the screen
   :return: A bool value for if the player wants to play again.
   """

    # Centre-aligning the message
    message_width, message_height = BUTTON_FONT.size(message)
    message_x, message_y = centre_align(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, 0, message_width, message_height)

    # Creating buttons for users to input what they want to do
    Button.buttons = []
    menu_button = Button(0, 0, "Go to Menu")
    retry_button = Button(0, 0, "Play Again")

    # Looping until the player clicks a button
    looping = True
    while looping:
        mouse_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = True

        # Checking if any of the buttons have been pressed
        mouse_pos = pygame.mouse.get_pos()
        if menu_button.check_clicked(mouse_pos, mouse_pressed):
            return False
        if retry_button.check_clicked(mouse_pos, mouse_pressed):
            return True

        # Adjusting button positions (because size changes if it is enlarged)
        menu_button.x = SCREEN_WIDTH - menu_button.width
        menu_button.y = SCREEN_HEIGHT - menu_button.height
        retry_button.y = SCREEN_HEIGHT - retry_button.height

        # Drawing the frame
        WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
        draw_text(message, (message_x, message_y), BUTTON_FONT, YELLOW)
        for button in Button.buttons:
            button.draw()
        WINDOW.blit(MOUSE_SPRITE, mouse_pos)
        pygame.display.update()


def main():
    """
   Tracks the current "state" of the game i.e. is it currently displaying Start Menu, getting username(s), or in game?
   Also controls the flow between different states based on what the user inputs.
   :return: Nil
   """
    game_state = "Start Menu"
    usernames = []
    program_running = True
    while program_running:
        if game_state == "Start Menu":
            usernames = []
            game_mode_choice = start_menu()
            game_state = game_mode_choice
        elif game_state == "Get 1 Username":
            usernames = [get_username("Enter username")]
            game_state = "In game"
        elif game_state == "Get 2 Usernames":
            usernames = [get_username("Player 1 name"), get_username("Player 2 name")]
            game_state = "In game"
        elif game_state == "In game":
            play_again = play_game(usernames)
            if not play_again:
                game_state = "Start Menu"
        else:
            quit()


main()
