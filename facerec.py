import cv2
import serial
import time
import sys

ARDUINO_PORT = '/dev/cu.usbmodem101'  
BAUD_RATE = 9600

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
# eerst indice 1 gebruiken omdat iphone indice 0 soms overneemt
CAMERA_INDICES = [1, 0, 2, 3]

FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(3) 
    print(f"Connected to Arduino on port {ARDUINO_PORT}")
except serial.SerialException as e:
    print(f"Error connecting to Arduino on {ARDUINO_PORT}.")
    print(e)
    sys.exit()

cap = None
chosen_index = -1
for i in CAMERA_INDICES:
    temp_cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
    if temp_cap.isOpened():
        temp_cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        temp_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        cap = temp_cap
        chosen_index = i
        break

if cap is None:
    print("Failed to open any webcam using tested indices. (iphone misschien aan het kloten met camera van mac?)")
    arduino.close()
    sys.exit()

print(f"Webcam successfully opened using index {chosen_index}. Resolution: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
print("Starting face tracking loop. Press 'q' to exit.")

def send_serial_coordinates(x, y):
    command = f"{x},{y}\n"
    try:
        arduino.write(command.encode('utf-8'))
    except serial.SerialException:
        print("Serial connection lost.")
        return False
    return True

smoothed_x = CAMERA_WIDTH // 2
smoothed_y = CAMERA_HEIGHT // 2
SMOOTHING_FACTOR = 0.2 

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=FACE_SCALE_FACTOR,
            minNeighbors=FACE_MIN_NEIGHBORS,
            minSize=(30, 30)
        )

        if len(faces) > 0:
            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            target_x = x + w // 2
            target_y = y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (target_x, target_y), 5, (0, 0, 255), -1)
            cv2.putText(frame, 'TRACKING', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            target_x = CAMERA_WIDTH // 2
            target_y = CAMERA_HEIGHT // 2
            cv2.putText(frame, 'SEARCHING', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        smoothed_x = int(smoothed_x + (target_x - smoothed_x) * SMOOTHING_FACTOR)
        smoothed_y = int(smoothed_y + (target_y - smoothed_y) * SMOOTHING_FACTOR)

        send_serial_coordinates(smoothed_x, smoothed_y)

        cv2.line(frame, (CAMERA_WIDTH // 2, 0), (CAMERA_WIDTH // 2, CAMERA_HEIGHT), (255, 255, 255), 1)

        cv2.imshow('Turret Camera Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Exiting due to Keyboard Interrupt.")

finally:
    print("Closing connection and exiting.")
    send_serial_coordinates(CAMERA_WIDTH // 2, CAMERA_HEIGHT // 2) 
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    arduino.close()
