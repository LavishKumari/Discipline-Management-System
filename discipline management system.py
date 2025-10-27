import mysql.connector
from datetime import datetime

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # change to your MySQL username
    password="lavi", # change to your MySQL password
    database="school_defaulters"
)
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    class_section VARCHAR(20),
    late INT DEFAULT 0,
    uniform INT DEFAULT 0,
    indiscipline INT DEFAULT 0,
    absent INT DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS defaults_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no INT,
    category VARCHAR(50),
    date_recorded DATE,
    FOREIGN KEY (roll_no) REFERENCES students(roll_no)
)
""")

# Student Class
class Student:
    def __init__(self, roll_no, name="", class_section=""):
        self.roll_no = roll_no
        self.name = name
        self.class_section = class_section

    def add_to_db(self):
        query = "INSERT INTO students (roll_no, name, class_section) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (self.roll_no, self.name, self.class_section))
            conn.commit()
            print(f"✅ Student {self.name} added successfully.")
        except:
            print("⚠️ Student already exists!")

    def add_default(self, category):
        query = f"UPDATE students SET {category} = {category} + 1 WHERE roll_no = %s"
        cursor.execute(query, (self.roll_no,))
        conn.commit()

        # also insert into log table with date
        log_query = "INSERT INTO defaults_log (roll_no, category, date_recorded) VALUES (%s, %s, %s)"
        cursor.execute(log_query, (self.roll_no, category, datetime.now().date()))
        conn.commit()

        print(f"⚠️ Default '{category}' added for Roll No {self.roll_no}.")


# School Class
class School:
    @staticmethod
    def show_all():
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()
        print("\n--- Student Records ---")
        for r in records:
            print(f"Roll: {r[0]}, Name: {r[1]}, Class: {r[2]}, Late: {r[3]}, Uniform: {r[4]}, Indiscipline: {r[5]}, Absent: {r[6]}")

    @staticmethod
    def most_undisciplined():
        query = """
        SELECT roll_no, name, class_section, (late + uniform + indiscipline + absent) as total
        FROM students ORDER BY total DESC LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            print(f"\n🏆 Most Undisciplined Student: {result[1]} (Roll {result[0]}, Class {result[2]}) with {result[3]} defaults.")
        else:
            print("No records yet.")

    @staticmethod
    def monthly_report(month, year):
        query = """
        SELECT s.roll_no, s.name, s.class_section, COUNT(l.id) as total
        FROM defaults_log l
        JOIN students s ON s.roll_no = l.roll_no
        WHERE MONTH(l.date_recorded) = %s AND YEAR(l.date_recorded) = %s
        GROUP BY s.roll_no, s.name, s.class_section
        ORDER BY total DESC
        LIMIT 3
        """
        cursor.execute(query, (month, year))
        results = cursor.fetchall()
        print(f"\n📊 Top 3 Defaulters for {month}/{year}")
        if results:
            for r in results:
                print(f"Roll: {r[0]}, Name: {r[1]}, Class: {r[2]}, Defaults: {r[3]}")
        else:
            print("No records for this month.")
    @staticmethod
    def student_history(roll_no):
        query = "SELECT name, class_section FROM students WHERE roll_no = %s"
        cursor.execute(query, (roll_no,))
        student = cursor.fetchone()

        if not student:
            print("❌ Student not found.")
            return

        print(f"\n📖 History for {student[0]} (Roll {roll_no}, Class {student[1]})")

        query = """
        SELECT category, date_recorded
        FROM defaults_log
        WHERE roll_no = %s
        ORDER BY date_recorded ASC
        """
        cursor.execute(query, (roll_no,))
        records = cursor.fetchall()

        if records:
            total = 0
            for r in records:
                print(f"⚠️ {r[0].capitalize()} default on {r[1]}")
                total += 1
            print(f"\n🔢 Total Defaults: {total}")
        else:
            print("✅ No defaults recorded for this student.")
    @staticmethod
    def top_defaulters(limit=5):
        query = """
        SELECT s.roll_no, s.name, s.class_section, COUNT(d.id) as total_defaults
        FROM students s
        LEFT JOIN defaults_log d ON s.roll_no = d.roll_no
        GROUP BY s.roll_no, s.name, s.class_section
        ORDER BY total_defaults DESC
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        results = cursor.fetchall()

        print(f"\n🏆 Top {limit} Most Undisciplined Students 🏆")
        if results:
            rank = 1
            for r in results:
                print(f"{rank}. {r[1]} (Roll {r[0]}, Class {r[2]}) → {r[3]} defaults")
                rank += 1
        else:
            print("✅ No defaulters recorded yet.")




# ---------------- Menu-driven Program ----------------
def main():
    while True:
        print("\n===== School Defaulter Tracking System =====")
        print("1. Add Student")
        print("2. Add Default")
        print("3. Show All Records")
        print("4. Show Most Undisciplined Student")
        print("5. Monthly Report")
        print("6. Show Student History")
        print("7. Show Top Defaulters")
        print("8. Exit")



        choice = input("Enter your choice: ")

        if choice == "1":
            roll = int(input("Enter Roll No: "))
            name = input("Enter Student Name: ")
            cls = input("Enter Class & Section: ")
            s = Student(roll, name, cls)
            s.add_to_db()

        elif choice == "2":
            roll = int(input("Enter Roll No: "))
            category = input("Enter Default (late/uniform/indiscipline/absent): ").lower()
            s = Student(roll)
            s.add_default(category)

        elif choice == "3":
            School.show_all()

        elif choice == "4":
            School.most_undisciplined()

        elif choice == "5":
            month = int(input("Enter Month (1-12): "))
            year = int(input("Enter Year (YYYY): "))
            School.monthly_report(month, year)

        elif choice == "6":
            roll = int(input("Enter Roll No: "))
            School.student_history(roll)
       
        elif choice == "7":
            School.top_defaulters()

        elif choice == "8":
            print("👋 Exiting program...")
            break




        else:
            print("❌ Invalid choice! Try again.")

# Run program
main()
