import os
import cv2
import numpy as np
import psycopg2
from const import CONST_DATABASE_URL


# Get database URL from environment variable
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

# ---------------- Face registration logic ----------------
name = input("Enter teacher name: ")

# Add teacher to database
cursor.execute("INSERT INTO people (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (name,))
conn.commit()
conn.close()

# Create faces folder
if not os.path.exists("faces"):
    os.mkdir("faces")

# Capture face
cam = cv2.VideoCapture(0)
print("Press 'S' to capture face")

while True:
    ret, frame = cam.read()
    cv2.imshow("Register Face", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f"faces/{name}.jpg", frame)
        print(f"{name}'s face saved!")
        break

cam.release()
cv2.destroyAllWindows()

# Convert to grayscale and save embedding
img = cv2.imread(f"faces/{name}.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

if len(faces) > 0:
    x, y, w, h = faces[0]
    face_region = gray[y:y+h, x:x+w]
    np.save(f"faces/{name}_embedding.npy", face_region)
    print(f"{name}'s face embedding saved!")
else:
    print("No face detected, try again.")
