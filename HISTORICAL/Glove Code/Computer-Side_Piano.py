# Import modules
# Attempt to import pygame
try:
    import pygame
except ModuleNotFoundError as e:
    print("Missing pygame library!")
    raise e
# Attempt to import pySerial
try:
    import serial
except ModuleNotFoundError as e:
    print("Missing pySerial library!")
    raise e


# Declare functions
def load_icon():
    """Loads the window icon"""
    # Necessary libraries for decoding and decompressing
    from zlib import decompress
    from base64 import b64decode

    # Decode and decompress the icon from a byte string
    compressed_icon = '''eJzt2y9Lg1EYhvFHHAaNVhGsWmYwG/wIFpP7CAYtgghmmyaTVQST4ILRok3FZhMMBvEPiJjmfXgH4hDcdo7nzHOuG66y9Pz
                         C2DvYzBhjbCB3pI7b7SS+JcXeVavdVeJbUgw/fvz48ePHX97w48ePHz9+/OUNP378+PHjx1/e8OPHjx8/fvzlDT9+/Pjx5+
                         0fUmNquOP1XP0zas2q3zfeqherrK571VTr6sPy8ddUQ13Yl/W3WpaHf15dW/fuXPzufb2p3qx3+3/3O/uu9ef+yX8X93zvr
                         ZqfvbPzuOd7bVI9W1j/YVSB37YsrN3ViCrw26mFtd+okagCv51ZOPuTmot7vvfcf1VC2B/VQuTbQ2zavj/T9tOlqsc+POCW
                         1Kv17n5QG2o0/snBN6tOrDu3+16wosaTXPq3m1LLalvtqwO1Z9Xn5KKaSHcaY6zUfQLcm4sg'''
    decoded_icon = b64decode(compressed_icon)
    icon_string = decompress(decoded_icon)

    # Load the image data as a pygame surface and return the result
    return pygame.image.fromstring(icon_string, (64, 64), 'RGBA')


def play_note(key):
    """Plays a particular key"""
    print(f"Played note {i} (Notes/note{i+1}.wav)")
    global notes
    notes[key].stop()
    notes[key].play()
    notes[key].fadeout(3000)


# Ask for port
port = input("Enter port for Arduino (ex: COM4): ")


# Initialize pygame
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.init()

# Get the mixer ready and load the notes from file
pygame.mixer.set_num_channels(26)
#notes = [pygame.mixer.Sound(f"Notes/note{12-i+1}.wav") for i in range(13)]


# Display window setup
win_width = 64*16
win_height = 64*9
win = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
pygame.display.set_caption("Larger Than Life Piano")

# Load window icon
icon = load_icon()
pygame.display.set_icon(icon)

# Declare keyboard state array
#key_states = list(False for i in range(13))

# Declare rectangle array representing the keys
# I am sorry for this
key_rects = [None for i in range(13)]
key_colors = [None for i in range(13)]
key_states = [None for i in range(13)]
notes = [None for i in range(13)]
# Black keys
for i, note_id in zip(range(1, 4), (3, 5, 7)):
    key_rects[note_id-1] = pygame.Rect(16*9-((i+1)*16), 20, 8, 60)
    key_colors[note_id-1] = (0, 0, 0)
    key_states[note_id-1] = False
    notes[note_id-1] = pygame.mixer.Sound(f"Notes/note{note_id}.wav")
for i, note_id in zip(range(0, 2), (10, 12)):
    key_rects[note_id-1] = pygame.Rect(16*9-((i+1)*16+5*16), 20, 8, 60)
    key_colors[note_id-1] = (0, 0, 0)
    key_states[note_id-1] = False
    notes[note_id-1] = pygame.mixer.Sound(f"Notes/note{note_id}.wav")
# White keys
for i, note_id in zip(range(8), (1, 2, 4, 6, 8, 9, 11, 13)):
    key_rects[note_id-1] = pygame.Rect(16*9-((i+1)*16), 16, 16, 64)
    key_colors[note_id-1] = (255, 255, 255)
    key_states[note_id-1] = False
    notes[note_id-1] = pygame.mixer.Sound(f"Notes/note{note_id}.wav")

# Declare key color array
#key_colors = list((255, 255, 255) for i in range(13))

# Set up internal window, sized for the keys
win2 = pygame.Surface((16*(8+2), 64+16*2))


# Main loop
running = True
connected = False
arduino = None
user_pressed_key = None
fullscreen = False
while running:
    # Attempt to connect to Arduino over serial (if not already connected)
    if not connected:
        try:
            arduino = serial.Serial(port, 9600, timeout=0.1)
        except serial.SerialException:
            pass
        else:
            connected = True
            
    # Handle events
    for event in pygame.event.get():
        # Program quit event
        if event.type == pygame.QUIT:
            running = False

        # Window resize event
        if event.type == pygame.VIDEORESIZE:
            new_w, new_h = event.w, event.h
            win = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
            win_width = new_w
            win_height = new_h

        # Mouse button pressed - user clicked on keyboard key via program
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position and convert to internal window coordinates
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x_prime = int(mouse_x * win2.get_width() / win.get_width())
            y_prime = int(mouse_y * win2.get_height() / win.get_height())

            # Find the top-level key the user clicked on, if any
            found_key = None
            for i, rect in enumerate(reversed(key_rects)):
                if rect.collidepoint(x_prime, y_prime):
                    found_key = 12-i
                    user_pressed_key = found_key
                    break

            # Play note, if applicable
            if found_key is not None:
                # Ignore key press if it's already being pressed
                if key_states[found_key]:
                    found_key = None
                else:
                    key_states[found_key] = True
                    play_note(found_key)

        # Mouse button released - user released key
        if event.type == pygame.MOUSEBUTTONUP:
            if user_pressed_key is not None:
                key_states[user_pressed_key] = 0
            user_pressed_key = None

        # Keyboard key pressed
        if event.type == pygame.KEYDOWN:
            # Escape key - toggle fullscreen
            if event.key == pygame.K_ESCAPE:
                if fullscreen:
                    win = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
                    fullscreen = False
                else:
                    win = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE | pygame.FULLSCREEN)
                    fullscreen = True

    # Handle serial (if connected)
    if connected:
        # Read in all messages
        msg = arduino.readline().decode()
        for sub_msg in msg.split("\n"):
            result = sub_msg.split("|")
            if result[0] == "keyDown":
                pressed_key = int(result[1])
                # Ignore key press if it's already being pressed
                if not key_states[pressed_key]:
                    key_states[pressed_key] = True
                    play_note(pressed_key)
            elif result[0] == "keyUp":
                pressed_key = int(result[1])
                # Ignore key release if it's not already being pressed
                if key_states[pressed_key]:
                    key_states[pressed_key] = False

    # Update screen
    for key_state, key_rect, key_color in zip(key_states, key_rects, key_colors):
        # Active keys are drawn in red.  Otherwise, they're drawn in white.
        if key_state:
            color = (255, 128, 128)
        else:
            color = key_color

        pygame.draw.rect(win2, color, key_rect)
        pygame.draw.line(win2, (0, 0, 0), key_rect.topleft, key_rect.bottomleft)

    # Draw internal rectangle to display and blit
    pygame.transform.scale(win2, (win.get_width(), win.get_height()), win)

    # Add Arduino connection indicator
    pygame.draw.rect(win,
                     (0, 255, 0) if connected else (255, 0, 0),
                     (0, 0, 32, 32))

    # Update screen
    pygame.display.flip()

# Close pygame
pygame.quit()
