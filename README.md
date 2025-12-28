<img width="1024" height="1536" alt="Face attendance system overview" src="https://github.com/user-attachments/assets/09bcda6c-2abb-4c40-869b-c508938f978f" />


Face Recognition Attendance System – Overview

This project is a Face Recognition–based Attendance System developed using Python, OpenCV, and PostgreSQL.
It automatically records attendance by identifying a person’s face through a camera and applying time-based rules.

The system is designed to reduce manual work, prevent proxy attendance, and ensure accurate attendance tracking.

How the System Works

The host (admin) registers people by storing their face data.

A live camera continuously captures faces.

The system matches detected faces with registered faces.

Attendance is marked automatically based on the current time:

Before start time → Present

Within allowed time window → Present (Late)

After closing time → Absent

People who do not appear at all are automatically marked Absent.

Key Features

Automatic face recognition–based attendance

Time-based attendance rules (Present / Late / Absent)

Automatic absent marking for non-attendees

PostgreSQL database for secure data storage

No manual input required from users

Use Cases

Schools and colleges

Offices and organizations

Training institutes

Project Summary

This system provides a contactless, accurate, and automated attendance solution using computer vision and database technology.
