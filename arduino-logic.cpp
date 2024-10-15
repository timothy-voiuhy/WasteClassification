#include <Servo.h>

Servo wasteServo;  // Create a servo object
int electromagnetPin = 7;  // Pin for controlling the electromagnet
int classification = -1;   // Classification result

void setup() {
  Serial.begin(9600);       // Initialize serial communication
  wasteServo.attach(9);     // Attach servo to pin 9
  pinMode(electromagnetPin, OUTPUT);  // Set the electromagnet pin as output
  digitalWrite(electromagnetPin, LOW); // Ensure electromagnet is off initially
}

void loop() {
  // Check if classification data is available from the AI system
  if (Serial.available() > 0) {
    classification = Serial.parseInt();  // Read the classification (integer)

    // Handle waste sorting based on classification number
    if (classification >= 0) {
      moveWasteToBin(classification);  // Move to the appropriate bin
    }
  }
}

void moveWasteToBin(int classification) {
  int servoPosition = 0;

  // Determine servo position based on classification
  switch (classification) {
    case 1:
      servoPosition = 30;  // Position for first bin
      break;
    case 2:
      servoPosition = 90;  // Position for second bin
      break;
    case 3:
      servoPosition = 150; // Position for third bin
      break;
    default:
      servoPosition = 0;   // Default position
      break;
  }

  // Move the servo motor to the required position
  wasteServo.write(servoPosition);
  delay(1000);  // Allow time for the waste to move

  // Activate the electromagnet to push waste into the bin
  digitalWrite(electromagnetPin, HIGH);  // Turn on electromagnet
  delay(500);  // Hold for 500ms to push the waste
  digitalWrite(electromagnetPin, LOW);   // Turn off electromagnet
}
