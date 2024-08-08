import mediapipe as mp
import cv2

# Hands model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# Does not correctly display thumb if flipped backwards
def finger_count(points):
    count = 0
    # Cord: (x, y)
    # Looking at the screen where
    # Top Left is (0, 0) & Bttm Right is (1,1)

    # If 8 is over 6
    if(points['Landmark_8'][1] < points['Landmark_6'][1]):
        count += 1
    if(points['Landmark_12'][1] < points['Landmark_10'][1]):
        count += 1
    if(points['Landmark_16'][1] < points['Landmark_13'][1]):
        count += 1
    if(points['Landmark_20'][1] < points['Landmark_18'][1]):
        count += 1
    
    if(points['Handedness'] == 'Left'):
        if(points['Landmark_4'][0] > points['Landmark_2'][0]):
            count += 1

    if(points['Handedness'] == 'Right'):
        if(points['Landmark_4'][0] < points['Landmark_2'][0]):
            count += 1

    return count





cap = cv2.VideoCapture(0) # 0 for default camera

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        # Extract Frame, update color format correction
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Hand Processing
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        up_fingers = 0


        if results.multi_hand_landmarks: # Only runs if there is a hand in frame

            # Num is the index, Hand is landmarks as a dict
            for num, hand in enumerate(results.multi_hand_landmarks):
                hand_info = {}

                # Multi-handedness sees both
                hand_info['Handedness'] = results[num].multi_handedness[num].classification[0].label

                for lm_idx, lm in enumerate(hand.landmark):
                    hand_info[f'Landmark_{lm_idx}'] = (round(lm.x,4), round(lm.y,4), round(lm.z,4))



                up_fingers += finger_count(hand_info)

                if cv2.waitKey(10) & 0xFF == ord('d'):
                    print(hand)

                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                          mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))


        image = cv2.putText(image, str(up_fingers),(50,50),cv2.FONT_HERSHEY_COMPLEX,
                            1, (0,255,0), 2, cv2.LINE_AA)

        #Display Image
        cv2.imshow('Hand Tracking v1', image)        

        # This is the close statement
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
