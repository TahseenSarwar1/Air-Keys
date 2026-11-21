# 🎹 AirKeys — Virtual Piano Using Hand Gestures

**Play the piano without touching a keyboard.**

AirKeys is a learning project that explores computer vision, hand tracking, gesture recognition and audio processing using Python.

It uses a webcam to track hand movements and allows users to interact with an on-screen virtual piano using simple hand gestures.

> **Project Status:** Early-stage learning project / Working prototype.

## ✨ What does it do?

The current version provides:

- **Real-time hand tracking:** Uses MediaPipe to detect hands and track 21 hand landmarks.
- **Finger tracking:** Tracks the index fingertip and thumb.
- **Gesture recognition:** Detects a pinch gesture when the thumb and index finger come close together.
- **Virtual piano:** Displays a one-octave piano (C4–B4) with white and black keys.
- **Gesture-based interaction:** Move your index finger over a piano key and pinch to play its corresponding note.
- **Sound generation:** Generates basic musical tones using NumPy and plays them through Pygame.

## 🛠️ Tech Stack

| Technology | Purpose                                    |
| ---------- | ------------------------------------------ |
| Python     | Core application logic                     |
| OpenCV     | Webcam access and image processing         |
| MediaPipe  | Hand detection and landmark tracking       |
| Pygame     | Virtual piano interface and audio playback |
| NumPy      | Digital sound-wave generation              |

## ⚙️ How It Works

The application follows a real-time processing pipeline:

1. **Webcam:** Captures video frames.
2. **OpenCV:** Reads and processes the frames.
3. **MediaPipe:** Detects the hand and identifies its 21 landmarks.
4. **Gesture Recognition:** Calculates the distance between the thumb and index fingertips to detect a pinch.
5. **Coordinate Mapping:** Maps the index fingertip's position to the virtual piano.
6. **Piano Interaction:** Identifies the key under the fingertip.
7. **Audio Engine:** Plays the corresponding musical note when a pinch is detected.

## 📁 Project Structure

```text
airkeys/
│
├── .venv/              # Virtual environment (not committed)
├── main.py             # Main application
├── requirements.txt    # Project dependencies
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/airkeys.git
cd airkeys
```

### 2. Create a virtual environment

```bash
python3.12 -m venv .venv
```

### 3. Activate the environment

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python main.py
```

## 🖐️ Controls

| Action                       | Function               |
| ---------------------------- | ---------------------- |
| Move index finger            | Move the piano pointer |
| Pinch thumb and index finger | Play the selected note |
| Release pinch                | Stop the active note   |
| Press `Q`                    | Quit the application   |

**Note:** Camera access permission must be enabled for the terminal or IDE running the application.

## 📌 Current Limitations

AirKeys is still an experimental prototype.

- Supports one active note at a time.
- Uses basic sine-wave tones rather than realistic piano samples.
- Requires manual adjustment of gesture sensitivity depending on camera positioning.
- Fingertip-to-piano coordinate mapping is currently basic.
- No multi-finger chord recognition yet.

## 🗺️ Future Improvements

Planned improvements include:

- [ ] Better hand-position calibration.
- [ ] Multi-finger tracking and simultaneous notes.
- [ ] Chord and scale recognition.
- [ ] Realistic piano sound samples.
- [ ] Improved gesture detection and reduced latency.
- [ ] Adjustable sensitivity and configurable gestures.
- [ ] Support for additional octaves.
- [ ] Custom strumming patterns and musical interactions.

## 🎯 Learning Objectives

This project is being developed as a hands-on way to learn:

- Python application development.
- Computer vision and image processing.
- Hand landmark detection using MediaPipe.
- Gesture recognition and coordinate geometry.
- Real-time event processing.
- Digital audio generation and playback.
- Integration of multiple Python libraries.
