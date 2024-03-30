import mediapipe as mp
import cv2

# Hands model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# cv2 capture
cap = cv2.VideoCapture(0)

def finger_count(points):
    count = 0
    # Cord: (x, y, z)
    # Looking at the screen the 
    # top left is (0, 0)
    # bottom right is (1,1)


    # If 8 is over 6
    print('Index Finger Tip', points['Landmark_8'])
    print('Index Finger Base', points['Landmark_6'])
    print()
    if(points['Landmark_8'][1] < points['Landmark_6'][1]):
        count += 1
        print("Index Finger Up!!")
 
    # If 12 is over 10
    if(points['Landmark_12'][1] < points['Landmark_10'][1]):
        count += 1
        print("Middle Finger Up!!")
        
    # If 16 is over 13
    if(points['Landmark_16'][1] < points['Landmark_13'][1]):
        count += 1
        print("Ring Finger Up!!")

    # If 20 is over 18
    if(points['Landmark_20'][1] < points['Landmark_18'][1]):
        count += 1
        print("Pinky Finger is Up!!")

    # The thumb may be entirely different because the thumb rotates
    # instead of folds
    # If 4 is more left 2, also need (hand orientation)
    if(points['Handedness'] == 'Left'):
        if(points['Landmark_4'][0] > points['Landmark_2'][0]):
            count += 1
            print("Thumb is Up!!")

    if(points['Handedness'] == 'Right'):
        if(points['Landmark_4'][0] < points['Landmark_2'][0]):
            count += 1
            print("Thumb is Up!!")
    
        

    print(count)



# Creates the hands object
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        # Extract Frame, update color format correction
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Hand processing
        results = hands.process(image)
        image.flags.writeable = True

        # Matching the hands drawing to the image
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                hand_info = {}

                hand_info['Handedness'] = results[0].multi_handedness[0].classification[0].label

                for lm_idx, lm in enumerate(hand.landmark):
                    hand_info[f'Landmark_{lm_idx}'] = (round(lm.x,4), round(lm.y, 4), round(lm.z, 4))


                # Debug section
                if cv2.waitKey(10) & 0xFF == ord('d'):
                    finger_count(hand_info)   
                

                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0,0, 0), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(121,44, 250), thickness=2, circle_radius=2))



        cv2.imshow('Hand Tracking v1', image)

        # This is the close statement
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()