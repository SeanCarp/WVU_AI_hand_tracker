import cv2
import mediapipe as mp

# Create a MediaPipe Pose instance
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# Open a video capture device (e.g. your webcam)
cap = cv2.VideoCapture('http://192.168.4.1:81/stream')

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    # Convert the frame to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Perform pose detection
    results = pose.process(rgb)
    
    # Draw the body skeletons for each person
    if results.pose_landmarks:
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
        )
    
    # Display the output
    cv2.imshow('Body Skeleton Detection', frame)
    
    # Exit on key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()