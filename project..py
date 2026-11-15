"""Student Attendance Manager.

A menu-driven console application to manage student attendance records,
calculate attendance percentages, identify students with attendance shortage
(below the 75% requirement), and persist data to attendance.txt.

Language: Python 3
Concepts: Lists, Dictionaries, Functions, File Handling
"""

import ast
import json
import os
import sys

# Directory and file setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE_NAME = os.path.join(SCRIPT_DIR, "attendance.txt")

# Storage format detected: 'dict' (default) or 'csv'
STORAGE_FORMAT = "dict"


def load_data(filename=DEFAULT_FILE_NAME):
    """Load student records from attendance.txt."""
    global STORAGE_FORMAT
    students = []
    if not os.path.exists(filename):
        return students

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line:
                    continue

                # 1. Parse JSON / Python dictionary format
                if (line.startswith("{") and line.endswith("}")) or (line.startswith("[") and line.endswith("]")):
                    STORAGE_FORMAT = "dict"
                    try:
                        try:
                            parsed = json.loads(line)
                        except Exception:
                            parsed = ast.literal_eval(line)

                        if isinstance(parsed, dict) and "roll" in parsed and "name" in parsed:
                            students.append({
                                "roll": int(parsed["roll"]),
                                "name": str(parsed["name"]),
                                "held": int(parsed.get("held", 0)),
                                "attended": int(parsed.get("attended", 0))
                            })
                            continue
                        elif isinstance(parsed, list):
                            for item in parsed:
                                if isinstance(item, dict) and "roll" in item and "name" in item:
                                    students.append({
                                        "roll": int(item["roll"]),
                                        "name": str(item["name"]),
                                        "held": int(item.get("held", 0)),
                                        "attended": int(item.get("attended", 0))
                                    })
                            continue
                    except Exception:
                        pass

                # 2. Parse comma-separated format
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 4:
                    try:
                        students.append({
                            "roll": int(parts[0]),
                            "name": str(parts[1]),
                            "held": int(parts[2]),
                            "attended": int(parts[3])
                        })
                        STORAGE_FORMAT = "csv"
                        continue
                    except ValueError:
                        pass

                # 3. Parse pipe-separated format
                parts_pipe = [p.strip() for p in line.split("|")]
                if len(parts_pipe) >= 4:
                    try:
                        students.append({
                            "roll": int(parts_pipe[0]),
                            "name": str(parts_pipe[1]),
                            "held": int(parts_pipe[2]),
                            "attended": int(parts_pipe[3])
                        })
                        continue
                    except ValueError:
                        pass
    except Exception as e:
        print(f"Warning: Could not read file {filename}: {e}")

    return students


def save_data(students, filename=DEFAULT_FILE_NAME):
    """Save student records to attendance.txt after every change."""
    global STORAGE_FORMAT
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for s in students:
                if STORAGE_FORMAT == "csv":
                    f.write(f"{s['roll']},{s['name']},{s['held']},{s['attended']}\n")
                else:
                    f.write(f'{{"roll": {s["roll"]}, "name": "{s["name"]}", "held": {s["held"]}, "attended": {s["attended"]}}}\n')
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")


def find_student(students, roll):
    """Find a student dictionary by roll number."""
    try:
        target_roll = int(roll)
    except (ValueError, TypeError):
        return None

    for student in students:
        if student.get("roll") == target_roll:
            return student
    return None


def calculate_percentage(student):
    """Calculate the attendance percentage for a student.
    
    Avoids dividing by zero when no classes are held yet.
    """
    held = student.get("held", 0)
    attended = student.get("attended", 0)
    if held == 0:
        return 0.0
    return (attended / held) * 100.0


def add_student(students, roll=None, name=None, filename=DEFAULT_FILE_NAME):
    """Add a new student with unique roll number and initial 0 attendance."""
    if roll is None:
        roll = input("Roll: ").strip()

    try:
        roll_num = int(roll)
        if roll_num <= 0:
            print("Roll number must be a positive integer.")
            return False
    except (ValueError, TypeError):
        print("Invalid roll number. Please enter a valid numeric roll number.")
        return False

    if find_student(students, roll_num) is not None:
        print(f"Roll number {roll_num} already exists.")
        return False

    if name is None:
        name = input("Name: ").strip()

    name_clean = str(name).strip()
    if not name_clean:
        print("Name cannot be empty.")
        return False

    new_student = {
        "roll": roll_num,
        "name": name_clean,
        "held": 0,
        "attended": 0
    }
    students.append(new_student)
    save_data(students, filename=filename)
    print(f"Student added: {new_student['roll']} │ {new_student['name']} │ Held: {new_student['held']} │ Attended: {new_student['attended']}")
    return True


def mark_attendance(students, roll=None, status=None, filename=DEFAULT_FILE_NAME):
    """Mark daily attendance for a student as Present (P) or Absent (A)."""
    if roll is None:
        roll = input("Roll: ").strip()

    student = find_student(students, roll)
    if not student:
        print(f"Roll number {roll} not found.")
        return False

    if status is None:
        status = input("Status: ").strip()

    status_upper = str(status).strip().upper()
    if status_upper not in ("P", "A"):
        print("Invalid status. Enter P or A.")
        return False

    student["held"] += 1
    if status_upper == "P":
        student["attended"] += 1

    save_data(students, filename=filename)
    status_text = "Present" if status_upper == "P" else "Absent"
    print(f"Attendance marked for {student['name']} (Roll {student['roll']}): {status_text}")
    return True


def show_percentage(students, roll=None):
    """View a student's attendance percentage."""
    if roll is None:
        roll = input("Roll: ").strip()

    student = find_student(students, roll)
    if not student:
        print(f"Roll number {roll} not found.")
        return

    held = student.get("held", 0)
    if held == 0:
        print(f"{student['name']}: Attendance 0.00% (no classes held yet)")
    else:
        pct = calculate_percentage(student)
        print(f"{student['name']}: Attendance {pct:.2f}%")


def show_shortage_list(students):
    """List students below the 75% attendance requirement and those who meet it."""
    if not students:
        print("No student records found.")
        return

    below_75 = []
    meets_req = []

    for s in students:
        pct = calculate_percentage(s)
        if pct < 75.0:
            below_75.append((s, pct))
        else:
            meets_req.append((s, pct))

    print("Below 75%:")
    if below_75:
        for s, pct in below_75:
            print(f"{s['roll']} │ {s['name']} │ {pct:.2f}%")
    else:
        print("None")

    for s, pct in meets_req:
        print(f"{s['name']} ({pct:.2f}%) meets the requirement.")


def display_menu():
    """Display the application menu."""
    print("\n==============================")
    print("  Student Attendance Manager  ")
    print("==============================")
    print("1. Add student")
    print("2. Mark attendance")
    print("3. View percentage")
    print("4. Shortage list")
    print("5. Exit")
    print("==============================")


def main():
    """Main execution loop for the Student Attendance Manager console application."""
    students = load_data()
    print("Welcome to Student Attendance Manager!")
    print(f"Loaded {len(students)} record(s) from {os.path.basename(DEFAULT_FILE_NAME)}.")

    while True:
        display_menu()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            mark_attendance(students)
        elif choice == "3":
            show_percentage(students)
        elif choice == "4":
            show_shortage_list(students)
        elif choice == "5":
            print("Exiting Student Attendance Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select an option between 1 and 5.")


if __name__ == "__main__":
    main()