import cv2
import serial
from ultralytics import YOLO

# Initialize the YOLO11s model 
# The custom-trained YOLO11s model trained on different kinds of waste
model = YOLO('wasteClassificationModel_best.pt')

# Note that the yolo model was trained model was trained to classify and segment 80 classes 
# But in this project it retrained putting an extra linear layer to reduce the classes to just 3 (which are the three classes of waste)

# Initialize the serial connection to Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Initialize the camera feed
cap = cv2.VideoCapture(0)  # 0 is for default camera, adjust if needed

def classify_waste():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Pass the frame through YOLOv8 model
        results = model(frame)

        # Assuming YOLO returns classes in the result
        if results:
            class_id = results[0].boxes.cls[0].item()  # Get the first detected class
            send_to_arduino(int(class_id))

        # Display the frame for monitoring (optional)
        cv2.imshow('Waste Classification', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def send_to_arduino(class_id):
    """
    Sends the classification result to Arduino over serial.
    class_id: The detected class (1, 2, or 3).
    """
    try:
        # Send the class_id as a number followed by newline
        arduino.write(f"{class_id}\n".encode())
        print(f"Sent to Arduino: {class_id}")
    except Exception as e:
        print(f"Error sending to Arduino: {e}")

if __name__ == '__main__':
    classify_waste()
