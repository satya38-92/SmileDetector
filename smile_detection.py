import cv2
import random
import time

# Load the pre-trained face and smile cascade classifiers from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

# Start video capture from the default camera
video = cv2.VideoCapture(0)

# Function to display the smile meter
def smile_meter(frame, x1, y1):
    score = random.randint(0, 100)  # Generate a random score for the smile meter
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 255)
    cv2.putText(frame, "Your Smile Score is:", (x1 - 15, y1 - 70), font, 1, color, 4, cv2.LINE_AA)
    cv2.putText(frame, str(score), (x1 + 50, y1 - 20), font, 1, color, 4, cv2.LINE_AA)
    time.sleep(1)  # Pause for a short duration to simulate processing time

while True:
    # Capture frame-by-frame
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw a rectangle around the face
        
        # Region of interest in the grayscale frame for smile detection
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect smiles in the region of interest
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=28)

        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (255, 0, 0), 2)  # Draw a rectangle around the smile
            
            # Display the smile meter
            smile_meter(frame, x, y)

    # Display the resulting frame
    cv2.imshow("Smile Meter", frame)

    # Exit the loop when 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
video.release()
cv2.destroyAllWindows()
