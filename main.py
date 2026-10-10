#!/usr/bin/env python3
"""Student result manager backed by SQLite."""
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("students.db")
SUBJECTS = ("English", "Mathematics", "Computer")

def connect():
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            english REAL NOT NULL,
            mathematics REAL NOT NULL,
            computer REAL NOT NULL
        )
    """)
    return db

def grade(percentage):
    if percentage >= 90: return "A+"
    if percentage >= 80: return "A"
    if percentage >= 70: return "B"
    if percentage >= 60: return "C"
    if percentage >= 50: return "D"
    return "Needs improvement"

def add_student(db):
    name = input("Student name: ").strip()
    roll = input("Roll number: ").strip()
    if not name or not roll:
        print("Name and roll number are required.")
        return
    marks = []
    for subject in SUBJECTS:
        try:
            mark = float(input(f"{subject} marks (0-100): ").strip())
            if not 0 <= mark <= 100:
                raise ValueError
            marks.append(mark)
        except ValueError:
            print("Marks must be a number between 0 and 100. Record not saved.")
            return
    try:
        db.execute(
            "INSERT INTO students(name, roll_no, english, mathematics, computer) VALUES (?, ?, ?, ?, ?)",
            (name, roll, *marks),
        )
        db.commit()
        print("Student result saved.")
    except sqlite3.IntegrityError:
        print("That roll number already exists.")

def print_student(row):
    marks = [row["english"], row["mathematics"], row["computer"]]
    total = sum(marks)
    percentage = total / len(SUBJECTS)
    print(f"\nName: {row['name']} | Roll: {row['roll_no']}")
    print(f"English: {marks[0]:.1f} | Mathematics: {marks[1]:.1f} | Computer: {marks[2]:.1f}")
    print(f"Total: {total:.1f}/300 | Percentage: {percentage:.2f}% | Grade: {grade(percentage)}")

def list_students(db):
    rows = db.execute("SELECT * FROM students ORDER BY name").fetchall()
    if not rows:
        print("No student records yet.")
        return
    for row in rows:
        marks = (row["english"] + row["mathematics"] + row["computer"]) / 3
        print(f"{row['roll_no']:<12} {row['name']:<24} {marks:>7.2f}%  {grade(marks)}")

def search_student(db):
    query = input("Enter roll number: ").strip()
    row = db.execute("SELECT * FROM students WHERE roll_no = ?", (query,)).fetchone()
    if row:
        print_student(row)
    else:
        print("No student found with that roll number.")

def main():
    with connect() as db:
        while True:
            print("\n=== Student Result Management System ===")
            print("1. Add student result\n2. List all results\n3. Search by roll number\n4. Exit")
            choice = input("Choose: ").strip()
            if choice == "1":
                add_student(db)
            elif choice == "2":
                list_students(db)
            elif choice == "3":
                search_student(db)
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
