# Discipline-Management-System
A Python and MySQL-based Discipline Management System to record, track, and analyze student behavior and discipline records efficiently.
🏫 School Discipline Management System
📘 Overview

This is a Python + MySQL project designed to help schools manage and record discipline-related data digitally.
I created this project as a Class 12 student after serving as the Discipline Minister in my school, where I faced difficulties managing records manually.
To solve this, I built a program that automates the process and stores data securely.

🚀 Features

Add, edit, and delete student discipline records

Track daily or weekly behavior reports

Record student class, section, and date of incident automatically

Generate reports for review or printing

🛠️ Technologies Used

Python 3.x

MySQL (Database)

Libraries: mysql.connector, datetime

🧩 Database Structure

Table: discipline_records

Column	Type	Description
id	INT	Auto Increment Primary Key
name	VARCHAR(100)	Student Name
class_section	VARCHAR(10)	Class and Section
date	DATE	Date of Record
issue	VARCHAR(200)	Reason for Record
remarks	VARCHAR(200)	Additional Notes
