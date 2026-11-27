"""Student Attendance Manager (PS 17)
Each student is a dict: {roll, name, held, attended}, stored in attendance.txt
File format: one line per student -> roll|name|held|attended
"""

FILE_NAME = "attendance.txt"
MIN_PERCENT = 75.0


def load_data():
    students = []
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) != 4:
                    continue
                try:
                    students.append({
                        "roll": parts[0],
                        "name": parts[1],
                        "held": int(parts[2]),
                        "attended": int(parts[3]),
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return students


def save_data(students):
    with open(FILE_NAME, "w") as f:
        for s in students:
            f.write(f"{s['roll']}|{s['name']}|{s['held']}|{s['attended']}\n")


def find_student(students, roll):
    for s in students:
        if s["roll"] == roll:
            return s
    return None


def percentage(student):
    if student["held"] == 0:
        return None  # avoids division by zero
    return student["attended"] / student["held"] * 100


def add_student(students):
    roll = input("Roll: ").strip()
    if not roll:
        print("Roll number cannot be empty.")
        return
    if find_student(students, roll):
        print(f"Roll number {roll} already exists.")
        return
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    s = {"roll": roll, "name": name, "held": 0, "attended": 0}
    students.append(s)
    save_data(students)
    print(f"Student added: {roll} | {name} | Held: 0 | Attended: 0")


def mark_attendance(students):
    roll = input("Roll: ").strip()
    s = find_student(students, roll)
    if s is None:
        print(f"Roll number {roll} not found.")
        return
    status = input("Status (P/A): ").strip().upper()
    if status not in ("P", "A"):
        print("Invalid status. Enter P or A.")
        return
    s["held"] += 1
    if status == "P":
        s["attended"] += 1
    save_data(students)
    print(f"Attendance marked for {s['name']}: {status}")


def show_percentage(students):
    roll = input("Roll: ").strip()
    s = find_student(students, roll)
    if s is None:
        print(f"Roll number {roll} not found.")
        return
    pct = percentage(s)
    if pct is None:
        print(f"{s['name']}: Attendance 0.00% (no classes held yet)")
    else:
        print(f"{s['name']}: Attendance {pct:.2f}%")


def shortage_list(students):
    if not students:
        print("No students found.")
        return
    for s in students:
        pct = percentage(s)
        if pct is None:
            print(f"{s['name']}: no classes held yet.")
        elif pct < MIN_PERCENT:
            print(f"Below 75%: {s['roll']} | {s['name']} | {pct:.2f}%")
        else:
            print(f"{s['name']} ({pct:.2f}%) meets the requirement.")


def main():
    students = load_data()
    while True:
        print("\n--- Student Attendance Manager ---")
        print("1. Add student")
        print("2. Mark attendance")
        print("3. View attendance percentage")
        print("4. Shortage list (below 75%)")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            mark_attendance(students)
        elif choice == "3":
            show_percentage(students)
        elif choice == "4":
            shortage_list(students)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose 1-5.")


if __name__ == "__main__":
    main()
