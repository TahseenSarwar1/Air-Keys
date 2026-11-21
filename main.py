import cv2
import mediapipe as mp
import pygame
import numpy as np
import math
import sys


# ==========================================
# 1. CONFIGURATION
# ==========================================

WIDTH = 1000
HEIGHT = 600
FPS = 60

CAMERA_INDEX = 0

WHITE_KEYS = 7
KEY_WIDTH = 100
KEY_HEIGHT = 250

PIANO_X = (WIDTH - WHITE_KEYS * KEY_WIDTH) // 2
PIANO_Y = 300

PINCH_THRESHOLD = 0.08

NOTES = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,
}

BLACK_KEYS = {
    "C#4": 277.18,
    "D#4": 311.13,
    "F#4": 369.99,
    "G#4": 415.30,
    "A#4": 466.16,
}

BLACK_KEY_POSITIONS = [0, 1, 3, 4, 5]


# ==========================================
# 2. INITIALIZE PYGAME
# ==========================================

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Piano")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)


# ==========================================
# 3. GENERATE PIANO SOUNDS
# ==========================================

def generate_sound(frequency):
    sample_rate = 44100
    duration = 1.0

    samples = np.arange(int(sample_rate * duration))

    wave = np.sin(
        2 * np.pi * frequency * samples / sample_rate
    )

    # Add a simple fade-out to reduce clicking
    envelope = np.linspace(1.0, 0.0, len(samples))

    wave = wave * envelope

    audio = (wave * 12000).astype(np.int16)

    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)


pygame.mixer.init(frequency=44100, size=-16, channels=2)

SOUNDS = {}

for note, frequency in {**NOTES, **BLACK_KEYS}.items():
    SOUNDS[note] = generate_sound(frequency)


# ==========================================
# 4. INITIALIZE MEDIAPIPE
# ==========================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)


# ==========================================
# 5. INITIALIZE CAMERA
# ==========================================

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("Camera could not be opened!")
    sys.exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# ==========================================
# 6. PIANO KEY GENERATION
# ==========================================

def get_piano_keys():

    keys = []

    for i, note in enumerate(NOTES):

        x = PIANO_X + i * KEY_WIDTH

        rect = pygame.Rect(
            x,
            PIANO_Y,
            KEY_WIDTH,
            KEY_HEIGHT
        )

        keys.append({
            "note": note,
            "rect": rect,
            "black": False
        })

    for position, note in zip(
        BLACK_KEY_POSITIONS,
        BLACK_KEYS
    ):

        x = PIANO_X + (position + 1) * KEY_WIDTH - 25

        rect = pygame.Rect(
            x,
            PIANO_Y,
            50,
            150
        )

        keys.append({
            "note": note,
            "rect": rect,
            "black": True
        })

    return keys


PIANO_KEYS = get_piano_keys()


# ==========================================
# 7. FIND WHICH KEY IS UNDER THE FINGER
# ==========================================

def find_key(x, y):

    # Check black keys first because they overlap white keys
    for key in PIANO_KEYS:

        if key["black"] and key["rect"].collidepoint(x, y):
            return key["note"]

    for key in PIANO_KEYS:

        if not key["black"] and key["rect"].collidepoint(x, y):
            return key["note"]

    return None


# ==========================================
# 8. DRAW PIANO
# ==========================================

