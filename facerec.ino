#include <Servo.h>

// gebruikte pins
const int HOR_SERVO_PIN = 8;
const int VER_SERVO_PIN = 7;
const int LED = 6;

Servo horServo;
Servo verServo;

const int HOR_CENTER_ANGLE = 90;
const int VER_CENTER_ANGLE = 90;

// camera instellingen (moeten de instellingen in python script matchen)
const int CAMERA_WIDTH = 640;
const int CAMERA_HEIGHT = 480;

const int VER_MIN_ANGLE = 20;  
const int VER_MAX_ANGLE = 160;  

int targetHor = HOR_CENTER_ANGLE;
int targetVer = VER_CENTER_ANGLE;

String serialData = "";

void setup() {
  horServo.attach(HOR_SERVO_PIN);
  verServo.attach(VER_SERVO_PIN);

  Serial.begin(9600);
  Serial.println("Turret Ready.");

  horServo.write(HOR_CENTER_ANGLE);
  verServo.write(VER_CENTER_ANGLE);

  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    serialData += inChar;

    if (inChar == '\n') {
      serialData.trim();

      int commaIndex = serialData.indexOf(',');
      if (commaIndex > 0) {
        int faceX = serialData.substring(0, commaIndex).toInt();
        int faceY = serialData.substring(commaIndex + 1).toInt();

        targetHor = map(faceX, 0, CAMERA_WIDTH, 0, 180);
        targetHor = constrain(targetHor, 0, 180);
        horServo.write(targetHor);
        digitalWrite(LED, HIGH);

        targetVer = map(faceY, 0, CAMERA_HEIGHT, VER_MIN_ANGLE, VER_MAX_ANGLE);
        targetVer = constrain(targetVer, VER_MIN_ANGLE, VER_MAX_ANGLE);
        verServo.write(targetVer);

      } else {
        // lampje uit als er geen gezicht te zien is op de camera
        digitalWrite(LED, LOW);
      }

      serialData = "";  
    }
  }
}