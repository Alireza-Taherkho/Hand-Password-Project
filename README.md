# Hand Gesture Controlled Multi-Utility Application

## Overview

This project is a computer vision application built with **Python**, **OpenCV**, and **CVZone** that allows users to interact with different utilities using **hand gestures** and **face tracking** through a webcam.

The application includes:

* Gesture-based password authentication
* Virtual painting tool
* Face detection and blink monitoring
* Hand gesture volume control
* Interactive menu navigation using finger tracking

---

## Features

### 1. Gesture Password System

Instead of typing a password, users create a password using the total number of raised fingers from both hands.

#### Password Creation

* The system records hand gestures.
* A voting mechanism (mode selection) is used to improve accuracy.
* Two gesture numbers are stored as the password.

#### Login

* Users repeat the saved gesture sequence.
* If the sequence matches, access is granted.

#### Additional Controls

* Left hand with all fingers raised → Clear entered password.
* Right hand with four fingers raised → Reset and create a new password.

---

### 2. Virtual Painting

Draw directly in the air using your index finger.

#### Controls

* Index finger up → Draw
* Index finger down → Stop drawing
* All fingers of one hand up → Clear canvas
* Both hands with all fingers up → Return to main menu

---

### 3. Face Detection & Blink Monitoring

The application uses Face Mesh landmarks to:

* Count visible faces
* Detect eye blinks
* Estimate whether the user's face is too close to the camera

#### Features

* Real-time face counting
* Blink status monitoring
* Warning indicator when the face is very close to the camera

---

### 4. Gesture-Based Volume Control

Control the system volume using the distance between:

* Thumb tip
* Index finger tip

#### Functionality

* Smaller distance → Lower volume
* Larger distance → Higher volume
* Real-time volume bar visualization
* Direct system volume adjustment using Pycaw

---

### 5. Interactive Gesture Menu

After successful login, users can navigate through a visual menu using their index finger.

#### Menu Options

* Painting
* Face Control
* Sound Control
* Logout

---

## Technologies Used

* Python
* OpenCV
* NumPy
* CVZone
* Face Mesh Detection
* Hand Tracking
* Pycaw (Windows Audio Control)
* Concurrent Futures

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### Install Dependencies

```bash
pip install opencv-python
pip install numpy
pip install cvzone
pip install matplotlib
pip install pycaw
```

---

## Project Structure

```text
project/
│
├── main.py
├── README.md
│
├── Hand Tracking
├── Face Mesh Detection
├── Password Authentication
├── Painting Module
├── Volume Control Module
└── User Interface
```

---

## How It Works

### Authentication Phase

1. Create a gesture password.
2. Confirm the password.
3. Enter the same gesture sequence to log in.

### Main Menu

After login:

* Blue Box → Painting
* Green Box → Face Control
* Yellow Box → Sound Control
* Red Box → Logout

### Exit Applications

Raise all fingers on both hands for a short period to return to the main menu.

### Quit Program

Press:

```text
ESC
```

---

## Future Improvements

* Save passwords to a file/database
* Multi-user support
* Gesture customization
* Additional drawing tools
* Brightness control
* Media playback controls
* Improved UI design

---

## Notes

* A webcam is required.
* Volume control functionality is designed for Windows systems because it uses Pycaw.
* Good lighting conditions improve hand and face detection accuracy.

---

## Author

Developed as a Computer Vision and Human-Computer Interaction project using OpenCV, CVZone, and Python.
