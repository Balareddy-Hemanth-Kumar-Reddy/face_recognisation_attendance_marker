import os
import cv2
import numpy as np
import psycopg2
from datetime import datetime, date, time as dt_time
from const import CONST_DATABASE_URL



start_hour=9
start_min=30
end_hour=16
end_min=12

DATABASE_URL = CONST_DATABASE_URL
if DATABASE_URL is None:
    print("DATABASE_URL not set!")
    exit()

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("Connected to PostgreSQL database!")
except Exception as e:
    print("Error connecting to database:", e)
    exit()

# Load registered faces
faces_dir = "faces"
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
labels = []
train_images = []

for file in os.listdir(faces_dir):
    if file.endswith(".jpg"):
        name = file.replace(".jpg", "")
        img = cv2.imread(os.path.join(faces_dir, file), cv2.IMREAD_GRAYSCALE)
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml").detectMultiScale(img)
        if len(faces) == 0:
            continue
        x, y, w, h = faces[0]
        face_region = img[y:y+h, x:x+w]
        train_images.append(face_region)
        labels.append(name)

# Convert labels to integers
label_map = {i: name for i, name in enumerate(labels)}
train_labels = np.array([i for i in range(len(labels))])

face_recognizer.train(train_images, train_labels)

# Start webcam
cam = cv2.VideoCapture(0)
recognized_today = set()
attendance_closed = False

print("Starting live attendance...")

while True:
    status=""
    ret, frame = cam.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml").detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
        face_region = gray_frame[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face_region)
        name = label_map.get(label, "Unknown")

        # Mark attendance
        now = datetime.now()
        today_date = date.today()
        current_time = now.time()

        if name != "Unknown" and name not in recognized_today:
            if current_time < dt_time(start_hour,start_min):
                status = "Present"
            elif dt_time(start_hour,start_min) <= current_time <= dt_time(end_hour,end_min):
                status = "Present Late"
            else:
                status = "Absent"
                attendance_closed = True

            cursor.execute("""
                INSERT INTO attendance (name, date, time, status)
                VALUES (%s, %s, %s, %s)
            """, (name, today_date, current_time, status))
            conn.commit()
            recognized_today.add(name)
            print(f"{name} marked as {status} at {current_time}")
        

    cv2.imshow("Live Attendance", frame)

    # Close after 11 AM automatically
    if datetime.now().time() > dt_time(end_hour,end_min):
        print("Attendance closed after 11 AM")
        attendance_closed = True

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

    if name=="unknown":
        print("Unknown face detected.")

# Mark absent for remaining people
cursor.execute("SELECT name FROM people")
all_people = {row[0] for row in cursor.fetchall()}
for person in all_people - recognized_today:
    cursor.execute("""
        INSERT INTO attendance (name, date, time, status)
        VALUES (%s, %s, %s, %s)
    """, (person, today_date, None, "Absent"))
conn.commit()

cam.release()
cv2.destroyAllWindows()
conn.close()
print("Attendance process finished.")