def draw_piano(hovered_key, active_key):

    screen.fill((25, 28, 40))

    title = font.render(
        "VIRTUAL PIANO",
        True,
        (255, 255, 255)
    )

    screen.blit(title, (WIDTH // 2 - 100, 40))

    instructions = small_font.render(
        "Move index finger over a key | Pinch to play | Q to quit",
        True,
        (200, 200, 200)
    )

    screen.blit(instructions, (WIDTH // 2 - 270, 90))

    # Draw white keys
    for key in PIANO_KEYS:

        if key["black"]:
            continue

        color = (255, 220, 100) if key["note"] == active_key else (230, 230, 230)

        if key["note"] == hovered_key and active_key is None:
            color = (180, 220, 255)

        pygame.draw.rect(
            screen,
            color,
            key["rect"]
        )

        pygame.draw.rect(
            screen,
            (30, 30, 30),
            key["rect"],
            2
        )

        label = small_font.render(
            key["note"],
            True,
            (20, 20, 20)
        )

        screen.blit(
            label,
            (key["rect"].x + 35, key["rect"].bottom - 35)
        )

    # Draw black keys
    for key in PIANO_KEYS:

        if not key["black"]:
            continue

        color = (255, 180, 70) if key["note"] == active_key else (20, 20, 20)

        if key["note"] == hovered_key and active_key is None:
            color = (80, 120, 180)

        pygame.draw.rect(
            screen,
            color,
            key["rect"],
            border_radius=4
        )

        label = small_font.render(
            key["note"],
            True,
            (255, 255, 255)
        )

        screen.blit(
            label,
            (key["rect"].x + 7, key["rect"].y + 110)
        )


# ==========================================
# 9. HAND TRACKING
# ==========================================

def process_hand(frame):

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    finger_position = None
    is_pinching = False

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            h, w, _ = frame.shape

            ix = int(index_tip.x * w)
            iy = int(index_tip.y * h)

            tx = int(thumb_tip.x * w)
            ty = int(thumb_tip.y * h)

            finger_position = (ix, iy)

            # Calculate normalized distance between thumb and index
            distance = math.hypot(
                index_tip.x - thumb_tip.x,
                index_tip.y - thumb_tip.y
            )

            is_pinching = distance < PINCH_THRESHOLD

            cv2.circle(
                frame,
                (ix, iy),
                10,
                (0, 255, 0),
                -1
            )

            cv2.circle(
                frame,
                (tx, ty),
                10,
                (255, 0, 0),
                -1
            )

            status = "PINCH" if is_pinching else "RELEASE"

            cv2.putText(
                frame,
                status,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            break

    return finger_position, is_pinching


# ==========================================
# 10. MAIN APPLICATION LOOP
# ==========================================

active_key = None
active_channel = None

try:

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        ret, frame = cap.read()

        if not ret:
            print("Failed to read webcam frame.")
            break

        frame = cv2.flip(frame, 1)

        finger_position, is_pinching = process_hand(frame)

        hovered_key = None

        if finger_position is not None:

            fx, fy = finger_position

            h, w, _ = frame.shape

            # Map webcam coordinates to piano window coordinates
            screen_x = int(fx * WIDTH / w)
            screen_y = int(fy * HEIGHT / h)

            hovered_key = find_key(
                screen_x,
                screen_y
            )

        # Play a note only when a valid key is pinched
        new_active_key = (
            hovered_key
            if is_pinching and hovered_key is not None
            else None
        )

        # Avoid restarting audio on every frame
        if new_active_key != active_key:

            if active_channel is not None:
                active_channel.stop()

            active_key = new_active_key
            active_channel = None

            if active_key is not None:
                active_channel = SOUNDS[active_key].play(-1)

        draw_piano(hovered_key, active_key)

        pygame.display.flip()

        # Show webcam separately
        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            running = False

        clock.tick(FPS)

finally:

    if active_channel is not None:
        active_channel.stop()

    cap.release()

    hands.close()

    cv2.destroyAllWindows()

    pygame.quit()

    print("Virtual Piano closed.")





# Hand Gesture 
# import cv2
# import mediapipe as mp
# import time

# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils

# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# def main():
#     global prev_time
#     with mp_hands.Hands(
#         max_num_hands=2,
#         min_detection_confidence=0.7,
#         min_tracking_confidence=0.5,
#     ) as hands:
#         while True:
#             ret, frame = cap.read()
#             max_attempts = 5
#             attempt = 0
#             while not ret and attempt < max_attempts:
#                 attempt += 1
#                 time.sleep(0.1)
#                 ret, frame = cap.read()
#             if not ret:
#                 print(f"Failed to read frame after {max_attempts} attempts.")
#                 break
#             frame = cv2.flip(frame, 1)
#             h, w, c = frame.shape
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = hands.process(rgb)

#             if results.multi_hand_landmarks:
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     mp_draw.draw_landmarks(
#                         frame,
#                         hand_landmarks,
#                         mp_hands.HAND_CONNECTIONS,
#                     )

#                     fingertips = {
#                         "thumb": hand_landmarks.landmark[4],
#                         "index": hand_landmarks.landmark[8],
#                         "middle finger": hand_landmarks.landmark[12],
#                         "ring": hand_landmarks.landmark[16],
#                         "pinky": hand_landmarks.landmark[20],
#                     }

#                     for name, landmark in fingertips.items():
#                         x, y = int(landmark.x * w), int(landmark.y * h)
#                         cv2.putText(
#                             frame,
#                             name,
#                             (x, y - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.5,
#                             (0, 255, 0),
#                             1,
#                         )
#                         cv2.circle(
#                             frame,
#                             (x, y),
#                             6,
#                             (0, 255, 0),
#                             -1
#                         )

#             cv2.imshow("Hand + Finger Tracking", frame)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()
