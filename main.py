import random
import pygame
import sys
import os
from words import word_list

# Initialize Pygame
pygame.init()

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (126, 173, 204)

# Set up font
FONT = pygame.font.SysFont('Arial', 30)
SMALL_FONT = pygame.font.SysFont('Arial', 20)

# Set up the window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hangrybird')

# Path to the animation frames folder
ANIMATION_FRAMES_DIR = "animation_frames"  # Directory where your frames are stored

# Check if the frames directory exists
if not os.path.exists(ANIMATION_FRAMES_DIR):
    print(f"Error: {ANIMATION_FRAMES_DIR} does not exist!")
    sys.exit()

# Check if all the frames are present
for i in range(1, 4):  # We are expecting frame1.png, frame2.png, frame3.png
    frame_path = f"{ANIMATION_FRAMES_DIR}/frame{i}.png"
    if not os.path.exists(frame_path):
        print(f"Error: {frame_path} does not exist!")
        sys.exit()
    else:
        print(f"Found {frame_path}")

# Function to load all frames of animation
def load_animation_frames():
    frames = []
    # Loading 3 frames: frame1.png, frame2.png, and frame3.png
    for i in range(1, 4):  # We have 3 frames
        frame_path = f"{ANIMATION_FRAMES_DIR}/frame{i}.png"
        if os.path.exists(frame_path):
            frames.append(pygame.image.load(frame_path))
        else:
            print(f"Error: {frame_path} does not exist!")
            sys.exit()  # Exit if any frame is missing
    return frames

# Load the animation frames
animation_frames = load_animation_frames()

# Optionally scale the image/frames (adjust the width/height as needed)
def scale_animation_frame(image, width=600, height=450):
    """ Scales the image to a larger size. You can adjust width and height as needed. """
    return pygame.transform.scale(image, (width, height))  # Scale to fit the window

# Scale all animation frames to a larger size (increased size)
animation_frames = [scale_animation_frame(frame) for frame in animation_frames]

# Get the word for the game
def get_word():
    word = random.choice(word_list)
    return word.upper()

# Function to draw text
def draw_text(text, font, color, y_position, x_position=20):
    """ Function to draw text on the screen at a specific Y position, aligned to the left """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x_position, y_position))  # Align to top-left
    screen.blit(text_surface, text_rect)

# Main gameplay loop
def play(word):
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 8

    # Index for the current frame in the animation (if using multiple frames)
    frame_index = 0
    num_frames = len(animation_frames)

    # Time control for slowing down the animation (in milliseconds)
    frame_delay = 130  # Delay in milliseconds (500ms = 0.5s per frame)

    last_frame_time = pygame.time.get_ticks()  # Time of the last frame update

    # Game Loop
    while not guessed and tries > 0:
        screen.fill(WHITE)  # Clear the screen

        # Check if enough time has passed to change the frame
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time >= frame_delay:
            # Time passed, change frame
            frame_index = (frame_index + 1) % num_frames
            last_frame_time = current_time  # Reset the last frame time

        # Display the animation (cycle through the frames)
        screen.blit(animation_frames[frame_index], (100, 75))  # Position the frame (increased size)

        # Display the word and other game info at the bottom
        if not guessed and tries > 0:
            draw_text("Word: " + " ".join(word_completion), FONT, BLACK, 510)  # Word at the bottom
            draw_text("Incorrect guesses: " + ", ".join(guessed_letters), SMALL_FONT, BLACK, 560)
            draw_text(f"Tries left: {tries}", SMALL_FONT, BLACK, 10, x_position=20)
        
        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key).upper()

                if len(guess) == 1 and guess.isalpha():
                    if guess in guessed_letters:
                        continue
                    elif guess not in word:
                        tries -= 1
                        guessed_letters.append(guess)
                    else:
                        guessed_letters.append(guess)
                        word_as_list = list(word_completion)
                        indices = [i for i, letter in enumerate(word) if letter == guess]
                        for index in indices:
                            word_as_list[index] = guess
                        word_completion = "".join(word_as_list)

                        if "_" not in word_completion:
                            guessed = True
                elif len(guess) == len(word) and guess.isalpha():
                    if guess != word:
                        tries -= 1
                        guessed_words.append(guess)
                    else:
                        guessed = True
                        word_completion = word

        pygame.display.update()

    # Once the game ends, we hide the word and incorrect guesses and show the final message
    if guessed:
        # Display final message when the player wins
        draw_text(f"Good job the Bird is excited to try some {word}", FONT, BLUE, 450)
    else:
        # Display final message when the player loses
        draw_text(f"You lost the bird is hangry!! The word was {word}", FONT, RED, 450)

    pygame.display.update()
    pygame.time.wait(2000)

# Main function to start the game
def main():
    word = get_word()
    play(word)

    while True:
        draw_text("Wanna find some more food? (Y/N)", SMALL_FONT, BLACK, 50)
        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key).upper() == 'Y':
                        word = get_word()
                        play(word)
                        waiting_for_input = False
                    elif pygame.key.name(event.key).upper() == 'N':
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()