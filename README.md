# facetrack

A Simplearduino project that uses the camera (python script) to turn coordinates into degrees for servos attached to an arduino.

## Hardware Requirements

- Arduino board
- 2 servo motors (horizontal and vertical)
- LED
- Webcam
- USB cable for Arduino connection

## Pin Configuration

- horservo: Pin 8
- verservo: Pin 7
- LED: Pin 6

## Software Requirements

- Python 3.x
- OpenCV (cv2)
- pyserial
- Arduino IDE

## Installation

1. Install the required Python packages:
```bash
pip install opencv-python pyserial
```

2. Upload the Arduino sketch (`facerec.ino`) to your Arduino board using the Arduino IDE.

3. Connect the hardware according to the pin configuration.

4. Update the `ARDUINO_PORT` in `facerec.py` to match your Arduino's port.


## Usage

1. Connect the Arduino to your computer.

2. Run the Python script:
```bash
python facerec.py
```

3. The system will:
   - Initialize the camera and Arduino connection
   - Display the camera feed
   - Control the servos to track detected faces

4. Press 'q' to quit the program. (or ctrl + C via terminal)

## Camera Settings

- Resolution: 640x480
- Face detection parameters are adjustable in the Python script
- Multiple camera indices are supported for automatic selection
