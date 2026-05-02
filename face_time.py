import numpy as np
import cv2
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import winsound  # For beep sound on Windows

# Define the emotions and assign a confidence factor for each.
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Load the pre-trained emotion detection model and its weights.
classifier = load_model('model_78.h5')
classifier.load_weights('model_weights_78.h5')

# Load the face detector using OpenCV's Haar Cascade.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def emotion():

    # Initialize variables to store the final emotion and confidence score.
    final_emotion = None
    final_confidence_score = 0
    face_absent_counter = 0  # Counter to track frames without a detected face

    # Start the webcam feed.
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame from webcam.
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale, as the face detector expects grayscale images.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame.
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Check if any faces are detected.
        if len(faces) == 0:
            face_absent_counter += 1
            print(face_absent_counter,"///////////////")
            # If the face is absent for more than 3 frames, play a beep sound.
            if face_absent_counter > 30:  # Change this to 3 frames
                winsound.Beep(1000, 500)  # Beep with 1000 Hz frequency and 500 ms duration
                face_absent_counter = 0  # Reset the counter after beeping
        else:
            face_absent_counter = 0  # Reset the counter when a face is detected

        # Loop over each detected face.
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

            # Extract the Region of Interest (ROI) for the face.
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            # Preprocess the face ROI for emotion prediction.
            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # Make the emotion prediction.
                prediction = classifier.predict(roi)[0]
                maxindex = int(np.argmax(prediction))
                emotion = emotion_labels[maxindex]

                # Calculate confidence score (probability) for the detected emotion.
                confidence_score = prediction[maxindex] * 100  # Convert to percentage.

                # Store the final emotion and confidence score.
                final_emotion = emotion
                final_confidence_score = confidence_score

                # Display the emotion label and confidence score above the detected face.
                label_position = (x, y - 10)
                cv2.putText(frame, f'{emotion}: {confidence_score:.2f}%', label_position, 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Estimate confidence level based on emotion.
                if emotion in ['Happy', 'Neutral']:
                    confidence_level = "High Confidence"
                elif emotion in ['Surprise', 'Angry']:
                    confidence_level = "Moderate Confidence"
                else:
                    confidence_level = "Low Confidence"

                # Display the confidence level below the face rectangle.
                confidence_position = (x, y + h + 20)
                cv2.putText(frame, confidence_level, confidence_position, 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Display the frame with the detected face, emotion, confidence score, and confidence level.
        cv2.imshow('Emotion & Confidence Detector', frame)

        # Exit the loop when the user presses the 'q' key.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the OpenCV windows.
    cap.release()
    cv2.destroyAllWindows()

    # Display the final calculated emotion and confidence score before exiting.
    if final_emotion is not None:
        print(f"Final Emotion: {final_emotion}")
        print(f"Final Confidence Score: {final_confidence_score:.2f}%")
    else:
        print("No emotion detected.")



emotion()