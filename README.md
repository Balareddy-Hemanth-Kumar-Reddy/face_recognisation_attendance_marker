<img width="1024" height="1536" alt="Face attendance system overview" src="https://github.com/user-attachments/assets/09bcda6c-2abb-4c40-869b-c508938f978f" />


# Face Recognition Attendance System

## 📌 Overview
This project is a **Face Recognition–based Attendance System** developed using **Python, OpenCV, and PostgreSQL**.  
It automatically records attendance by identifying a person’s face through a camera and applying **time-based rules**.

The system reduces manual effort, prevents proxy attendance, and ensures accurate attendance tracking.

---

## ⚙️ How It Works
1. The host (admin) registers people by storing their face data.
2. A live camera continuously captures faces.
3. The system matches detected faces with registered faces.
4. Attendance is marked automatically based on time:
   - **Before start time** → Present  
   - **Within allowed time window** → Present (Late)  
   - **After closing time** → Absent  
5. People who do not appear at all are **automatically marked Absent**.

---

## ✨ Key Features
- Face recognition–based automatic attendance
- Time-based attendance rules (Present / Late / Absent)
- Automatic marking of absentees
- Secure PostgreSQL database storage
- Contactless and user-friendly system

---

## 🏫 Use Cases
- Schools and colleges  
- Offices and organizations  
- Training institutes  

---

## 📄 Project Summary
This system provides a **contactless, reliable, and automated attendance solution** using computer vision and database technologies.

