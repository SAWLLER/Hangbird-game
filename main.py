import random
import pygame
import sys
import os
from words import word_list

# For pygame 
pygame.init()

# Colors used for fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (126, 173, 204)

# Font set up 
FONT = pygame.font.SysFont('Arial', 30)
SMALL_FONT = pygame.font.SysFont('Arial', 20)

# Set up for the pygame window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hangrybird')

# This is for the animation frames
ANIMATION_FRAMES_DIR = "animation_frames"

# Check if the frames directory exists
if not os.path.exists(ANIMATION_FRAMES_DIR):
    print(f"Error: {ANIMATION_FRAMES_DIR} does not exist!")
    sys.exit()

# Load all frames of the main animation
def load_animation_frames():
    frames = []
    for i in range(1, 4):
        frame_path = f"{ANIMATION_FRAMES_DIR}/frame{i}.png"
        if os.path.exists(frame_path):
            frames.append(pygame.image.load(frame_path))
        else:
            print(f"Error: {frame_path} does not exist!")
            sys.exit()
    return frames

# Load winning animation frames
def load_winning_animation_frames():
    frames = []
    for i in range(4, 11):
        frame_path = f"{ANIMATION_FRAMES_DIR}/frame{i}.png"
        if os.path.exists(frame_path):
            frames.append(pygame.image.load(frame_path))
        else:
            print(f"Error: {frame_path} does not exist!")
            return frames
    print(f"Loaded {len(frames)} winning frames.")
    return frames

# Load losing animation frames
def load_losing_animation_frames():
    frames = []
    for i in range(11, 20):
        frame_path = f"{ANIMATION_FRAMES_DIR}/frame{i}.png"
        if os.path.exists(frame_path):
            frames.append(pygame.image.load(frame_path))
        else:
            print(f"Error: {frame_path} does not exist!")
            return frames
    print(f"Loaded {len(frames)} losing frames.")
    return frames

# Load the animation frames
animation_frames = load_animation_frames()
winning_animation_frames = load_winning_animation_frames()
losing_animation_frames = load_losing_animation_frames()

# Scale frames for display
def scale_animation_frame(image, width=600, height=450):
    return pygame.transform.scale(image, (width, height))

animation_frames = [scale_animation_frame(frame) for frame in animation_frames]
winning_animation_frames = [scale_animation_frame(frame) for frame in winning_animation_frames]
losing_animation_frames = [scale_animation_frame(frame) for frame in losing_animation_frames]

# Get a random word
def get_word():
    return random.choice(word_list).upper()

# Draw text on the screen
def draw_text(text, font, color, y_position, x_position=20):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x_position, y_position))
    screen.blit(text_surface, text_rect)

# Function to play winning animation
def play_winning_animation(rounds_won, total_rounds):
    frame_index = 0
    num_frames = len(winning_animation_frames)
    frame_delay = 130
    last_frame_time = pygame.time.get_ticks()

    if num_frames == 0:
        print("No winning frames to display.")
        return

    while True:
        screen.fill(WHITE)  # Clear screen before drawing

        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time >= frame_delay:
            frame_index = (frame_index + 1) % num_frames
            last_frame_time = current_time

        # Draw the current frame
        screen.blit(winning_animation_frames[frame_index], (100, 75))

        # Draw final score above the winning animation
        draw_text(f"Final score: {rounds_won} out of {total_rounds}", FONT, BLACK, 20)  
        draw_text("Wanna find some more food? (Y/N)", SMALL_FONT, BLACK, 450)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key).upper() == 'Y':
                    return True  # Continue playing
                elif pygame.key.name(event.key).upper() == 'N':
                    pygame.quit()
                    sys.exit()

# Function to play losing animation
def play_losing_animation(word):
    frame_index = 0
    num_frames = len(losing_animation_frames)
    frame_delay = 130
    last_frame_time = pygame.time.get_ticks()

    if num_frames == 0:
        print("No losing frames to display.")
        return

    while True:
        screen.fill(WHITE)  # Clear screen before drawing

        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time >= frame_delay:
            frame_index = (frame_index + 1) % num_frames
            last_frame_time = current_time

        # Draw the current frame
        screen.blit(losing_animation_frames[frame_index], (100, 75))
        draw_text(f"The bird is fuming! The word was {word}.", FONT, RED, 480)
        draw_text("Do you want to try again? (Y/N)", FONT, RED, 530)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key).upper() == 'Y':
                    return True  # Restart the game
                elif pygame.key.name(event.key).upper() == 'N':
                    pygame.quit()
                    sys.exit()

# Main gameplay loop
def play(word):
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    tries = 6
    score = 0  # Initialize score
    frame_index = 0
    num_frames = len(animation_frames)
    frame_delay = 130
    last_frame_time = pygame.time.get_ticks()

    while not guessed and tries > 0:
        screen.fill(WHITE)

        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time >= frame_delay:
            frame_index = (frame_index + 1) % num_frames
            last_frame_time = current_time

        screen.blit(animation_frames[frame_index], (100, 75))

        if not guessed and tries > 0:
            draw_text("Word: " + " ".join(word_completion), FONT, BLACK, 510)
            draw_text("Incorrect guesses: " + ", ".join(guessed_letters), SMALL_FONT, BLACK, 560)
            draw_text(f"Tries left: {tries}", SMALL_FONT, BLACK, 10, x_position=20)
            draw_text(f"Score: {score}", SMALL_FONT, BLACK, 10, x_position=600)  # Display score

        pygame.display.update()

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
                        score += 10  # Increment score for each correct letter

                        if "_" not in word_completion:
                            guessed = True
                elif len(guess) == len(word) and guess.isalpha():
                    if guess != word:
                        tries -= 1
                    else:
                        guessed = True
                        word_completion = word
                        score += 50  # Bonus score for guessing the whole word

    if guessed:
        return True  # Indicate win
    else:
        play_losing_animation(word)  # Play losing animation
        return False  # Indicate loss

# Main function to start the game
def main():
    while True:  # Loop for multiple rounds
        rounds_won = 0
        total_rounds = 3

        for _ in range(total_rounds):
            word = get_word()
            if play(word):
                rounds_won += 1  # Increment score if the player guessed the word
            else:
                break  # Exit the loop if the player chooses not to play again

        # Play winning animation if rounds_won is greater than 0
        if rounds_won > 0:
            play_winning_animation(rounds_won, total_rounds)

if __name__ == "__main__":
    main()
