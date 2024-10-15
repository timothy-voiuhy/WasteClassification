import cv2
from gpiozero import Servo, LED
from time import sleep
import argparse
from ultralytics import YOLO
import logging
import sys

MODEL_PATH = '/Models/wasteClassificationModel_best.pt' # This path is relative to the rasberrypi4

def initializePins():
    logging.info("Initializing pins")
    try:
        servo = Servo(17)  # GPIO pin 17 for the servo
        logging.info("Servo pin successfully initialized")
    except Exception as e:
        logging.error(f"Encountered technical error after the servo pin could not be initiaized recieving exception {e}")
    try:
        electromagnet = LED(27)  # GPIO pin 27 for the electromagnet (using LED as switch)
        logging.info("Electromagnet pin successfully initialized")
    except Exception as e:
        logging.error(f"Encountered technical error after the electromagnet pin could not be initiaized recieving exception {e}")
    return servo, electromagnet

def startLiveFeedDetection(model:YOLO = None, monitor =False):
    servo, electromagnet = initializePins()
    if model is None:
        __model = MODEL_PATH
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Failed to open camera")
        sys.exit(1)
    window_name = "live capture with detection mode"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # cv2.resizeWindow(window_name, 800, 800)
    # start the live capture in a while loop
    try:
        while True:
            # capture frame by frame from the camera
            ret, frame = cap.read() 
            if not ret:
                logging.warning("Failed to grab frame")
                break

            # perform inference on the frame 
            results = __model.predict(frame)

            for result in results:
                boxes = result.boxes.xyxy # get the boxes coordinates 
                confidences = result.boxes.conf  # get the confidence levels 
                class_ids = result.boxes.cls # get the class ids 
                class_names = result.names 

                for box, confidence, class_id  in zip(boxes, confidences, class_ids):
                    if monitor:
                        # capture the corners 
                        x1, y1, x2, y2 = map(int, box)
                        # rectangle for the bounding box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        # label 
                        label = f"Class: {class_names[int(class_id)]}, Confidence: {confidence:.2f}"
                        #place the label onto the image at a spcific point 
                        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        cv2.imshow(window_name, frame)

                        # After showing results on the screen, send the class_id to the control mechanism
                        control_mechanism(class_id, servo, electromagnet)

                        # break the loop if q is pressed
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    else:
                        control_mechanism(class_id)
    except Exception as e:
        logging.warning(f"Experienced exception {e}")
        cap.release() 
        cv2.destroyAllWindows()


def control_mechanism(class_id, servo:Servo, electromagnet:LED):
    """
    Controls the servo motor and electromagnet based on the classification result.
    class_id: The waste class (1, 2, or 3).
    """
    enabled_classes = [1,2,3]
    if class_id in enabled_classes:
        if class_id == 1:
            move_servo(0.1, servo)  # Position 1 for first bin
        elif class_id == 2:
            move_servo(0.5, servo)  # Position 2 for second bin
        elif class_id == 3:
            move_servo(1.0, servo)  # Position 3 for third bin
    
    # Activate the electromagnet after moving
    activate_electromagnet(electromagnet)

def move_servo(position, servo:Servo):
    """
    Move the servo to a specified position.
    position: Value between -1 (fully counterclockwise) and 1 (fully clockwise).
    """
    print(f"Moving servo to position: {position}")
    servo.value = position
    sleep(1)  # Allow time for the waste to be positioned

def activate_electromagnet(electromagnet:LED):
    """
    Activate the electromagnet to push the waste into the bin.
    """
    print("Activating electromagnet")
    electromagnet.on()  # Turn on the electromagnet
    sleep(0.5)  # Hold for half a second
    electromagnet.off()  # Turn off the electromagnet
    print("Electromagnet deactivated")

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--monitor", action="store_true", help="Whether is a monitor is present for showing the live feed")
    parser.add_argument("--start", action="store_true", help="Start running system")
    parser.add_argument("--model", type = str, default="/Models/wasteClassificationModel_best.pt", help="The path to the yolo fine tuned model")
    return parser

if __name__ == '__main__':
    parser = parseArgs()
    args = parser.parse_args()
    if args.start:
        startLiveFeedDetection(args.model, args.monitor)
    else:
        parser.print_help()