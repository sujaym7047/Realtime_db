import cv2
import numpy as np
import time
import json
import pymysql
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load model
model = load_model('emotion.hdf5', compile=False)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Connect MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='new980'
)
cursor = conn.cursor()

# Start webcam
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (64, 64))
        face = face.astype("float") / 255.0
        face = np.expand_dims(face, axis=-1)
        face = np.expand_dims(face, axis=0)

        preds = model.predict(face, verbose=0)[0]
        emotion_probability = np.max(preds)
        emotion_label = emotion_labels[preds.argmax()]

        print(f"Detected: {emotion_label} ({emotion_probability * 100:.2f}%)")

        # Draw rectangle box around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display emotion above rectangle
        text = f"{emotion_label} ({emotion_probability * 100:.1f}%)"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 255, 0), 2)

        # Store into MySQL
        try:
            cursor.execute("INSERT INTO emotionlog (time, emotion) VALUES (%s, %s)",
                           (time.strftime("%H:%M:%S"), emotion_label))
            conn.commit()
        except Exception as e:
            print("Failed to insert into MySQL:", e)

    cv2.imshow("Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()
